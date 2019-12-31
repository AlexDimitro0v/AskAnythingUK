from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import UserProfile
from PIL import Image


class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField()
    first_name = forms.CharField(required=True, max_length=30)
    last_name = forms.CharField(required=True, max_length=30)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2']


class EditUserForm(forms.ModelForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email']


class EditProfileForm(forms.ModelForm):
    x = forms.FloatField(widget=forms.HiddenInput(), required=False)
    y = forms.FloatField(widget=forms.HiddenInput(), required=False)
    width = forms.FloatField(widget=forms.HiddenInput(), required=False)
    height = forms.FloatField(widget=forms.HiddenInput(), required=False)
    image = forms.ImageField(label='Profile Image', required=False, error_messages={'invalid': "Image files only"}, widget=forms.FileInput)

    class Meta:
        model = UserProfile
        fields = ['city', 'description', 'image', 'x', 'y', 'width', 'height', ]

    def save(self):
        photo = super(EditProfileForm, self).save()
        if (self.cleaned_data.get('x') and self.cleaned_data.get('x') and self.cleaned_data.get('y')
                and self.cleaned_data.get('width') and self.cleaned_data.get('height')):

            x = self.cleaned_data.get('x')
            y = self.cleaned_data.get('y')
            w = self.cleaned_data.get('width')
            h = self.cleaned_data.get('height')

            image = Image.open(photo.image)
            cropped_image = image.crop((x, y, w + x, h + y))
            resized_image = cropped_image.resize((200, 200), Image.ANTIALIAS)
            resized_image.save(photo.image.path)

            return photo
