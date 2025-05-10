from django import forms
from .models import Item, ExchangeProposal, UserProfile

class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['title', 'description', 'category', 'condition', 'image']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }

class ExchangeProposalForm(forms.ModelForm):
    class Meta:
        model = ExchangeProposal
        fields = ['offered_item', 'message']
        widgets = {
            'message': forms.Textarea(attrs={'rows': 4}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['offered_item'].queryset = Item.objects.filter(
                owner=user,
                is_active=True
            )

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['phone', 'address', 'avatar', 'bio']
        widgets = {
            'address': forms.Textarea(attrs={'rows': 3}),
            'bio': forms.Textarea(attrs={'rows': 3}),
        } 