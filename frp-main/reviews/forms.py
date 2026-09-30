from django import forms
from .models import *
from django.forms import inlineformset_factory
from datetime import date
class ReviewForm(forms.ModelForm):

    class Meta:
        model = Review

        fields = [
            'student_name',
            'student_email',
            'course',
            'batch',
            'rating',
            'teaching_quality',
            'communication',
            'practical_knowledge',
            'doubt_solving',
            'feedback',
            'is_anonymous',
        ]

        widgets = {

            'student_name': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Enter your name',
                }
            ),

            'student_email': forms.EmailInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Enter your email',
                }
            ),

            'course': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Enter your course',
                }
            ),

            # ==============================
            # BATCH DROPDOWN
            # ==============================

            'batch': forms.Select(
                choices=[
                    ('', 'Select Batch'),
                    ('Morning', 'Morning'),
                    ('Afternoon', 'Afternoon'),
                    ('Evening', 'Evening'),
                ],
                attrs={
                    "class": "form-select batch-select",
                }
            ),

            'rating': forms.Select(
                choices=[
                    ('', 'Select Rating'),
                    (1, '1 - Poor'),
                    (2, '2 - Fair'),
                    (3, '3 - Good'),
                    (4, '4 - Very Good'),
                    (5, '5 - Excellent'),
                ],
                attrs={
                    'class': 'form-select',
                }
            ),

            'teaching_quality': forms.Select(
                choices=[
                    ('', 'Select Rating'),
                    (1, '1'),
                    (2, '2'),
                    (3, '3'),
                    (4, '4'),
                    (5, '5'),
                ],
                attrs={
                    'class': 'form-select',
                }
            ),

            'communication': forms.Select(
                choices=[
                    ('', 'Select Rating'),
                    (1, '1'),
                    (2, '2'),
                    (3, '3'),
                    (4, '4'),
                    (5, '5'),
                ],
                attrs={
                    'class': 'form-select',
                }
            ),

            'practical_knowledge': forms.Select(
                choices=[
                    ('', 'Select Rating'),
                    (1, '1'),
                    (2, '2'),
                    (3, '3'),
                    (4, '4'),
                    (5, '5'),
                ],
                attrs={
                    'class': 'form-select',
                }
            ),

            'doubt_solving': forms.Select(
                choices=[
                    ('', 'Select Rating'),
                    (1, '1'),
                    (2, '2'),
                    (3, '3'),
                    (4, '4'),
                    (5, '5'),
                ],
                attrs={
                    'class': 'form-select',
                }
            ),

            'feedback': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Write your feedback...',
                    'rows': 5,
                }
            ),

            'is_anonymous': forms.CheckboxInput(
                attrs={
                    'class': 'form-check-input',
                }
            ),
        }
class FacultyProfileForm(forms.ModelForm):
            class Meta:
                model = FacultyProfile

                fields = [
                    "name",
                    "designation",
                    "profile_image",
                    "short_intro",
                    "about",
                    "location",
                    "email",
                    "students_trained",
                    "teaching_approach",
                    "quote",
                ]

                widgets = {
                    "name": forms.TextInput(attrs={
                        "class": "form-control",
                        "placeholder": "Enter your name",
                    }),

                    "designation": forms.TextInput(attrs={
                        "class": "form-control",
                        "placeholder": "Example: AI/ML Educator & Developer",
                    }),

                    "profile_image": forms.ClearableFileInput(attrs={
                        "class": "form-control",
                        "accept": "image/*",
                    }),

                    "short_intro": forms.Textarea(attrs={
                        "class": "form-control",
                        "rows": 3,
                        "placeholder": "Write a short introduction...",
                    }),

                    "about": forms.Textarea(attrs={
                        "class": "form-control",
                        "rows": 5,
                        "placeholder": "Tell students about yourself...",
                    }),

                    "location": forms.TextInput(attrs={
                        "class": "form-control",
                        "placeholder": "Example: Gujarat, India",
                    }),

                    "email": forms.EmailInput(attrs={
                        "class": "form-control",
                        "placeholder": "Enter your email",
                    }),

                    "students_trained": forms.TextInput(attrs={
                        "class": "form-control",
                        "placeholder": "Example: 700+",
                    }),

                    "teaching_approach": forms.TextInput(attrs={
                        "class": "form-control",
                        "placeholder": "Example: Learn → Try → Build → Improve",
                    }),

                    "quote": forms.Textarea(attrs={
                        "class": "form-control",
                        "rows": 3,
                        "placeholder": "Enter your quote...",
                    }),
                }
