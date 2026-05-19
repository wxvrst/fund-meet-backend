from rest_framework import serializers

from content.models import PublicationModel, PublicationContentModel, PublicationTagModel, PublicationCommentModel


class PublicationSerializer(serializers.ModelSerializer):
    tags = serializers.SlugRelatedField(
        many=True,
        slug_field="name",
        queryset=PublicationTagModel.objects.all(),
        allow_null=True,
        allow_empty=True,
        required=False,
    )

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
