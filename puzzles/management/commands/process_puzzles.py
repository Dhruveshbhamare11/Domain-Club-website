from django.core.management.base import BaseCommand
from puzzles.services import process_expired_puzzles


class Command(BaseCommand):
    help = "Process expired weekly puzzles, scores, streaks, badges, and rankings."

    def handle(self, *args, **options):
        results = process_expired_puzzles()
        if not results:
            self.stdout.write("No expired unprocessed puzzles found.")
        for result in results:
            winner = result["winner"].username if result["winner"] else "None"
            self.stdout.write(self.style.SUCCESS(f"Processed {result['puzzle'].title}: winner={winner}, correct={result['correct']}, points awarded={result['points']}"))

