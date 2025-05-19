from django import forms

class TwitterCheckerForm(forms.Form):
    twitter_url = forms.URLField(
        label="Twitter URL",
        widget=forms.URLInput(attrs={
            'placeholder': 'https://x.com/example',
            'class': 'w-full border border-gray-300 rounded-lg px-4 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500'
        })
    )
