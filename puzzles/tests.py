from datetime import timedelta
from unittest.mock import patch

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from .models import Puzzle, Submission
from .services import process_puzzle


class PuzzleLifecycleTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user("solver", password="test-password-123")
        self.client.login(username="solver", password="test-password-123")

    def create_puzzle(self, start):
        return Puzzle.objects.create(title="Test", content="What is 3.14?", correct_answer="3.14", solution="It is pi.", start_time=start)

    def test_end_time_is_exactly_24_hours(self):
        start = timezone.now()
        puzzle = self.create_puzzle(start)
        self.assertEqual(puzzle.end_time, start + timedelta(hours=24))

    def test_puzzle_page_lists_every_active_puzzle(self):
        first = self.create_puzzle(timezone.now() - timedelta(hours=2))
        second = Puzzle.objects.create(
            title="Second active puzzle", content="A second challenge", correct_answer="2",
            solution="Two.", start_time=timezone.now() - timedelta(hours=1),
        )
        response = self.client.get(reverse("puzzles:current"))
        self.assertContains(response, first.title)
        self.assertContains(response, second.title)

    def test_before_start_rejects_submission(self):
        puzzle = self.create_puzzle(timezone.now() + timedelta(hours=1))
        self.client.post(reverse("puzzles:submit", args=(puzzle.pk,)), {"answer": "3.14"})
        self.assertFalse(Submission.objects.exists())

    def test_decimal_equivalence_and_one_submission(self):
        puzzle = self.create_puzzle(timezone.now() - timedelta(hours=1))
        self.client.post(reverse("puzzles:submit", args=(puzzle.pk,)), {"answer": "3.140"})
        submission = Submission.objects.get()
        self.assertTrue(submission.is_correct)
        self.client.post(reverse("puzzles:submit", args=(puzzle.pk,)), {"answer": "3.14"})
        self.assertEqual(Submission.objects.count(), 1)

    def test_invalid_number_creates_no_submission(self):
        puzzle = self.create_puzzle(timezone.now() - timedelta(hours=1))
        response = self.client.post(reverse("puzzles:submit", args=(puzzle.pk,)), {"answer": "not a number"})
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Submission.objects.exists())

    def test_expired_puzzle_awards_points_once_and_resets_skips(self):
        other = User.objects.create_user("skipped", password="test-password-123")
        self.user.profile.current_streak = 2; self.user.profile.save()
        other.profile.current_streak = 4; other.profile.save()
        puzzle = self.create_puzzle(timezone.now() - timedelta(hours=25))
        Submission.objects.create(user=self.user, puzzle=puzzle, submitted_value="3.140", is_correct=True)
        process_puzzle(puzzle)
        self.user.profile.refresh_from_db(); other.profile.refresh_from_db(); puzzle.refresh_from_db()
        self.assertEqual(self.user.profile.points, 10)
        self.assertEqual(self.user.profile.current_streak, 3)
        self.assertEqual(other.profile.current_streak, 0)
        self.assertEqual(puzzle.winner, self.user)
        process_puzzle(puzzle)
        self.user.profile.refresh_from_db()
        self.assertEqual(self.user.profile.points, 10)

    def test_admin_process_button_triggers_puzzle_processing(self):
        admin_user = User.objects.create_superuser("admin_tester", "admin@dbit.ac.in", "adminpass123")
        self.client.login(username="admin_tester", password="adminpass123")
        puzzle = self.create_puzzle(timezone.now() - timedelta(hours=2))
        Submission.objects.create(user=self.user, puzzle=puzzle, submitted_value="3.14", is_correct=True)
        
        # Call the admin process URL
        response = self.client.get(f"/admin/puzzles/puzzle/process/{puzzle.pk}/", follow=True)
        self.assertEqual(response.status_code, 200)
        puzzle.refresh_from_db()
        self.assertTrue(puzzle.is_processed)
        self.assertEqual(puzzle.winner, self.user)
        self.user.profile.refresh_from_db()
        self.assertEqual(self.user.profile.points, 10)

    def test_admin_process_all_expired_url(self):
        admin_user = User.objects.create_superuser("admin_tester2", "admin2@dbit.ac.in", "adminpass123")
        self.client.login(username="admin_tester2", password="adminpass123")
        p1 = self.create_puzzle(timezone.now() - timedelta(hours=30))
        Submission.objects.create(user=self.user, puzzle=p1, submitted_value="3.14", is_correct=True)
        
        response = self.client.get("/admin/puzzles/puzzle/process-all/", follow=True)
        self.assertEqual(response.status_code, 200)
        p1.refresh_from_db()
        self.assertTrue(p1.is_processed)
        self.assertEqual(p1.winner, self.user)

