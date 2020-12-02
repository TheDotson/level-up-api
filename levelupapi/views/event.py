from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.http import HttpResponseServerError
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from levelupapi.models import Game, Event, Gamer, GamerEvent
from levelupapi.views.game import GameSerializer

class Events(ViewSet):

    def create(self, request):
        gamer = Gamer.objects.get(user=request.auth.user)
        event = Event()
        event.time = request.data["time"]
        event.date = request.data["date"]
        event.description = request.data["description"]
        event.organizer = gamer
        game = Game.objects.get(pk=request.data["gameId"])
        event.game = game

        try:
            event.save()
            serializer = EventSerializer(event, context={'request': request})
            return Response(serializer.data)
        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)


    def retrieve(self, request, pk=None):
        try:
            event = Event.objects.get(pk=pk)
            serializer = EventSerializer(event, context={'request': request})
            return Response(serializer.data)
        except Exception:
            return HttpResponseServerError(ex)


    def update(self, request, pk=None):
        organizer = Gamer.objects.get(user=request.auth.user)
        event = Event.objects.get(pk=pk)
        event.description = request.data["description"]
        event.date = request.data["date"]
        event.time = request.data["time"]
        event.organizer = organizer
        game = Game.objects.get(pk=request.data["gameId"])
        event.game = game
        event.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk=None):
        try:
            event = Event.objects.get(pk=pk)
            event.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except Event.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def list(self, request):
        gamer = Gamer.objects.get(user=request.auth.user)
        events = Event.objects.all()

        for event in events:
            event.joined = None

            try: 
                GamerEvent.objects.get(event=event, gamer=gamer)
                event.joined = True
            except GamerEvent.DoesNotExist:
                event.joined = False

        game = self.request.query_params.get('gameId', None)
        if game is not None:
            events = events.filter(game__id=type)

        serializer = EventSerializer(
            events, many=True, context={'request': request})
        return Response(serializer.data)


    @action(methods=['get', 'post', 'delete'], detail=True)
    def signup(self, request, pk=None):
        if request.method == "POST":
            event = Event.objects.get(pk=pk)
            gamer = Gamer.objects.get(user=request.auth.user)

            try:
                registration = GamerEvent.objects.get(
                    event=event, gamer=gamer)
                return Response(
                    {'message': 'Gamer already signed up for this event.'},
                    status=status.HTTP_422_UNPROCESSABLE_ENTITY
                )
            except GamerEvent.DoesNotExist:
                registration = GamerEvent()
                registration.event = event
                registration.gamer = gamer
                registration.save()
                return Response({}, status=status.HTTP_201_CREATED)

        elif request.method == "DELETE":
            try:
                event = Event.objects.get(pk=pk)
            except Event.DoesNotExist:
                return Response(
                    {'message': 'Event does not exist.'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            gamer = Gamer.objects.get(user=request.auth.user)
            try: 
                registration = GamerEvent.objects.get(
                    event=event, gamer=gamer)
                registration.delete()
                return Response(None, status=status.HTTP_204_NO_CONTENT)
            except GamerEvent.DoesNotExist:
                return Response(
                    {'message': 'Not currently registered for event.'},
                    status=status.HTTP_404_NOT_FOUND
                )

        return Response({}, status=HTTP_405_METHOD_NOT_ALLOWED)


class EventUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']


class EventGamerSerializer(serializers.ModelSerializer):
    user = EventUserSerializer(many=False)

    class Meta:
        model = Gamer
        fields = ['user']

class GameSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Game
        fields = ('id', 'title', 'maker', 'number_of_players', 'skill_level')

class EventSerializer(serializers.HyperlinkedModelSerializer):
    organizer = EventGamerSerializer(many=False)
    game = GameSerializer(many=False)
    class Meta:
        model = Event
        url = serializers.HyperlinkedIdentityField(
            view_name='event',
            lookup_field='id'
        )
        fields = ('id', 'url', 'game', 'organizer',
                  'description', 'date', 'time', 'joined')
