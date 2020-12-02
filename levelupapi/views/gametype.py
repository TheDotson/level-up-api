from django.http import HttpResponse
from rest_framework.viewsets import ViewSet 
from rest_framework.response import Response 
from rest_framework import serializers
from levelupapi.models import GameType

class GameTypes(ViewSet):
    def retrieve(self, request, pk=None):
        try:
            game_type = GameType.objects.get(pk=pk)
            serializer = GameTypeSerializer(game_type, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def list(self, request):
        gametypes = GameType.objects.all()

        serializer = GameTypeSerializer(
            gametypes, many=True, context={'request': request}
        )
        return Response(serializer.data)


class GameTypeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = GameType
        url = serializers.HyperlinkedIdentityField(
          view_name='gametype',
          lookup_field='id'
        )
        fields = ('id', 'url', 'label')
