from rest_framework import serializers

from content.models import PublicationModel, PublicationContentModel, PublicationTagModel, PublicationCommentModel


class PublicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = PublicationModel
        fields = '__all__'

class PublicationContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = PublicationContentModel
        fields = '__all__'


class PublicationTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = PublicationTagModel
        fields = '__all__'

class PublicationCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = PublicationCommentModel
        fields = '__all__'
