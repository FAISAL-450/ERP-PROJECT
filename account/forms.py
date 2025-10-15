from django import forms
from .models import Account

class AccountForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = [
            'name',
            'code',
            'type',
            'description',
            'is_active',
            'currency',
            'cost_center',
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
            'cost_center': forms.TextInput(attrs={'placeholder': 'e.g. Marketing, IT'}),
        }
