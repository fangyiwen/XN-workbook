from django.contrib import admin
from django.urls import reverse
from django.db import models
from django import forms
import nested_admin

from .models import Course, Quiz, Question, Option


class OptionInline(nested_admin.NestedTabularInline):
    model = Option
    extra = 4
    # formfield_overrides = {
    #     models.TextField: {'widget': forms.TextInput}
    # }


class QuestionInline(nested_admin.NestedStackedInline):
    model = Question
    extra = 3
    inlines = [OptionInline]
    # formfield_overrides = {
    #     models.TextField: {'widget': forms.TextInput}
    # }


class QuizInline(admin.TabularInline):
    model = Quiz
    extra = 3
    inlines = [QuestionInline]


class QuestionAdmin(nested_admin.NestedModelAdmin):
    inlines = [OptionInline]
    list_display = ('get_course_id', 'get_course_name', 'get_course_instructor', 'get_quiz_number', 'question_number')
    list_display_links = ('get_course_id', 'question_number')
    search_fields = ['quiz_id']

    def get_course_id(self, obj):
        return obj.quiz.course.course_id

    def get_course_name(self, obj):
        return obj.quiz.course.course_name

    def get_course_instructor(self, obj):
        return obj.quiz.course.course_instructor

    def get_quiz_number(self, obj):
        return  obj.quiz.quiz_number

    get_course_id.short_description = 'Course ID'
    get_course_name.short_description = 'Course Name'
    get_course_instructor.short_description = 'Course Instructor'
    get_quiz_number.short_description = 'Quiz No.'


class QuizAdmin(nested_admin.NestedModelAdmin):
    inlines = [QuestionInline]
    list_display = ('get_course_id', 'get_course_name', 'quiz_id', 'quiz_name', 'pub_date')
    list_display_links = ('get_course_id', 'quiz_id', 'quiz_name')
    list_filter = ['pub_date']
    search_fields = ['quiz_name']

    def get_course_id(self, obj):
        return obj.course.course_id

    def get_course_name(self, obj):
        return obj.course.course_name

    get_course_id.admin_order_field = 'course__course_id'  # Allows column order sorting
    get_course_id.short_description = 'Course ID'  # Renames column head

    get_course_name.admin_order_field = 'course__course_name'  # Allows column order sorting
    get_course_name.short_description = 'Course Name'  # Renames column head


class CourseAdmin(admin.ModelAdmin):
    inlines = [QuizInline]
    list_display = ('course_id', 'course_name', 'course_instructor', 'pub_date')
    list_display_links = ('course_id', 'course_name')
    list_filter = ['pub_date']
    search_fields = ['course_name']


admin.site.register(Course, CourseAdmin)
admin.site.register(Quiz, QuizAdmin)
admin.site.register(Question, QuestionAdmin)


