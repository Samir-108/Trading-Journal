from django.db import models
from django.conf import settings

class Course(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    thumbnail = models.ImageField(upload_to='course_thumbnails/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title

class Lesson(models.Model):
    CONTENT_TYPES = (
        ('TEXT', 'Text/Markdown'),
        ('VIDEO', 'YouTube Video'),
        ('LINK', 'External Link'),
    )
    
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='lessons')
    title = models.CharField(max_length=200)
    content_type = models.CharField(max_length=10, choices=CONTENT_TYPES, default='TEXT')
    content = models.TextField(help_text="Markdown text, YouTube URL, or External Link URL", blank=True)
    video_url = models.URLField(blank=True, null=True, help_text="YouTube Video URL")
    external_link = models.URLField(blank=True, null=True, help_text="External Resource Link")
    order = models.PositiveIntegerField(default=0)
    duration_minutes = models.PositiveIntegerField(default=10, help_text="Estimated duration in minutes")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.course.title} - {self.title}"

class UserCourseProgress(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='course_progress')
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ('user', 'lesson')

    def __str__(self):
        return f"{self.user.username} - {self.lesson.title}"
