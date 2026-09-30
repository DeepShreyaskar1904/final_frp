from django.contrib import admin
from .models import *

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = (
        'student_name',
        'course',
        'rating',
        'sentiment',
        'created_at',
    )
    list_filter = (
        'rating',
        'sentiment',
        'course',
        'created_at',
    )
    search_fields = (
        'student_name',
        'student_email',
        'course',
        'feedback',
    )
    ordering = (
        '-created_at',
    )

@admin.register(FacultyProfile)
class FacultyProfileAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "designation",
        "students_trained",
        "updated_at",
    )


@admin.register(Education)
class EducationAdmin(admin.ModelAdmin):
    list_display = (
        "degree",
        "field_of_study",
        "status",
        "display_order",
    )
    list_filter = ("status",)


@admin.register(FacultySkill)
class FacultySkillAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "profile",
        "display_order",
    )