class FacultyProfileForm(forms.ModelForm):

    class Meta:
        model = FacultyProfile

        fields = [
            "name",
            "designation",
            "profile_image",
            "short_intro",
            "about",
            "location",
            "email",
            "students_trained",
            "teaching_approach",
            "quote",
        ]

        widgets = {
            "name": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Enter your name",
            }),

            "designation": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "AI/ML Educator & Developer",
            }),

            "profile_image": forms.ClearableFileInput(attrs={
                "class": "form-control",
                "accept": "image/*",
            }),

            "short_intro": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 3,
                "placeholder": "Write a short introduction...",
            }),

            "about": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 5,
                "placeholder": "Tell students about yourself...",
            }),

            "location": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Gujarat, India",
            }),

            "email": forms.EmailInput(attrs={
                "class": "form-control",
                "placeholder": "Enter your email",
            }),

            "students_trained": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "700+",
            }),

            "teaching_approach": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Learn → Try → Build → Improve",
            }),

            "quote": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 3,
                "placeholder": "Enter your quote...",
            }),
        }
class EducationForm(forms.ModelForm):

    start_year = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={
                "class": "form-control year-input",
                "placeholder": "Select Year",
                "autocomplete": "off",
                "readonly": "readonly",
            }
        ),
    )

    end_year = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={
                "class": "form-control year-input",
                "placeholder": "Select Year",
                "autocomplete": "off",
                "readonly": "readonly",
            }
        ),
    )

    status = forms.ChoiceField(
        required=False,
        choices=[
            ("", "Select Status"),
            ("Completed", "Completed"),
            ("Pursuing", "Pursuing"),
        ],
        widget=forms.Select(
            attrs={
                "class": "form-control minimal-select",
            }
        ),
    )

    display_order = forms.ChoiceField(
        required=False,
        choices=[
            ("", "Select Order"),
            ("0", "Auto"),
            *[(str(i), str(i)) for i in range(1, 11)],
        ],
        widget=forms.Select(
            attrs={
                "class": "form-control minimal-select",
            }
        ),
    )

    class Meta:
        model = Education

        fields = [
            "degree",
            "field_of_study",
            "institution",
            "status",
            "start_year",
            "end_year",
            "display_order",
        ]

        widgets = {
            "degree": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "B.Tech / M.Tech / Ph.D.",
                }
            ),

            "field_of_study": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "AI & Data Science",
                }
            ),

            "institution": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Institution / University",
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Existing DB years -> show as plain year
        if self.instance and self.instance.pk:

            if self.instance.start_year:
                self.initial["start_year"] = str(
                    self.instance.start_year
                )

            if self.instance.end_year:
                self.initial["end_year"] = str(
                    self.instance.end_year
                )

    def clean_start_year(self):
        value = self.cleaned_data.get("start_year")

        if not value:
            return None

        try:
            return int(value)
        except (ValueError, TypeError):
            raise forms.ValidationError(
                "Please select a valid year."
            )

    def clean_end_year(self):
        value = self.cleaned_data.get("end_year")

        if not value:
            return None

        try:
            return int(value)
        except (ValueError, TypeError):
            raise forms.ValidationError(
                "Please select a valid year."
            )

    def clean_display_order(self):
        value = self.cleaned_data.get("display_order")

        if value in (None, ""):
            return 0

        return int(value)
# =========================================================
# SKILL FORM
# =========================================================

class FacultySkillForm(forms.ModelForm):

    class Meta:

        model = FacultySkill

        fields = [
            "name",
            "display_order",
        ]

        widgets = {

            "name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Python"
                }
            ),

            "display_order": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "1",
                    "min": "0"
                }
            ),
        }


# =========================================================
# EDUCATION FORMSET
# =========================================================

EducationFormSet = inlineformset_factory(
    FacultyProfile,
    Education,
    form=EducationForm,
    extra=0,
    can_delete=True
)


# =========================================================
# SKILL FORMSET
# =========================================================

SkillFormSet = inlineformset_factory(
    FacultyProfile,
    FacultySkill,
    form=FacultySkillForm,
    extra=0,
    can_delete=True
)