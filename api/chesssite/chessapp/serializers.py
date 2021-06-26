from rest_framework import serializers
from chessapp.models import Game
from django.contrib.auth.models import User


class GameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        owner = serializers.ReadOnlyField(source='owner.username')
        fields = [
            "id",
            "title",
            "description",
            "move_list",
            "white",
            "white_level",
            "black",
            "black_level",
            "time_controls",
            "results",
            "fen",
            'owner',
        ]

    def create(self, validated_data):
        """
        Create and return a new `Game` instance, given the validated data.
        """
        return Game.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update and return an existing `Game` instance, given the validated data.
        """
        instance.title = validated_data.get("title", instance.title)
        instance.description = validated_data.get("description", instance.description)
        instance.move_list = validated_data.get("move_list", instance.move_list)
        instance.white = validated_data.get("white", instance.white)
        instance.white_level = validated_data.get("white_level", instance.white_level)
        instance.black = validated_data.get("black", instance.black)
        instance.black_level = validated_data.get("black_level", instance.black_level)
        instance.time_controls = validated_data.get(
            "time_controls", instance.time_controls
        )
        instance.results = validated_data.get("results", instance.results)
        instance.fen = validated_data.get("fen", instance.fen)
        instance.save()
        return instance

class UserSerializer(serializers.ModelSerializer):
    games = serializers.PrimaryKeyRelatedField(many=True, queryset=Game.objects.all())


    class Meta:
        model = User
        fields = ['id', 'username', 'games']