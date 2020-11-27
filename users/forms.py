from django import forms 


class name_users(forms.Form):
    username = forms.CharField(max_length=20, label='Username')
    password = forms.CharField(label='Password', widget=forms.PasswordInput)

class new_user(forms.Form):
    username = forms.CharField(max_length=15, label='Username')
    f_name = forms.CharField(max_length=15, label='First Name')
    l_name = forms.CharField(label='Last Name', max_length=15)
    email = forms.EmailField(label='Email')
    password =forms.CharField(label='Password', widget=forms.PasswordInput)
    conf_password =forms.CharField(label='Confirm Password', widget=forms.PasswordInput)
