from django import forms

class TwitterCheckerForm(forms.Form):
    twitter_url = forms.CharField(label='Twitter URL', required=True)