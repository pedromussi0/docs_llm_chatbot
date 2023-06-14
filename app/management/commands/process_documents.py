from django.core.management.base import BaseCommand
from app.utils.link_scraper import scrape_links
from app.utils.langchain_url_handler import load_documents, embed_documents
from app.models import ProcessedDocument
from django.conf import settings


class Command(BaseCommand):
    help = "Scrape URLs, load documents, and save them to the db"

    def handle(self, *args, **options):
        error_urls = []
        existing_urls = set(ProcessedDocument.objects.values_list("url", flat=True))
        processed_urls = set()  # Track processed URLs

        try:
            scraped_links = scrape_links(url=settings.NEXT_DOCS_URL)
            self.stdout.write(self.style.SUCCESS("Successfully scraped URLs"))
        except ValueError as e:
            self.stderr.write(self.style.ERROR(f"Error while scraping URLs: {e}"))
            return

        for url in scraped_links:
            if url in existing_urls or url in processed_urls:
                self.stdout.write(
                    self.style.WARNING(
                        f"Duplicate URL found. Skipping processing: {url}"
                    )
                )
                continue

            try:
                documents = load_documents([url])
                self.stdout.write(
                    self.style.SUCCESS(f"Successfully loaded document from URL: {url}")
                )
            except ValueError:
                self.stderr.write(
                    self.style.ERROR(f"Error while loading document from URL: {url}")
                )
                error_urls.append(url)
                continue

            # Save the document to the database
            for document in documents:
                try:
                    if document.metadata["source"] in existing_urls:
                        self.stdout.write(
                            self.style.WARNING(
                                f"Duplicate URL found. Skipping saving: {document.metadata['source']}"
                            )
                        )
                        continue

                    doc = ProcessedDocument(
                        content=document.page_content,
                        url=document.metadata["source"],
                    )
                    doc.save()
                    processed_urls.add(document.metadata["source"])  # Add processed URL
                    existing_urls.add(document.metadata["source"])
                    self.stdout.write(
                        self.style.SUCCESS(
                            f"Document saved to the database: {document.metadata['source']}"
                        )
                    )
                except Exception:
                    error_urls.append(document.metadata["source"])
                    self.stderr.write(
                        self.style.ERROR(
                            f"Error saving document with URL: {document.metadata['source']}"
                        )
                    )

        # Handle errors
        for url in error_urls:
            self.stderr.write(
                self.style.ERROR(f"Document processing failed for URL: {url}")
            )
