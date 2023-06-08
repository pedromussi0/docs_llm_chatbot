from django.core.management.base import BaseCommand
from app.utils.langchain_url_handler import embed_documents
from app.models import Document


class Command(BaseCommand):
    help = "Embed documents and save them to the database"

    def handle(self, *args, **options):
        documents = Document.objects.all()
        embed_documents(documents)
        self.stdout.write(self.style.SUCCESS('Successfully embedded documents'))
