from django.views import View
from django.shortcuts import render, get_object_or_404, redirect

from .models import Course
from .forms import CourseForm


class CoursesView(View):
    template_name = 'course_generic.html'

    def get(self, request, course_id=None, *args, **kwargs):
        context = {}

        if course_id:
            course = get_object_or_404(Course, id=course_id)
            context['course'] = course
            context['page_title'] = f"Course {course}"

        return render(request, self.template_name, context)


class CoursesListView(View):
    template_name = 'courses_list.html'

    def get(self, request, *args, **kwargs):
        courses = Course.objects.all()

        context = {
            'courses': courses,
            'page_title': 'Courses'
        }

        return render(request, self.template_name, context)

class CourseFormView(View):
    def get_object_instance(self):
        course_id = self.kwargs.get('course_id')
        return get_object_or_404(Course, id=course_id)

    def get_form(self, request):
        course_id = self.kwargs.get('course_id')

        if course_id:
            course_object = self.get_object_instance()

            form = {
                'GET': CourseForm(instance=course_object),
                'POST': CourseForm(request.POST, instance=course_object)
            }

            return form[request.method]

        else:
            form = {
                'GET': CourseForm(),
                'POST': CourseForm(request.POST)
            }

            return form[request.method]

class CourseCreateUpdateView(CourseFormView, View):
    page_title = ''
    template_name = 'course_form.html'

    def get(self, request, *args, **kwargs):
        form = self.get_form(request)
        context = {
            'form': form,
            'page_title': self.page_title,
        }

        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = self.get_form(request)

        if form.is_valid():
            form.save()
            return redirect('courses:index')

        context = {
            'form': form,
            'page_title': self.page_title,
        }

        return render(request, self.template_name, context)

class CourseDeleteView(CourseFormView, View):
    template_name = 'course_delete.html'
    course = None

    def get(self, request, *args, **kwargs):
        self.course = self.get_object_instance()
        context = {
            'course': self.course,
        }

        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        course = self.get_object_instance()
        course.delete()
        return redirect('courses:index')

        context = {
            'course': self.course,
        }

        return render(request, self.template_name, context)
