# backend/academics/forms.py

from django import forms
from django_flatpickr.widgets import DatePickerInput
from django_flatpickr.schemas import FlatpickrOptions

from .models import SchoolClass, AcademicYear, Term
from teachers.models import Teacher
from academics.models import Subject


# ─── reusable DatePicker widget ─────────────────────────────────────────
_date = DatePickerInput(
    options=FlatpickrOptions(
        altFormat='F j, Y',  # e.g. “ le 31 May, 2025”
        allowInput=True,
        maxDate=None,
    )
)


class SchoolClassForm(forms.ModelForm):
    class Meta:
        model  = SchoolClass
        fields = ["name", "academic_year", "main_teacher", "teachers", "room"]
        widgets = {
            "teachers": forms.CheckboxSelectMultiple,
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["academic_year"].queryset = (
            AcademicYear.objects.order_by("-start_date")
        )


class AcademicYearForm(forms.ModelForm):
    class Meta:
        model  = AcademicYear
        fields = ["name", "start_date", "end_date", "is_current"]
        widgets = {
            "start_date": _date,
            "end_date":   _date,
        }


class TermForm(forms.ModelForm):
    class Meta:
        model  = Term
        fields = ["academic_year", "name", "start_date", "end_date"]
        labels = {
            "academic_year": "Academic year",
            "name":          "Term name",
            "start_date":    "Start date",
            "end_date":      "End date",
        }
        widgets = {
            "start_date": _date,
            "end_date":   _date,
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["academic_year"].queryset = (
            AcademicYear.objects.order_by("-start_date")
        )


class SubjectForm(forms.ModelForm):
    class Meta:
        model  = Subject
        fields = ["code", "name", "school_class", "teacher"]
        labels = {
            "code":         "Code (unique)",
            "name":         "Subject / Course title",
            "school_class": "Class",
            "teacher":      "Teacher in charge",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["school_class"].queryset = (
            SchoolClass.objects.select_related("academic_year")
                        .order_by("academic_year__name", "name")
        )
        self.fields["teacher"].queryset = (
            Teacher.objects.order_by("last_name", "first_name")
        )
