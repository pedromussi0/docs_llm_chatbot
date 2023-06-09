from django.core.management.base import BaseCommand
from app.utils.langchain_url_handler import load_documents

# from app.models import Document


class Command(BaseCommand):
    help = "Load documents from the scraped URLs"

    def handle(self, *args, **options):
        # Load scraped_links from the file or other data storage
        with open("scraped_links.txt", "r") as f:
            scraped_links = [line.strip() for line in f.readlines()]

        documents = load_documents(scraped_links)

        # for doc in documents:
        # Save the returned documents to the database
        # Document.objects.create(content=doc.content, metadata=doc.metadata)

        self.stdout.write(self.style.SUCCESS("Successfully loaded documents"))
