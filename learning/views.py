from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.db.models import Count, Q, Avg
from .models import Course, Lesson, UserCourseProgress

@login_required
def course_list(request):
    courses = Course.objects.annotate(
        lesson_count=Count('lessons'),
        total_duration=Count('lessons__duration_minutes')
    ).all()
    
    # Calculate progress for each course
    courses_with_progress = []
    for course in courses:
        completed_lessons = UserCourseProgress.objects.filter(
            user=request.user,
            lesson__course=course,
            completed=True
        ).count()
        
        total_lessons = course.lessons.count()
        progress_percent = 0
        if total_lessons > 0:
            progress_percent = round((completed_lessons / total_lessons) * 100)
        
        # Calculate total duration
        total_duration = sum([lesson.duration_minutes or 0 for lesson in course.lessons.all()])
        hours = total_duration // 60
        minutes = total_duration % 60
        duration_str = f"{hours}h {minutes}m" if hours > 0 else f"{minutes}m"
        
        courses_with_progress.append({
            'course': course,
            'progress_percent': progress_percent,
            'total_lessons': total_lessons,
            'completed_lessons': completed_lessons,
            'duration_str': duration_str,
            'total_duration': total_duration
        })
    
    # Overall stats
    total_courses = courses.count()
    total_lessons_all = Lesson.objects.count()
    completed_all = UserCourseProgress.objects.filter(user=request.user, completed=True).count()
    overall_progress = 0
    if total_lessons_all > 0:
        overall_progress = round((completed_all / total_lessons_all) * 100)
    
    context = {
        'courses_data': courses_with_progress,
        'total_courses': total_courses,
        'total_lessons': total_lessons_all,
        'completed_lessons': completed_all,
        'overall_progress': overall_progress
    }
    return render(request, 'learning/course_list.html', context)

@login_required
def course_detail(request, pk):
    course = get_object_or_404(Course, pk=pk)
    lessons = course.lessons.all()
    
    # Calculate progress
    completed_lessons = UserCourseProgress.objects.filter(
        user=request.user, 
        lesson__course=course, 
        completed=True
    ).values_list('lesson_id', flat=True)
    
    progress_percent = 0
    if lessons.count() > 0:
        progress_percent = (len(completed_lessons) / lessons.count()) * 100
        
    return render(request, 'learning/course_detail.html', {
        'course': course,
        'lessons': lessons,
        'completed_lessons': completed_lessons,
        'progress_percent': round(progress_percent),
    })

@login_required
def lesson_detail(request, course_pk, lesson_pk):
    course = get_object_or_404(Course, pk=course_pk)
    lesson = get_object_or_404(Lesson, pk=lesson_pk, course=course)
    
    # Mark as completed
    UserCourseProgress.objects.get_or_create(
        user=request.user,
        lesson=lesson,
        defaults={'completed': True, 'completed_at': timezone.now()}
    )
    
    # Get next lesson
    next_lesson = course.lessons.filter(order__gt=lesson.order).order_by('order').first()
    prev_lesson = course.lessons.filter(order__lt=lesson.order).order_by('-order').first()
    
    # If no lesson found by order (e.g. same order), try by ID as fallback
    if not next_lesson:
        next_lesson = course.lessons.filter(order=lesson.order, pk__gt=lesson.pk).order_by('pk').first()
    if not prev_lesson:
        prev_lesson = course.lessons.filter(order=lesson.order, pk__lt=lesson.pk).order_by('-pk').first()
    
    return render(request, 'learning/lesson_detail.html', {
        'course': course,
        'lesson': lesson,
        'next_lesson': next_lesson,
        'prev_lesson': prev_lesson,
    })

# Admin CRUD Views
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import UserPassesTestMixin

class SuperUserRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_superuser

class CourseCreateView(SuperUserRequiredMixin, CreateView):
    model = Course
    fields = ['title', 'description', 'thumbnail']
    template_name = 'learning/course_form.html'
    success_url = reverse_lazy('course_list')

class CourseUpdateView(SuperUserRequiredMixin, UpdateView):
    model = Course
    fields = ['title', 'description', 'thumbnail']
    template_name = 'learning/course_form.html'
    success_url = reverse_lazy('course_list')

class CourseDeleteView(SuperUserRequiredMixin, DeleteView):
    model = Course
    template_name = 'learning/course_confirm_delete.html'
    success_url = reverse_lazy('course_list')

class LessonCreateView(SuperUserRequiredMixin, CreateView):
    model = Lesson
    fields = ['title', 'content_type', 'content', 'video_url', 'external_link', 'duration_minutes', 'order']
    template_name = 'learning/lesson_form.html'
    
    def form_valid(self, form):
        if 'course_pk' in self.kwargs:
            course = get_object_or_404(Course, pk=self.kwargs['course_pk'])
            form.instance.course = course
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if 'course_pk' in self.kwargs:
            context['course'] = get_object_or_404(Course, pk=self.kwargs['course_pk'])
        return context

    def get_success_url(self):
        return reverse_lazy('course_detail', kwargs={'pk': self.object.course.pk})

class LessonUpdateView(SuperUserRequiredMixin, UpdateView):
    model = Lesson
    fields = ['title', 'content_type', 'content', 'video_url', 'external_link', 'duration_minutes', 'order']
    template_name = 'learning/lesson_form.html'
    
    def get_success_url(self):
        return reverse_lazy('course_detail', kwargs={'pk': self.object.course.pk})

class LessonDeleteView(SuperUserRequiredMixin, DeleteView):
    model = Lesson
    template_name = 'learning/lesson_confirm_delete.html'
    
    def get_success_url(self):
        return reverse_lazy('course_detail', kwargs={'pk': self.object.course.pk})
