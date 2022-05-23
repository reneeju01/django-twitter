from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from tweets.api.serializers import TweetSerializer, TweetSerializerForCreate
from tweets.models import Tweet
from newsfeeds.services import NewsFeedService


class TweetViewSet(viewsets.GenericViewSet):
    """
    API endpoint that allows users to create, list tweets
    """
    # serializer_class = TweetSerializer
    serializer_class = TweetSerializerForCreate

    def get_permissions(self):
        if self.action == 'list':
            return [AllowAny()]
        return [IsAuthenticated()]

    def list(self, request):
        """
        Override the list method, do not list all tweets, must specify
        user_id as a filter condition
        """
        if 'user_id' not in request.query_params:
            return Response('missing user_id', status=400)
        user_id = request.query_params['user_id']

        # This query will be translated as
        # select * from twitter_tweets
        # where user_id = xxx
        # order by created_at desc
        # This SQL query will use the joint index of user and created_at
        # A simple user index is not enough
        tweets = Tweet.objects.filter(user_id=user_id).order_by('-created_at')
        serializer = TweetSerializer(tweets, many=True)
        # Generally speaking, the response in json format should use the hash
        # format by default. instead of list format (by convention)
        return Response({'tweets': serializer.data})

    def create(self, request):
        """
        Override the create method, because need to use the currently logged in
        user as tweet.user by default
        """
        serializer = TweetSerializerForCreate(
            data=request.data,
            context={'request': request},
        )
        if not serializer.is_valid():
            return Response({
                "success": False,
                "message": "Please check input.",
                "errors": serializer.errors,
            }, status=400)
        # save will call create method in TweetSerializerForCreate
        tweet = serializer.save()
        NewsFeedService.fansout_to_followers(tweet)
        return Response(TweetSerializer(tweet).data, status=201)