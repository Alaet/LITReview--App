from django import forms
from flux import models


class ReviewForm(forms.ModelForm):
    STARS = [
        # Value | Readable stuff
        ('0', '0 ⭐'),
        ('1', '1 ⭐'),
        ('2', '2 ⭐'),
        ('3', '3 ⭐'),
        ('4', '4 ⭐'),
        ('5', '5 ⭐'),
    ]
    edit_review = forms.BooleanField(widget=forms.HiddenInput, initial=True)
    note = forms.ChoiceField(widget=forms.RadioSelect, choices=STARS)

    class Meta:
        model = models.Review
        fields = ['accroche', 'note', 'critique']


class DeleteReviewForm(forms.Form):
    delete_review = forms.BooleanField(widget=forms.HiddenInput, initial=True)


class TicketForm(forms.ModelForm):
    edit_ticket = forms.BooleanField(widget=forms.HiddenInput, initial=True)

    class Meta:
        model = models.Ticket
        fields = ['titre', 'description', 'image']


class DeleteTicketForm(forms.Form):
    delete_ticket = forms.BooleanField(widget=forms.HiddenInput, initial=True)


class UserFollowsForm(forms.Form):
    username_follow = forms.CharField(
        label="", max_length=60, widget=forms.TextInput(attrs={"size": "60"})
    )
