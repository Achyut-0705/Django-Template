from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm,UserChangeForm

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        models=get_user_model()
        fields=('username','first_name', 'last_name','gender','date_of_birth','is_superuser', 'address', 'mobile_no')
        

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        models=get_user_model()
        fields=('first_name', 'last_name','gender','date_of_birth','is_superuser', 'address', 'mobile_no')