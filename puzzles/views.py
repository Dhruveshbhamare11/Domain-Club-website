from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from .forms import SubmissionForm
from .models import Puzzle, Submission
from .services import answers_match


def current_puzzle(request):
    active_puzzles = Puzzle.objects.filter(
        start_time__lte=timezone.now(), end_time__gt=timezone.now()
    ).order_by("start_time")
    return render(request, "puzzles/puzzle_list.html", {"puzzles": active_puzzles})


def puzzle_detail(request, pk):
    puzzle = get_object_or_404(Puzzle, pk=pk)
    submission = request.user.submissions.filter(puzzle=puzzle).first() if request.user.is_authenticated else None
    return render(request, "puzzles/puzzle.html", {"puzzle": puzzle, "submission": submission, "form": SubmissionForm()})


@login_required
def submit(request, pk):
    if request.method != "POST": return redirect("puzzles:detail", pk=pk)
    puzzle = get_object_or_404(Puzzle, pk=pk)
    now = timezone.now()
    if not (puzzle.start_time <= now < puzzle.end_time):
        messages.error(request, "This puzzle is not accepting submissions.")
        return redirect("puzzles:detail", pk=pk)
    if Submission.objects.filter(user=request.user, puzzle=puzzle).exists():
        messages.error(request, "You have already submitted an answer for this puzzle.")
        return redirect("puzzles:detail", pk=pk)
    form = SubmissionForm(request.POST)
    if not form.is_valid():
        return render(request, "puzzles/puzzle.html", {"puzzle": puzzle, "form": form, "submission": None})
    try:
        submission = Submission.objects.create(user=request.user, puzzle=puzzle, submitted_value=form.cleaned_data["answer"], is_correct=answers_match(form.cleaned_data["answer"], puzzle.correct_answer))
    except IntegrityError:
        messages.error(request, "You have already submitted an answer for this puzzle.")
    else:
        messages.success(request, "Answer submitted. Results are revealed when the puzzle closes.")
    return redirect("puzzles:detail", pk=pk)


def archive(request):
    return render(request, "puzzles/puzzle_archive.html", {"puzzles": Puzzle.objects.filter(end_time__lte=timezone.now())})
