# -*- coding: utf-8 -*-

# This file is part of wger Workout Manager.
#
# wger Workout Manager is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# wger Workout Manager is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with Workout Manager.  If not, see <http://www.gnu.org/licenses/>.

from rest_framework import serializers
import re
from django.contrib.auth.models import User
from django.utils import translation
from wger.config.models import GymConfig
from rest_framework.authtoken.models import Token
from django.shortcuts import get_object_or_404
from wger.core.models import (
    UserProfile,
    Language,
    DaysOfWeek,
    License,
    RepetitionUnit,
    WeightUnit,
    UserModel
)
from wger.gym.models import GymUserConfig


class UserApiSerializer(serializers.ModelSerializer):
    """ Serializer to map to User model in relation to api user"""
    api_key = serializers.CharField(required=True)
    username = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True, min_length=8, write_only=True)

    class Meta:
        model = User
        read_only_fields = ['api_key']
        fields = ['api_key', 'username', 'password', 'email']

    def validate(self, data):
        check_email = User.objects.filter(email=data['email'])
        check_username = User.objects.filter(email=data['username'])
        if check_email.exists():
            raise serializers.ValidationError("Email already in use.")
        elif check_username.exists():
            raise serializers.ValidationError("username already is already taken.")
        elif not re.match(r"^[a-zA-Z0-9_.-]+$", data['username']):
            raise serializers.ValidationError('Username can have a number but not at start')
        elif not re.search(r"^(\w+\d+|\d+\w+)+$", data['password']):
            raise serializers.ValidationError(
                'Password should be a combination of Alphabets and Numbers')
        return dict(data)

    def create(self, validated_data):
        key_id = get_object_or_404(Token, key=validated_data['api_key'])
        allow_user = UserProfile.objects.filter(user_id=key_id.user_id, is_allowed=True).exists()
        if not allow_user:
            raise serializers.ValidationError("You're not allowed to create other users")
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'])
        user.save()
        # Pre-set some values of the user's profile
        language = Language.objects.get(short_name=translation.get_language())
        user.userprofile.notification_language = language
        # Set default gym, if needed
        gym_config = GymConfig.objects.get(pk=1)
        if gym_config.default_gym:
            user.userprofile.gym = gym_config.default_gym
            # Create gym user configuration object
            config = GymUserConfig()
            config.gym = gym_config.default_gym
            config.user = user
            config.save()
        user.userprofile.save()
        creator = User.objects.get(pk=key_id.user_id)
        new_user = UserModel.objects.create(api_user=user, created_by=creator)
        new_user.save()
        return new_user


class UserprofileSerializer(serializers.ModelSerializer):
    '''
    Workout session serializer
    '''
    class Meta:
        model = UserProfile


class UsernameSerializer(serializers.Serializer):
    '''
    Serializer to extract the username
    '''
    username = serializers.CharField()


class LanguageSerializer(serializers.ModelSerializer):
    '''
    Language serializer
    '''
    class Meta:
        model = Language


class DaysOfWeekSerializer(serializers.ModelSerializer):
    '''
    DaysOfWeek serializer
    '''
    class Meta:
        model = DaysOfWeek


class LicenseSerializer(serializers.ModelSerializer):
    '''
    License serializer
    '''
    class Meta:
        model = License


class RepetitionUnitSerializer(serializers.ModelSerializer):
    '''
    Repetition unit serializer
    '''
    class Meta:
        model = RepetitionUnit


class WeightUnitSerializer(serializers.ModelSerializer):
    '''
    Weight unit serializer
    '''
    class Meta:
        model = WeightUnit
