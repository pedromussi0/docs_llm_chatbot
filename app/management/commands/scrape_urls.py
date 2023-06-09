from django.core.management.base import BaseCommand
from app.utils.link_scraper import get_urls


class Command(BaseCommand):
    help = "Scrape URLs from the specified website"

    def handle(self, *args, **options):
        scraped_links = get_urls()

        # Save scraped_links to a file or other data storage
        with open("scraped_links.txt", "w") as f:
            for link in scraped_links:
                f.write(f"{link}\n")

        self.stdout.write(self.style.SUCCESS("Successfully scraped URLs"))
