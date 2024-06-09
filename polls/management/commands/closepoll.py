from django.core.management.base import BaseCommand, CommandError
from polls.models import Question as Poll

class Command(BaseCommand):
    help = "Close poll for voting"

    def add_arguments(self, parser):
        parser.add_argument("poll_ids", nargs="+", type=int)
        parser.add_argument("--open",action="store_true")

    def handle(self, *args, **options):
        for poll_id in options["poll_ids"]:
            try:
                poll = Poll.objects.get(pk=poll_id)
            except Poll.DoesNotExist:
                raise CommandError("Poll %s does not exist" % poll_id)

            poll.open = False

            if options["open"]:
                poll.open = True

            poll.save()

            self.stdout.write(
                self.style.SUCCESS('Successfully closed %s' % poll_id)
            )