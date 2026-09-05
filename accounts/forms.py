from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from .models import StudentProfile


class StudentRegisterForm(forms.Form):
    first_name = forms.CharField(max_length=150)
    last_name = forms.CharField(max_length=150)
    email = forms.EmailField()
    branch = forms.ChoiceField(choices=StudentProfile.BRANCH_CHOICES)
    year = forms.ChoiceField(choices=StudentProfile.YEAR_CHOICES)
    password1 = forms.CharField(label="Password", min_length=6, widget=forms.PasswordInput)
    password2 = forms.CharField(label="Confirm password", widget=forms.PasswordInput)

    def clean_email(self):
        email = self.cleaned_data["email"].lower()
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("An account with this email already exists.")
        return email

    def clean(self):
        cleaned = super().clean()
        if cleaned.get("password1") and cleaned.get("password2") and cleaned["password1"] != cleaned["password2"]:
            self.add_error("password2", "Passwords do not match.")
        return cleaned

    def _unique_username(self):
        base = self.cleaned_data["email"].split("@", 1)[0]
        base = "".join(character for character in base if character.isalnum() or character in "._-")[:120] or "student"
        candidate, suffix = base, 1
        while User.objects.filter(username=candidate).exists():
            suffix += 1
            candidate = f"{base[:145 - len(str(suffix))]}-{suffix}"
        return candidate

    def save(self, commit=True):
        user = User(
            username=self._unique_username(), email=self.cleaned_data["email"],
            first_name=self.cleaned_data["first_name"], last_name=self.cleaned_data["last_name"],
        )
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
            profile = user.profile
            profile.branch = self.cleaned_data["branch"]
            profile.year = self.cleaned_data["year"]
            profile.save()
        return user


class ProfileForm(forms.ModelForm):
    class Meta:
        model = StudentProfile
        fields = ("branch", "year")


class EmailAuthenticationForm(AuthenticationForm):
    username = forms.EmailField(label="Email address", widget=forms.EmailInput(attrs={"autocomplete": "email"}))
