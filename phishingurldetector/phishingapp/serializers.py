from rest_framework import serializers

from phishingapp.models import phishing

class phishingSerializers(serializers.ModelSerializer):
    class Meta:
        model = phishing
        fields = "__all__"