from django.core.exceptions import ValidationError
from rest_framework import status
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet 
from rest_framework.response import Response 
from rest_framework import serializers
from rest_framework import status
from levelupapi.models import Game, GameType, Gamer


class Games(ViewSet):

    def create(self, request):
        gamer = Gamer.objects.get(user=request.auth.user)
        game = Game()
        game.title = request.data["title"]
        game.maker = request.data["maker"]
        game.number_of_players = request.data["numberOfPlayers"]
        game.skill_level = request.data["skillLevel"]
        game.gamer = gamer
        gametype = GameType.objects.get(pk=request.data["gameTypeId"])
        game.gametype = gametype

        try:
            game.save()
            serializer = GameSerializer(game, context={'request': request})
            return Response(serializer.data)
        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)


    def retrieve(self, request, pk=None):
        try:
            game = Game.objects.get(pk=pk)
            serializer = GameSerializer(game, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    
    def update(self, request, pk=None):
        gamer = Gamer.objects.get(user=request.auth.user)
        game = Game.objects.get(pk=pk)
        game.title = request.data["title"]
        game.maker = request.data["maker"]
        game.number_of_players = request.data["numberOfPlayers"]
        game.skill_level = request.data["skillLevel"]
        game.gamer = gamer
        gametype = GameType.objects.get(pk=request.data["gameTypeId"])
        game.gametype = gametype
        game.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)


    def destroy(self, request, pk=None):
        try:
            game = Game.objects.get(pk=pk)
            game.delete()
            return Response({}, status=status.HTTP_204_NO_CONTENT)
        except Game.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTPP_500_INTERNAL_SERVER_ERROR)

    
    def list(self, request):
        games = Game.objects.all()

        game_type = self.request.query_params.get('type', None)
        if game_type is not None:
            games = games.filter(gametype__id=game_type)
        
        serializer = GameSerializer(
            games, many=True, context={'request': request})
        return Response(serializer.data)


class GameSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Game
        url = serializers.HyperlinkedIdentityField(
          view_name='game',
          lookup_field='id'
        )
        fields = ('id', 'url', 'title', 'maker', 'number_of_players', 'skill_level', 'gametype')
        depth = 1
