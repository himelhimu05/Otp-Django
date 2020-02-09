from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField

from .models import User
class LoginFrom(forms.form):
    phone = forms.IntegerField(label = 'Your Phone Number')
    password = forms.CharField(widget = forms.PasswordInput)


class VerifyForm(forms.form):
    key = forms.IntegerField(label = 'Please enter your OTP here')



class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget = forms.PasswordInput)
    password2 = forms.CharField(label = 'Confirm Password', widget = forms.PasswordInput)

    class Meta:
        model = User
        fields = ('phone',)

        def clean_phone(self):
            phone = self.cleaned_data.get('phone')
            qs = User.objects.filter(phone=phone)
            if qs.exits():
                raise forms.ValidationError("phone is taken")
            return phone

        def clean_password2(self):
            #Check that the two password entries match
            password1 = self.cleaned_data.get("password1")
            password2 = self.cleaned_data.get("password2")
            if password1 and password2 and password1 != password2:
                raise forms.ValidationError("The 2 Password do not match")
            return password2




class TempRegistrationForm(forms.form):
    phone = forms.IntegerField()
    otp   = forms.IntegerField()


class SetPassowrdForm(forms.form):
    password = forms.CharField(label = 'Password', widget= forms.PasswordInput)
    password2 = forms.CharField(label = 'Confirm passwoed', widget = froms.PasswordInput) 



class UserAdminCreationForm(forms.ModelForm):

    password1 = forms.CharField(label = 'Password', widget = forms.PasswordInput)

    class Meta:
        model = User
        fields = ('phone',)

     def clean_password2(self):
            #Check that the two password entries match
            password1 = self.cleaned_data.get("password1")
            password2 = self.cleaned_data.get("password2")
            if password1 and password2 and password1 != password2:
                raise forms.ValidationError("The 2 Password do not match")
            return password2

    def save(self, commit=True):
        #Save the provided password in hashed format
        user = super(UserAdminCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        # user.active = False
        if commit:
            user.save()
        return user

class UserAdminChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the users, but replaces the password field with admin's
    password hash display field
    """

    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ('phone', 'password', 'active', 'admin')

    def clean_password(self):
        #Regardless of what the user provides, return the initial value.
        #This is done here, rather than on the field, because the
        #field does not have access to the initial value
        return self.initial["password"]

