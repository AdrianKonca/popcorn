from django import forms
from django_registration.forms import RegistrationForm
from django_summernote.widgets import SummernoteWidget

from .models import Recipe, User, Comment


# Adding css to django class
# https://stackoverflow.com/questions/5827590/css-styling-in-django-forms
# https://docs.djangoproject.com/en/2.2/topics/forms/#working-with-form-templates
# https://www.youtube.com/watch?v=6-XXvUENY_8

# https://stackoverflow.com/questions/3737116/how-to-add-optgroups-to-a-django-modelmultiplechoicefield

class RecipeForm(forms.ModelForm):
    # name = forms.CharField()
    # difficulty = forms.ChoiceField()
    # recipe = SummernoteTextFormField()

    class Meta:
        model = Recipe
        fields = [
            'name',
            'difficulty',
            'preparation_time',
            'servings_count',
            'categories',
            'icon',
            'content',
        ]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'difficulty': forms.Select(attrs={'class': 'form-control'}),
            'preparation_time': forms.NumberInput(attrs={'class': 'form-control'}),
            'servings_count': forms.NumberInput(attrs={'class': 'form-control'}),
            'categories': forms.CheckboxSelectMultiple(choices=["blablabla"]),
            # 'icon': forms.ImageField(),
            'content': SummernoteWidget({
                'summernote': {
                    'width': '100%',
                    'height': '2000',
                },
            }),
        }
        labels = {
            'name': 'Nazwa przepisu',
            'difficulty': 'Trudność',
            'preparation_time': 'Czas przygotowania (w minutach)',
            'servings_count': 'Ilość porcji',
            'categories': 'Kategorie',
            'icon': 'Miniaturka',
            'content': '',
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {'content': SummernoteWidget({
            'summernote': {
                'toolbar': [
                    ['style', ['style', ]],
                    ['font', ['bold', 'italic', 'underline', 'color', ]],
                    ['paragraph', ['paragraph', 'ol', 'ul', ]],
                    ['misc', ['undo', 'redo']],
                ],
                'width': '100%',
                'height': '400',
            },
        })}
        labels = {'content': ''}


class UserRegistrationForm(RegistrationForm):
    class Meta(RegistrationForm.Meta):
        model = User


class EmailChangeForm(forms.Form):
    """
    A form that lets a user change set their email while checking for a change in the
    e-mail.
    """
    error_messages = {
        'email_mismatch': _("The two email addresses fields didn't match."),
        'not_changed': _("The email address is the same as the one already defined."),
    }

    new_email1 = forms.EmailField(
        label=_("New email address"),
        widget=forms.EmailInput,
    )

    new_email2 = forms.EmailField(
        label=_("New email address confirmation"),
        widget=forms.EmailInput,
    )

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(EmailChangeForm, self).__init__(*args, **kwargs)

    def clean_new_email1(self):
        old_email = self.user.email
        new_email1 = self.cleaned_data.get('new_email1')
        if new_email1 and old_email:
            if new_email1 == old_email:
                raise forms.ValidationError(
                    self.error_messages['not_changed'],
                    code='not_changed',
                )
        return new_email1

    def clean_new_email2(self):
        new_email1 = self.cleaned_data.get('new_email1')
        new_email2 = self.cleaned_data.get('new_email2')
        if new_email1 and new_email2:
            if new_email1 != new_email2:
                raise forms.ValidationError(
                    self.error_messages['email_mismatch'],
                    code='email_mismatch',
                )
        return new_email2

    def save(self, commit=True):
        email = self.cleaned_data["new_email1"]
        self.user.email = email
        if commit:
            self.user.save()
        return self.user
