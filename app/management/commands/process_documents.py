from django.core.management.base import BaseCommand
from app.utils.link_scraper import scrape_links
from app.utils.langchain_url_handler import load_documents, embed_documents
from app.models import ProcessedDocument
from django.conf import settings


class Command(BaseCommand):
    help = "Scrape URLs, load documents, and embed their contents"

    def handle(self, *args, **options):
        scraped_links = scrape_links(url=settings.NEXT_DOCS_URL)
        self.stdout.write(self.style.SUCCESS("Successfully scraped URLs"))

        # self.stderr.write(self.style.ERROR(f"Error while scraping URLs: {e}"))
        # return

        scraped_links = scraped_links[0:3]
        documents = load_documents(scraped_links)
        for doc in documents:
            print(doc)
        self.stdout.write(self.style.SUCCESS("Successfully loaded documents"))

        # self.stderr.write(self.style.ERROR(f"Error while loading documents: {e}"))
        # return

        embedded_documents = embed_documents(documents)

        self.stdout.write(self.style.SUCCESS("Successfully embedded documents"))
        # except Exception as e:
        #     self.stderr.write(self.style.ERROR(f"Error while embedding documents: {e}"))
        #     return

        # # Save documents to the database
        # for document, embedded_document in zip(documents, embedded_documents):
        #     doc = ProcessedDocument(
        #         content=document.content,
        #         url=document.url,
        #         embedded_document=embedded_document,
        #     )
        #     doc.save()

        # self.stdout.write(self.style.SUCCESS('Documents saved to the database'))
