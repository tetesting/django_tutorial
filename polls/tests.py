from django.test import TestCase
from django.core.urlresolvers import reverse
from django.utils import timezone
import datetime

from polls.models import Poll


def create_poll(question, days):
    """
    Creates a poll with the given `question` published the given number of
    `days` offset to now (negative for polls published in the past,
    positive for polls that have yet to be published).
    """
    return Poll.objects.create(question=question,
        pub_date=timezone.now()+datetime.timedelta(days=days))


class PollMethodTests(TestCase):
    def test_was_published_recently_with_future_poll(self):
        """
        was_published_recently() should return False for polls whose
        pub_date is in the future
        """
        future_poll = create_poll(question="Future poll.", days=30)
        self.assertEqual(future_poll.was_published_recently(), False)

    def test_was_published_recently_with_old_poll(self):
        """
        was_published_recently() should return False for polls whose 
        pub_date is older than 1 day
        """
        old_poll = create_poll(question="Old poll.", days=-30)
        self.assertEqual(old_poll.was_published_recently(), False)

    def test_was_published_recently_with_recent_poll(self):
        """
        was_published_recently() should return True for polls whose 
        pub_date is within the last_day
        """
        recent_poll = create_poll(question="Recent poll.", days=-0.5)
        self.assertEqual(recent_poll.was_published_recently(), True)

