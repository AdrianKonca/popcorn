from django import forms
from django.utils.translation import gettext_lazy as _
from django_registration.forms import RegistrationForm
from django_summernote.widgets import SummernoteWidget
from django.contrib.auth.forms import AuthenticationForm
from .models import Recipe, User, Comment, Category


class CategoriesModelChoiceIterator(forms.models.ModelChoiceIterator):
    def __iter__(self):
        group = ""
        subgroup = []
        for category in self.queryset:
            if not group:
                group = category.get_tag_display()

            if group != category.get_tag_display():
                yield (group, subgroup)
                group = category.get_tag_display()
                subgroup = [(category.id, category.name)]
            else:
                subgroup.append((category.id, category.name))
        yield (group, subgroup)


class CategoriesField(forms.ModelMultipleChoiceField):
    iterator = CategoriesModelChoiceIterator


class CheckboxSelectMultipleCustom(forms.CheckboxSelectMultiple):
    template_name = 'popcorn/multiple_input.html'
    option_template_name = 'popcorn/input_option.html'


class RecipeForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(RecipeForm, self).__init__(*args, **kwargs)

        self.fields['categories'].label = 'Kategorie'

        if self.instance:
            self.fields['categories'].initial = None

    categories = CategoriesField(queryset=Category.objects.all(),
                                 widget=forms.CheckboxSelectMultiple(attrs={'class': 'my-class'}))

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
    def __init__(self, *args, **kwargs):
        super(UserRegistrationForm, self).__init__(*args, **kwargs)

    class Meta(RegistrationForm.Meta):
        model = User
        fields = [
            User.USERNAME_FIELD,
            User.get_email_field_name(),
            "password1",
            "password2",
        ]


class LoginForm(AuthenticationForm):
    remember_me = forms.BooleanField(label=_("Remember me"), required=False)  # and add the remember_me field
    class Meta():
        pass
        labels = {'username': _("Username")}


class EmailChangeForm(forms.Form):
    """
    A form that lets a user change set their email while checking for a change in the
    e-mail.
    """
    error_messages = {
        'password_incorrect': _("Your old password was entered incorrectly. Please enter it again."),
        'email_mismatch': _("The two email addresses fields didn't match."),
        'not_changed': _("The email address is the same as the one already defined."),
    }

    old_password = forms.CharField(
        label=_("Old password"),
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'current-password', 'autofocus': True}),
    )

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

    def clean_old_password(self):
        """
        Validate that the old_password field is correct.
        """
        old_password = self.cleaned_data["old_password"]
        if not self.user.check_password(old_password):
            raise forms.ValidationError(
                self.error_messages['password_incorrect'],
                code='password_incorrect',
            )
        return old_password

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
