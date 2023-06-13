"""View module for handling requests about song"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from tunaapi.models import Artist, SongGenre, Song


class SongView(ViewSet):
    """Song view"""
    
    def retrieve(self, request, pk):

        song = Song.objects.get(pk=pk)
        serializer = SongSerializer(song)
        return Response(serializer.data)


    def list(self, request):
      
        song = Song.objects.all() 
        
        artist = request.query_params.get('id', None)
        if artist is not None:
            song = song.filter(artist_id=artist)

        genre = request.query_params.get('description', None)
        if genre is not None:
            genre = genre.filter(description=genre)
        serializer = SongSerializer(song, many=True)
        return Response(serializer.data)
    
    def create(self, request):

        artist_id = Artist.objects.get(pk=request.data["artist_id"])

        song = Song.objects.create(
        title = request.data["title"],
        album=request.data["album"],
        length=request.data["length"],
        artist_id=artist_id
        )
        serializer = SongSerializer(song)
        return Response(serializer.data)
    
    def update(self, request, pk):
       """Handle PUT requests for a song

        Returns:
        Response -- Empty body with 204 status code
        """

       song = Song.objects.get(pk=pk)
       song.title = request.data["title"]
       song.album = request.data["album"]
       song.length = request.data["length"]
       artist_id = Artist.objects.get(pk=request.data["artist_id"])
       song.artist_id = artist_id
       song.save()
       return Response(None, status=status.HTTP_204_NO_CONTENT)
    
    def destroy(self, request, pk):
        song = Song.objects.get(pk=pk)
        song.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)

class SongGenreSerializer(serializers.ModelSerializer):
    """JSON serializer for Song Genre"""
    class Meta:
        model = SongGenre
        fields = ('genre_id', )
        depth = 2

class SongSerializer(serializers.ModelSerializer):
  """JSON serializer for song   
  """
  genre = SongGenreSerializer(many=True, read_only=True)
  class Meta:
        model = Song
        fields = ('id', 'title', 'artist_id', 'album', 'length', 'genre')
        
        depth = 1
