"""View module for handling requests about genre"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from tunaapi.models import Genre, SongGenre


class GenreView(ViewSet):
    """Level up genre view"""

    def retrieve(self, request, pk):

        genre = Genre.objects.get(pk=pk)
        serializer = GenreSerializer(genre)
        return Response(serializer.data)


    def list(self, request):
      
        genre = Genre.objects.all()
        serializer = GenreSerializer(genre, many=True)
        return Response(serializer.data)
    
    def create(self, request):

        genre = Genre.objects.create(
        description = request.data["description"],
        )
        serializer = GenreSerializer(genre)
        return Response(serializer.data)
    
    def update(self, request, pk):
      
       """Handle PUT requests for a genre

        Returns:
        Response -- Empty body with 204 status code
        """

       genre = Genre.objects.get(pk=pk)
       genre.description = request.data["description"]
       genre.save()
       return Response(None, status=status.HTTP_204_NO_CONTENT)
    
    def destroy(self, request, pk):
        genre = Genre.objects.get(pk=pk)
        genre.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)

class SongGenreSerializer(serializers.ModelSerializer):
    """JSON serializer for Song Genre"""
    class Meta:
        model = SongGenre
        fields = ('song_id', )
        depth = 1
        
class GenreSerializer(serializers.ModelSerializer):
  """JSON serializer for genre   
  """
  song = SongGenreSerializer(many=True, read_only=True)

  class Meta:
        model = Genre
        fields = ('id', 'description', 'song')
        depth = 0
