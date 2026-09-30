from django.db import models
class Review(models.Model):
    RATING_CHOICES = [
        (1, '1 - Very Poor'),
        (2, '2 - Poor'),
        (3, '3 - Average'),
        (4, '4 - Good'),
        (5, '5 - Excellent'),
    ]

    SENTIMENT_CHOICES = [
        ('positive', 'Positive'),
        ('neutral', 'Neutral'),
        ('negative', 'Negative'),
    ]

    student_name = models.CharField(max_length=150)

    student_email = models.EmailField()

    course = models.CharField(max_length=150)

    batch = models.CharField(
        max_length=100,
        blank=True,
        null = True
    )

    rating = models.PositiveSmallIntegerField(
        choices=RATING_CHOICES
    )

    teaching_quality = models.PositiveSmallIntegerField(
        choices=RATING_CHOICES
    )

    communication = models.PositiveSmallIntegerField(
        choices=RATING_CHOICES
    )

    practical_knowledge = models.PositiveSmallIntegerField(
        choices=RATING_CHOICES
    )

    doubt_solving = models.PositiveSmallIntegerField(
        choices=RATING_CHOICES
    )

    feedback = models.TextField()

    sentiment = models.CharField(
        max_length=20,
        choices=SENTIMENT_CHOICES,
        default='neutral'
    )

    is_anonymous = models.BooleanField(
        default=False
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.student_name} - {self.rating}/5"
from django.db import models


class FacultyProfile(models.Model):
    name = models.CharField(max_length=150)
    designation = models.CharField(max_length=150)

    profile_image = models.ImageField(
        upload_to="faculty/profile/",
        blank=True,
        null=True
    )

    short_intro = models.TextField(
        blank=True,
        help_text="Short introduction shown on the profile card."
    )

    about = models.TextField(
        blank=True,
        help_text="About section."
    )

    location = models.CharField(
        max_length=150,
        blank=True
    )

    email = models.EmailField(
        blank=True
    )

    students_trained = models.CharField(
        max_length=50,
        blank=True,
        help_text="Example: 700+"
    )

    teaching_approach = models.CharField(
        max_length=255,
        blank=True,
        help_text="Example: Learn → Try → Build → Improve"
    )

    quote = models.TextField(
        blank=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return self.name


class Education(models.Model):
    profile = models.ForeignKey(
        FacultyProfile,
        on_delete=models.CASCADE,
        related_name="educations"
    )

    degree = models.CharField(
        max_length=150
    )

    field_of_study = models.CharField(
        max_length=200
    )

    institution = models.CharField(
        max_length=200,
        blank=True
    )

    status = models.CharField(
        max_length=100,
        blank=True,
        help_text="Example: Currently pursuing / Completed"
    )

    start_year = models.PositiveIntegerField(
        blank=True,
        null=True
    )

    end_year = models.PositiveIntegerField(
        blank=True,
        null=True
    )

    display_order = models.PositiveIntegerField(
        default=0
    )

    def __str__(self):
        return f"{self.degree} - {self.field_of_study}"

    class Meta:
        ordering = ["display_order", "-end_year"]


class FacultySkill(models.Model):
    profile = models.ForeignKey(
        FacultyProfile,
        on_delete=models.CASCADE,
        related_name="skills"
    )

    name = models.CharField(
        max_length=100
    )

    display_order = models.PositiveIntegerField(
        default=0
    )

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["display_order", "name"]