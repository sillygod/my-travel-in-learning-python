from django import forms


class ContactForm(forms.Form):
    subject = forms.CharField()
    email = forms.EmailField(required=False,
                             label='fucking e-mail ok?')
    message = forms.CharField(widget=forms.Textarea)

    def clean_message(self):
        message = self.cleaned_data['message']
        num_words = (message.split())
        if num_words < 4:
            raise forms.ValidationError("not enough words")
        return message
