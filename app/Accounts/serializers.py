# # import imp
# # import os
# # from django.db import transaction
# from rest_framework import serializers
# from dj_rest_auth.registration.serializers import RegisterSerializer
# from allauth.account.adapter import get_adapter
# # from allauth.account.utils import setup_user_email
# from dj_rest_auth.serializers import UserDetailsSerializer
# from django.contrib.auth import get_user_model
# from django.contrib.sites.models import Site
# from django.contrib.sites.shortcuts import get_current_site
# from django.urls import reverse
# from urllib.parse import urlsplit
# from django.utils.encoding import escape_uri_path, iri_to_uri
# from django.contrib.auth.forms import SetPasswordForm, PasswordResetForm
# from dj_rest_auth.serializers import PasswordResetSerializer as _PasswordResetSerializer
# from django.conf import settings
# from django.core.exceptions import ValidationError as DjangoValidationError
# from dj_rest_auth.models import TokenModel
# from dj_rest_auth.utils import import_callable
# from dj_rest_auth.serializers import UserDetailsSerializer as DefaultUserDetailsSerializer
# from .encryption import encrypt
# from Accounts.models import CustomUser


# if 'allauth' in settings.INSTALLED_APPS:
#     from allauth.account import app_settings
#     from allauth.account.adapter import get_adapter
#     from allauth.account.forms import \
#         ResetPasswordForm as DefaultPasswordResetForm
#     from allauth.account.forms import default_token_generator
#     from allauth.account.utils import (filter_users_by_email,
#                                        user_pk_to_url_str, user_username)



# class CustomRegisterSerializer(RegisterSerializer):
#     first_name = serializers.CharField()
#     last_name = serializers.CharField()
#     gender = serializers.CharField()
#     date_of_birth = serializers.DateField()
#     address = serializers.CharField()
#     mobile_no = serializers.CharField()
#     role = serializers.CharField()
#     email=None

#     def get_cleaned_data(self):
#         super(CustomRegisterSerializer, self).get_cleaned_data()
#         return {
#             'password1': self.validated_data.get('password1', ''),
#             'password2': self.validated_data.get('password2', ''),
#             'address': self.validated_data.get('address', ''),
#             'mobile_no': self.validated_data.get('mobile_no', ''),
#             'username': self.validated_data.get('username', ''),
#             'first_name': self.validated_data.get('first_name', ''),
#             'last_name': self.validated_data.get('last_name', ''),
#             'date_of_birth': self.validated_data.get('date_of_birth', ''),
#             'role': self.validated_data.get('role', ''),
#             'gender': self.validated_data.get('gender', ''),
#         }

#     def save(self, request):
#         adapter = get_adapter()
#         user = adapter.new_user(request)
#         self.cleaned_data = self.get_cleaned_data()
#         user = adapter.save_user(request, user, self, commit=False)
#         user.date_of_birth=self.data.get('date_of_birth')
#         user.address=self.data.get('address')
#         user.mobile_no=self.data.get('mobile_no')
#         user.role=self.data.get('role')
#         user.gender=self.data.get('gender')
        
#         try:
#             adapter.clean_password(self.cleaned_data['password1'], user=user)
#         except DjangoValidationError as exc:
#             raise serializers.ValidationError(
#                 detail=serializers.as_serializer_error(exc)
#             )
            
#         user.save()
#         userd=request.data.get('userdetails')
#         if userd:
#             UserInfo(user=user,os=userd.get('os'),browser=userd.get('browser'),ip=userd.get('ip')).save()
#         self.custom_signup(request, user)
#         # setup_user_email(request, user, [])
#         return user

# class UserSerializer(UserDetailsSerializer):
#     pk = serializers.SerializerMethodField()

#     class Meta(UserDetailsSerializer.Meta):
#         model=get_user_model()
#         fields = ('gender', 'first_name', 'last_name','date_of_birth','pk', 'address', 'mobile_no', 'status', 'role')


#     def get_pk(self, instance):
#         return encrypt(instance.id)

#     def update(self, instance, validated_data):
#         # userprofile_serializer = self.fields['profile']
#         # userprofile_instance = instance.userprofile
#         # userprofile_data = validated_data.pop('userprofile', {})

#         # # to access the 'company_name' field in here
#         # # company_name = userprofile_data.get('company_name')

#         # # update the userprofile fields
#         # userprofile_serializer.update(userprofile_instance, userprofile_data)

#         instance = super().update(instance, validated_data)
#         return instance

# class UpdateUserSerializer(UserDetailsSerializer):
#     class Meta(UserDetailsSerializer.Meta):
#         model=get_user_model()
#         fields = ('gender','date_of_birth','pk', 'address', 'mobile_no', 'first_name', 'last_name', 'status')


# class CustomTokenSerializer(serializers.ModelSerializer):
#     user = UserDetailsSerializer(read_only=True)

#     class Meta:
#         model = TokenModel
#         fields = ('key', 'user', )


# class AdminDashboardSerializer(serializers.ModelSerializer):
#     approved_users = serializers.SerializerMethodField()
#     pending_users = serializers.SerializerMethodField()

