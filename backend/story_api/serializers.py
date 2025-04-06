from rest_framework import serializers

class IdeaInputSerializer(serializers.Serializer):
    idea = serializers.CharField()

class EpisodeInputSerializer(serializers.Serializer):
    title = serializers.CharField()
    plot = serializers.CharField()

class ThumbnailPromptSerializer(serializers.Serializer):
    title = serializers.CharField()
    plot = serializers.CharField()

class FinalImageInputSerializer(serializers.Serializer):
    prompt_index = serializers.IntegerField()

class AudioInputSerializer(serializers.Serializer):
    script = serializers.CharField()
