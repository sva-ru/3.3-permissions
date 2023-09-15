from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from advertisements.models import Advertisement


class UserSerializer(serializers.ModelSerializer):
    """Serializer для пользователя."""

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name',
                  'last_name',)

class AdvertisementSerializer(serializers.ModelSerializer):
    creator = UserSerializer(
        read_only=True)
    class Meta:
        model = Advertisement
        fields = ('id', 'title', 'description',
                  'status', 'created_at', 'creator')

    def create(self, validated_data):
        validated_data["creator"] = self.context["request"].user
        print(validated_data["creator"])
        return super().create(validated_data)

    def validate(self, data):
        advertisemen_count = Advertisement.objects.filter(creator=self.context["request"].user,
                                                           status='OPEN').count()
        status = self.initial_data.get('status')
        if advertisemen_count >= 10 and status != 'CLOSED':
            raise ValidationError(['No more than 10 active ads are allowed'])
        return data
