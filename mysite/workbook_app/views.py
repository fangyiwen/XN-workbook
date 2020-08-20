from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from django.views import generic
from django.utils import timezone

from .models import Course, Quiz, Question, Option


def index(request):
    course_list = Course.objects.order_by('-pub_date')[:5]
    template = loader.get_template('workbook_app/index.html')
    context = {
        'course_list': course_list,
    }
    return HttpResponse(template.render(context, request))


class CourseView(generic.ListView):
    model = Course
    template_name = 'workbook_app/courses_list.html'
    context_object_name = 'latest_course_list'

    def get_queryset(self):
        return Course.objects.order_by('course_id')[:]


class CourseQuizList(generic.ListView):
    model = Course
    template_name = 'workbook_app/course_quizzes_list.html'
    context_object_name = 'course_quiz_list'

    def get_queryset(self):
        return Course.objects.get(course_id=self.kwargs['course_id']).quiz_set.all().order_by('quiz_id')


class QuizQuestionList(generic.ListView):
    model = Course
    template_name = 'workbook_app/quiz_questions_list.html'
    context_object_name = 'quiz_question_list'

    def get_queryset(self):
        quiz_set = Course.objects.get(course_id=self.kwargs['course_id']).quiz_set.all()
        return quiz_set.get(quiz_id=self.kwargs['quiz_id']).question_set.all().order_by('question_id')


class QuestionDetailView(generic.DetailView):
    model = Question
    template_name = 'workbook_app/question_detail.html'
    slug_field = 'question_id'


def results(request, course_id, quiz_id, rate, percent_rate):
    template = loader.get_template('workbook_app/results.html')
    # after redirect, the rate becomes string, so use float to cast type
    return render(request, 'workbook_app/results.html', {'rate': float(rate), 'percent_rate': percent_rate})


def choose(request, course_id, quiz_id):
    quiz_set = Quiz.objects.filter(quiz_id=quiz_id)  # quiz__quiz_id !!!
    quiz = quiz_set[0]
    question_set = quiz.question_set.all()
    count = 0
    total_questions = len(question_set)
    post_answer_number = 0
    # calculate the number of answered questions of student's submission
    # using len(request.POST.keys()) doesn't work here!
    for question in question_set:
        post_answer_number += 1 if request.POST.get(question.question_id, '-1') != '-1' else 0
    # if the questions are not all answered, return the view to ask student to finish them.
    if post_answer_number != total_questions:
        return render(request, 'workbook_app/error.html')
    for question in question_set:
        if request.POST[question.question_id] == question.question_answer:
            count += 1
    # selected_option.save()
    # Always return an HttpResponseRedirect after successfully dealing
    # with POST data. This prevents data from being posted twice if a
    # user hits the Back button.
    # return HttpResponseRedirect(reverse('workbook_app:results', args=(course_id, quiz_id, rate)))
    # return HttpResponse("Congratulations! Your accuracy rate is %.2f%%!" % (rate * 100))
    rate = round(count / total_questions, 2)
    percent_rate = str(count / total_questions * 100) + '%'
    return HttpResponseRedirect(reverse('workbook_app:results', args=(course_id, quiz_id, rate, percent_rate)))

