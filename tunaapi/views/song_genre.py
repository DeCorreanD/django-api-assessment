"""View module for handling requests about song_genre"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from tunaapi.models import Song, Genre, SongGenre


class SongGenreView(ViewSet):
    """Song_Genre view"""
    
    def retrieve(self, request, pk):

        song_genre = SongGenre.objects.get(pk=pk)
        serializer = SongGenreSerializer(song_genre)
        return Response(serializer.data)


    def list(self, request):
      
        song_genre = SongGenre.objects.all()
        serializer = SongGenreSerializer(song_genre, many=True)
        return Response(serializer.data)
    
    def create(self, request):

        song_id = Song.objects.get(pk=request.data["song_id"])
        genre_id = Genre.objects.get(pk=request.data["genre_id"])

        song_genre = SongGenre.objects.create(
        song_id=song_id,
        genre_id=genre_id
        )
        serializer = SongGenreSerializer(song_genre)
        return Response(serializer.data)
    
    def destroy(self, request, pk):
        song = Song.objects.get(pk=pk)
        song.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)


class SongGenreSerializer(serializers.ModelSerializer):
  """JSON serializer for song   
  """
  class Meta:
        model = SongGenre
        fields = ('id', 'genre_id', 'song_id')
        depth = 2
