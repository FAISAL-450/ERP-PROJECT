from django import forms
from .models import Contractor

class ContractorForm(forms.ModelForm):
    class Meta:
        model = Contractor
        fields = ['project_name', 'contractor_name', 'contractor_phone', 'contractor_address']
        labels = {
            'project_name': 'Project Name',
            'contractor_name': 'Contractor Name',
            'contractor_phone': 'Contractor Phone',
            'contractor_address': 'Contractor Address',
        }
        widgets = {
            'project_name': forms.Select(attrs={'class': 'form-control'}),
            'contractor_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter contractor name'}),
            'contractor_phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter phone number'}),
            'contractor_address': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter address', 'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Ensure blank option appears at top of dropdown
        self.fields['project_name'].empty_label = "--------- Select Project ---------"
