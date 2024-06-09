from django.shortcuts import render, reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.db.models import F, Sum

from django.views import generic

from .models import Question, Choice
# Create your views here.


class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = "latest_questions"

    def get_queryset(self):
        return Question.objects.order_by("-pub_date")[:5] \
        .annotate(total_votes=Sum("choice__votes"))


class DetailView(generic.DetailView):
    model = Question
    template_name = "polls/detail.html"

class ResultView(generic.DetailView):
    model = Question
    template_name = "polls/results.html"


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)

    if not question.open:
        return render(
            request,
            "polls/detail.html",
            {
                "question": question,
                "error_message": "Voting closed"
            }
        )

    try:
        selected_choice = question.choice_set.get(pk=request.POST["choice"])
    except (Choice.DoesNotExist, KeyError):
        return render(
            request,
            "polls/detail.html",
            {
                "question": question,
                "error_message": "You did not select choice"
            }
        )
        pass
    else:
        selected_choice.votes = F("votes") + 1
        selected_choice.save()
        return HttpResponseRedirect(reverse("polls:results", args=(question_id,)))