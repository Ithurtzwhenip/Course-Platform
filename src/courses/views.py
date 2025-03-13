from urllib import request
from urllib.error import HTTPError
from django.http import Http404
from django.shortcuts import render
from . import services


# Create your views here.

def course_list():
    queryset = services.get_publish_sources()
    return render(request, 'courses/list.html', {})


def course_detail(request, course_id=None, *args, **kwargs):
    course_obj = services.get_course_detail(course_id=course_id)
    if course_obj is None:
        raise Http404
    return render(request, 'courses/detail.html', {})


def lesson_detail(request, course_id=None, lesson_id=None, *args, **kwargs):
    lesson_obj = services.get_lesson_detail(
        course_id=course_id, lesson_id=lesson_id)
    if lesson_obj is None:
        raise Http404
    return render(request, 'courses/lesson.html', {})