#     class Meta:
#         model = CustomUser
#         fields = ('approved_users', 'pending_users')

#     def get_approved_users(self, instance):
#         queryset = CustomUser.objects.filter(role="Staff", status="Approved", approved_by=instance)
#         return UserSerializer(queryset, many=True).data

#     def get_pending_users(self, instance):
#         queryset = CustomUser.objects.filter(role="Staff", status="Pending")
#         return UserSerializer(queryset, many=True).data


# class SuperAdminDashboardSerializer(serializers.ModelSerializer):
#     approved_officers = serializers.SerializerMethodField()
#     pending_officers = serializers.SerializerMethodField()
#     approved_admins = serializers.SerializerMethodField()
#     pending_admins = serializers.SerializerMethodField()

#     class Meta:
#         model = CustomUser
#         fields = ('approved_officers', 'pending_officers', 'approved_admins', 'pending_admins')

#     def get_approved_officers(self, instance):
#         queryset = CustomUser.objects.filter(role="Staff", status="Approved", approved_by=instance)
#         return UserSerializer(queryset, many=True).data

#     def get_pending_officers(self, instance):
#         queryset = CustomUser.objects.filter(role="Staff", status="Pending")
#         return UserSerializer(queryset, many=True).data

#     def get_approved_admins(self, instance):
#         queryset = CustomUser.objects.filter(role="Admin", status="Approved", approved_by=instance)
#         return UserSerializer(queryset, many=True).data

#     def get_pending_admins(self, instance):
#         queryset = CustomUser.objects.filter(role="Admin", status="Pending")
#         return UserSerializer(queryset, many=True).data


# import imp
# import os
# from django.db import transaction
from email.mime import image
from rest_framework import serializers
from dj_rest_auth.registration.serializers import RegisterSerializer
from allauth.account.adapter import get_adapter
# from allauth.account.utils import setup_user_email
from dj_rest_auth.serializers import UserDetailsSerializer
from django.contrib.auth import get_user_model
from django.contrib.sites.models import Site
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from urllib.parse import urlsplit
from django.utils.encoding import escape_uri_path, iri_to_uri
from django.contrib.auth.forms import SetPasswordForm, PasswordResetForm
from dj_rest_auth.serializers import PasswordResetSerializer as _PasswordResetSerializer
from django.conf import settings
from django.core.exceptions import ValidationError as DjangoValidationError
from dj_rest_auth.models import TokenModel
from dj_rest_auth.utils import import_callable
from dj_rest_auth.serializers import UserDetailsSerializer as DefaultUserDetailsSerializer
import urllib
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank
from Accounts.models import ProfileImage
from .encryption import encrypt
from Accounts.models import CustomUser


if 'allauth' in settings.INSTALLED_APPS:
    from allauth.account import app_settings
    from allauth.account.adapter import get_adapter
    from allauth.account.forms import \
        ResetPasswordForm as DefaultPasswordResetForm
    from allauth.account.forms import default_token_generator
    from allauth.account.utils import (filter_users_by_email,
                                       user_pk_to_url_str, user_username)



class CustomRegisterSerializer(RegisterSerializer):
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    gender = serializers.CharField()
    date_of_birth = serializers.DateField()
    address = serializers.CharField()
    designation = serializers.CharField()
    file = serializers.ImageField()
    mobile_no = serializers.CharField()
    role = serializers.CharField()
    email=None

    def get_cleaned_data(self):
        super(CustomRegisterSerializer, self).get_cleaned_data()
        return {
            'password1': self.validated_data.get('password1', ''),
            'password2': self.validated_data.get('password2', ''),
            'address': self.validated_data.get('address', ''),
            'mobile_no': self.validated_data.get('mobile_no', ''),
            'username': self.validated_data.get('username', ''),
            'first_name': self.validated_data.get('first_name', ''),
            'last_name': self.validated_data.get('last_name', ''),
            'date_of_birth': self.validated_data.get('date_of_birth', ''),
            'role': self.validated_data.get('role', ''),
            'file': self.validated_data.get('file', None),
            'gender': self.validated_data.get('gender', ''),
            'designation': self.validated_data.get('designation', ''),
        }

    def save(self, request):
        adapter = get_adapter()
        user = adapter.new_user(request)
        self.cleaned_data = self.get_cleaned_data()
        user = adapter.save_user(request, user, self, commit=False)
        user.date_of_birth=self.data.get('date_of_birth')
        user.address=self.data.get('address')
        user.mobile_no=self.data.get('mobile_no')
        user.role=self.data.get('role')
        user.gender=self.data.get('gender')
        user.designation=self.data.get('designation')
        
        try:
            adapter.clean_password(self.cleaned_data['password1'], user=user)
        except DjangoValidationError as exc:
            raise serializers.ValidationError(
                detail=serializers.as_serializer_error(exc)
            )
            
        user.save()
        if request.data.get("file"):
            ProfileImage.objects.create(user=user, file=request.data.get("file"))
        userd=request.data.get('userdetails')
        # if userd:
            # UserInfo(user=user,os=userd.get('os'),browser=userd.get('browser'),ip=userd.get('ip')).save()
        self.custom_signup(request, user)
        # setup_user_email(request, user, [])
        return user

