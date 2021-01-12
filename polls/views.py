from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, Http404
from .models import Question, Choice
from django.template import loader
from django.urls import reverse, reverse_lazy
from django.views import generic
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone


class IndexView(generic.ListView):
    template_name = 'polls/index.html'

    context_object_name = 'latest_question_list'
    def get_queryset(self):
        """Return the last five published questions."""
        return Question.objects.filter(pub_date__lte=timezone.now()
        ).order_by('-pub_date')[:3]

    def get_context_data(self):
        """Return a list of all polls."""
        context = super(IndexView, self).get_context_data()
        context['all_polls'] = Question.objects.all()
        return context


class CreateView(LoginRequiredMixin, generic.CreateView):
    success_url = reverse_lazy('polls:index')
    redirect_field_name = 'accounts:signup'
    model = Question
    fields = ['question_text']
    template_name = 'polls/poll_form.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        response = super(CreateView, self).form_valid(form)
        return response


class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'


def vote(request, question_id):
    question = get_object_or_404(Question, id=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))


