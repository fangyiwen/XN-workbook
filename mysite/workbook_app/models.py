import datetime

from django.db import models
from django.utils import timezone


class Course(models.Model):
	objects = models.Manager()
	course_id = models.CharField(max_length=30, unique=True)
	course_name = models.CharField(max_length=300, unique=True)
	pub_date = models.DateTimeField(verbose_name='date published')
	course_instructor = models.CharField(max_length=30)

	def __str__(self):
		return self.course_name

	def was_published_recently(self):
		now = timezone.now()
		return now - datetime.timedelta(days=1) <= self.pub_date <= now

	was_published_recently.admin_order_field = 'pub_date'
	was_published_recently.boolean = True
	was_published_recently.short_description = 'Published recently?'


class Quiz(models.Model):
	objects = models.Manager()
	course = models.ForeignKey(Course, on_delete=models.CASCADE)  # one to many relationship
	quiz_number = models.CharField(max_length=30, verbose_name='quiz No.')
	quiz_id = models.CharField(max_length=30, default=quiz_number, editable=False)
	quiz_name = models.CharField(max_length=60)
	pub_date = models.DateTimeField('date published')
	quiz_date = models.DateTimeField('the date of quiz')

	def __str__(self):
		return self.course.course_id + " " + self.quiz_name

	def save(self, **kwargs):
		super(Quiz, self).save(**kwargs)
		self.quiz_id = str(self.course.course_id) + "_" + str(self.quiz_number)
		super(Quiz, self).save(**kwargs)


class Question(models.Model):
	objects = models.Manager()
	quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
	question_number =  models.CharField(max_length=30, verbose_name='question No.')
	question_id = models.CharField(max_length=30, default=question_number, editable=False)
	question_text = models.CharField(max_length=300)
	question_answer = models.CharField(max_length=30, verbose_name='Answer')

	# pub_date = models.DateTimeField('date published')

	def __str__(self):
		return self.question_text

	def save(self, **kwargs):
		super(Question, self).save(**kwargs)
		self.question_id = str(self.quiz.quiz_id) + "_" + str(self.question_number)
		super(Question, self).save(**kwargs)

	def was_published_recently(self):
		return self.pub_date >= timezone.now() - datetime.timedelta(days=1)

	was_published_recently.admin_order_field = 'pub_date'
	was_published_recently.boolean = True
	was_published_recently.short_description = 'Published recently?'


class Option(models.Model):
	objects = models.Manager()
	question = models.ForeignKey(Question, on_delete=models.CASCADE)
	option_number = models.CharField(max_length=30, verbose_name='option No.')
	option_text = models.CharField(max_length=300)

	def __str__(self):
		return ''
