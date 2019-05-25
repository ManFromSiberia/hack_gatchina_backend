from rest_framework import serializers

from chat.models import Chat


class ChatDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chat
        fields = ('id', 'social_network', 'city', 'city_district', 'postal_code', 'street', 'house_number',
                  'residential_complex', 'app_chat_identification', 'is_private_house')
