# backend/students/forms.py
from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import gettext_lazy as _
from django_flatpickr.widgets import DatePickerInput
from django_flatpickr.schemas import FlatpickrOptions
from .models import Student
from academics.models import SchoolClass    

# ──────────────────────────────────────────────────────────
# Shared date-picker widget
# ──────────────────────────────────────────────────────────
date_widget = DatePickerInput(
    options=FlatpickrOptions(
        altFormat='j F, Y',    # human-readable
        allowInput=True,
        maxDate='today',
    )
)

# ──────────────────────────────────────────────────────────
# Main student form
# ──────────────────────────────────────────────────────────
class StudentForm(forms.ModelForm):
    class Meta:
        model  = Student
        fields = [
            "student_id", "first_name", "last_name", "gender",
            "date_of_birth", "nationality", "address", "phone",
            "email", "guardian_name", "guardian_phone",
            "school_class",            # ← FK replaces old class_level
            "enrol_date", "status", "photo",
        ]
        widgets = {
            "date_of_birth": date_widget,
            "enrol_date":    date_widget,
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["school_class"].queryset = SchoolClass.objects.order_by("name")
# ──────────────────────────────────────────────────────────
# Custom login error messages
# ──────────────────────────────────────────────────────────
class CustomAuthForm(AuthenticationForm):
    error_messages = {
        "invalid_login": _(
            "Oups ! Les informations d'identification ne correspondent pas à nos données. "
            "Veuillez vérifier et réessayer."
        ),
        "inactive": _("Ce compte est inactif."),
    }

def clean_photo(self):
    photo = self.cleaned_data.get("photo")
    if photo and photo.size > 2 * 1024 * 1024:
        raise forms.ValidationError("Photo must be 2MB or smaller.")
    return photo
