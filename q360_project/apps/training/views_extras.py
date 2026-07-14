from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils.translation import gettext_lazy as _
from .models import TrainingResource, LearningPath, CourseCategory, Exam

@login_required
def courses_list(request):
    """
    Bütün aktiv kurslar/təlimlər siyahısı.
    """
    courses = TrainingResource.objects.filter(is_active=True)
    
    context = {
        'title': _('Kurslar və Təlimlər'),
        'courses': courses
    }
    return render(request, 'training/courses.html', context)


@login_required
def learning_paths_list(request):
    """
    Öyrənmə yolları siyahısı.
    """
    paths = LearningPath.objects.prefetch_related('courses').filter(is_active=True)
    
    context = {
        'title': _('Öyrənmə Yolları'),
        'paths': paths
    }
    return render(request, 'training/learning_paths.html', context)


@login_required
def course_categories_list(request):
    """
    Kurs kateqoriyalarının siyahısı.
    """
    categories = CourseCategory.objects.all()
    
    context = {
        'title': _('Kurs Kateqoriyaları'),
        'categories': categories
    }
    return render(request, 'training/course_categories.html', context)


@login_required
def exams_list(request):
    """
    İmtahanlar və qiymətləndirmələr.
    """
    exams = Exam.objects.select_related('course').filter(is_active=True)
    
    context = {
        'title': _('İmtahanlar'),
        'exams': exams
    }
    return render(request, 'training/exams.html', context)