class UserSerializer(UserDetailsSerializer):
    pk = serializers.SerializerMethodField()
    profile_image = serializers.SerializerMethodField()

    class Meta(UserDetailsSerializer.Meta):
        model=get_user_model()
        fields = ('gender', 'first_name', 'last_name','date_of_birth','pk', 'address', 'mobile_no', 'status', 'role', 'approved_by', 'designation', 'profile_image')
        read_only_fields = ('profile_image',)


    def get_pk(self, instance):
        return encrypt(instance.id)
    
    def get_profile_image(self, instance):
        images = ProfileImage.objects.filter(user=instance)
        if images.exists():
            image = images[0]
            return {"path": image.file.url, "id": image.id}
        return None


    def update(self, instance, validated_data):
        # userprofile_serializer = self.fields['profile']
        # userprofile_instance = instance.userprofile
        # userprofile_data = validated_data.pop('userprofile', {})

        # # to access the 'company_name' field in here
        # # company_name = userprofile_data.get('company_name')

        # # update the userprofile fields
        # userprofile_serializer.update(userprofile_instance, userprofile_data)

        instance = super().update(instance, validated_data)
        return instance

class UpdateUserSerializer(UserDetailsSerializer):
    class Meta(UserDetailsSerializer.Meta):
        model=get_user_model()
        fields = ('gender','date_of_birth','pk', 'address', 'mobile_no', 'first_name', 'last_name', 'status')


class CustomTokenSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = TokenModel
        fields = ('key', 'user', )


class AdminDashboardSerializer(serializers.ModelSerializer):
    approved_users = serializers.SerializerMethodField()
    pending_users = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = ('approved_users', 'pending_users')

    def get_approved_users(self, instance):
        queryset = CustomUser.objects.filter(role="Staff", status="Approved")
        if 'query' in self.context:
            queryset = queryset.annotate(rank=SearchRank(
            self.context['vector'], self.context['query'])).distinct().filter(rank__gte=0.1).order_by('-rank')
        return UserSerializer(queryset, many=True).data

    def get_pending_users(self, instance):
        queryset = CustomUser.objects.filter(role="Staff", status="Pending")
        if 'query' in self.context:
            queryset = queryset.annotate(rank=SearchRank(
            self.context['vector'], self.context['query'])).distinct().filter(rank__gte=0.1).order_by('-rank')
        return UserSerializer(queryset, many=True).data


class SuperAdminDashboardSerializer(serializers.ModelSerializer):
    approved_officers = serializers.SerializerMethodField()
    pending_officers = serializers.SerializerMethodField()
    approved_admins = serializers.SerializerMethodField()
    pending_admins = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = ('approved_officers', 'pending_officers', 'approved_admins', 'pending_admins')

    def get_approved_officers(self, instance):
        queryset = CustomUser.objects.filter(role="Staff", status="Approved")
        if 'query' in self.context:
            queryset = queryset.annotate(rank=SearchRank(
            self.context['vector'], self.context['query'])).distinct().filter(rank__gte=0.1).order_by('-rank')
        return UserSerializer(queryset, many=True).data

    def get_pending_officers(self, instance):
        queryset = CustomUser.objects.filter(role="Staff", status="Pending")
        if 'query' in self.context:
            queryset = queryset.annotate(rank=SearchRank(
            self.context['vector'], self.context['query'])).distinct().filter(rank__gte=0.1).order_by('-rank')
        return UserSerializer(queryset, many=True).data

    def get_approved_admins(self, instance):
        queryset = CustomUser.objects.filter(role="Admin", status="Approved")
        if 'query' in self.context:
            queryset = queryset.annotate(rank=SearchRank(
            self.context['vector'], self.context['query'])).distinct().filter(rank__gte=0.1).order_by('-rank')
        return UserSerializer(queryset, many=True).data

    def get_pending_admins(self, instance):
        queryset = CustomUser.objects.filter(role="Admin", status="Pending")
        if 'query' in self.context:
            queryset = queryset.annotate(rank=SearchRank(
            self.context['vector'], self.context['query'])).distinct().filter(rank__gte=0.1).order_by('-rank')
        return UserSerializer(queryset, many=True).data


class MyFileSerializer(serializers.ModelSerializer):
    class Meta():
        model = ProfileImage
        fields = ('file', 'user', 'uploaded_at')

    def create(self, validated_data):
        # validated_data['user'] = self.context.get('user')
        # profile_image = ProfileImage.objects.create(file=validated_data['file'],userProfile=validated_data['user'])
        profile_image = ProfileImage.objects.create(**validated_data)
        return profile_image

    def update(self, instance, data):
        instance.image = data['file']
        instance.save()
        return instance

class GetImagelSerializer(serializers.ModelSerializer):
       
    class Meta:
        model = ProfileImage
        fields = '__all__'