from rest_framework import serializers
from bot.models import user_history

class userSerializer(serializers.ModelSerializer):
    class Meta:
        model = user_history
        fields = '__all__'