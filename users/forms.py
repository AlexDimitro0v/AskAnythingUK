from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, PasswordResetForm
from .models import UserProfile
from PIL import Image
from django.forms.widgets import DateInput


class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField()
    first_name = forms.CharField(required=True, max_length=30)
    last_name = forms.CharField(required=True, max_length=30)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2']

    def clean_email(self):
        # Get the email
        email = self.cleaned_data.get('email')

        # Check to see if any users already exist with this email.
        try:
            match = User.objects.get(email=email)
        except User.DoesNotExist:
            # Unable to find a user, this is fine
            return email

        # A user was found with this email, raise an error.
        raise forms.ValidationError('This email address is already in use.')


# class EditUserForm(forms.ModelForm):
#
#     class Meta:
#         model = User
#         fields = ['username', 'email']
#
#     def __init__(self, *args, **kwargs):
#         # Disable users to edit the username field
#         super(EditUserForm, self).__init__(*args, **kwargs)
#         self.fields['username'].disabled = True
#         self.fields['email'].disabled = True
#
#     def clean_email(self):
#         # Get the email
#         email = self.cleaned_data.get('email')
#         logged_in_user_username = self.cleaned_data.get('username')
#
#         # Check to see if any users already exist with this email.
#         if User.objects.filter(email=email, is_active=True).exclude(username=logged_in_user_username).exists():
#             # A user was found with this as a username, raise an error.
#             raise forms.ValidationError('This email address is already in use.')
#
#         # Unable to find a user, this is fine - return the email.
#         return email


class EmailValidationOnForgotPassword(PasswordResetForm):
    # Make sure the email is in the database
    def clean_email(self):
        email = self.cleaned_data['email']
        if not User.objects.filter(email__iexact=email, is_active=True).exists():
            raise forms.ValidationError("There is no user registered with the specified E-Mail address.")
        return email


class PrivateInformationForm(forms.ModelForm):

    class Meta:
        model = UserProfile
        fields = ['gender', 'phone_number', 'dob']
        labels = {
            'dob': 'Date of Birth',
        }
        widgets = {
            'dob': DateInput(attrs={'type': 'date'})
        }


class PublicInformationForm(forms.ModelForm):

    class Meta:
        model = UserProfile
        fields = ['city', 'description', 'linkedin', 'url_link_1', 'url_link_2']


class ProfileImageForm(forms.ModelForm):
    x = forms.FloatField(widget=forms.HiddenInput(), required=False)
    y = forms.FloatField(widget=forms.HiddenInput(), required=False)
    width = forms.FloatField(widget=forms.HiddenInput(), required=False)
    height = forms.FloatField(widget=forms.HiddenInput(), required=False)
    image = forms.ImageField(label='Profile Image', required=False, error_messages={'invalid': "Image files only"}, widget=forms.FileInput)

    class Meta:
        model = UserProfile
        fields = ['image', 'x', 'y', 'width', 'height']

    def save(self):
        photo = super(ProfileImageForm, self).save()
        if (self.cleaned_data.get('x') and self.cleaned_data.get('y') and self.cleaned_data.get('width')
                and self.cleaned_data.get('height')):
            x = self.cleaned_data.get('x')
            y = self.cleaned_data.get('y')
            w = self.cleaned_data.get('width')
            h = self.cleaned_data.get('height')

            image = Image.open(photo.image)
            cropped_image = image.crop((x, y, w + x, h + y))
            resized_image = cropped_image.resize((200, 200), Image.ANTIALIAS)
            resized_image.save(photo.image.path)

            return photo
