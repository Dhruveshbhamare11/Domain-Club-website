from decimal import Decimal, InvalidOperation
from django import forms


class SubmissionForm(forms.Form):
    answer = forms.CharField(max_length=100, label="Your numerical answer")

    def clean_answer(self):
        value = self.cleaned_data["answer"].strip()
        try:
            Decimal(value)
        except InvalidOperation:
            raise forms.ValidationError("Enter a valid integer or decimal answer.")
        return value
