from django.core.management.base import BaseCommand
from app.utils.link_scraper import get_urls
from app.utils.langchain_url_handler import load_documents, embed_documents
from app.models import ProcessedDocument


class Command(BaseCommand):
    help = "Scrape URLs, load documents, and embed their contents"

    def handle(self, *args, **options):
        try:
            scraped_links = get_urls()
            self.stdout.write(self.style.SUCCESS('Successfully scraped URLs'))
        except Exception as e:
            self.stderr.write(self.style.ERROR(f"Error while scraping URLs: {e}"))
            return

        try:
            documents = load_documents(scraped_links)
            self.stdout.write(self.style.SUCCESS('Successfully loaded documents'))
        except Exception as e:
            self.stderr.write(self.style.ERROR(f"Error while loading documents: {e}"))
            return

        try:
            embedded_documents = embed_documents(documents)
            self.stdout.write(self.style.SUCCESS('Successfully embedded documents'))
        except Exception as e:
            self.stderr.write(self.style.ERROR(f"Error while embedding documents: {e}"))
            return

        # Save documents to the database
        for document, embedded_document in zip(documents, embedded_documents):
            doc = ProcessedDocument(
                content=document.content,
                url=document.url,
                embedded_document=embedded_document,
            )
            doc.save()

        self.stdout.write(self.style.SUCCESS('Documents saved to the database'))