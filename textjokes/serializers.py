from rest_framework import serializers
from models import TextJokeCategory, TextJoke, TextPunchline, JokeVotes, \
    TextComment
from ppuser.serializers import UserSerializer


class JokeCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = TextJokeCategory
        fields = ('id', 'name', 'slug', 'description', 'num_jokes')


class TextCommentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True, many=False)

    class Meta:
        model = TextComment
        fields = ('id', 'user', 'text', 'active', 'created', 'comment_on')


class TextPunchlineSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True, many=False)
    comments = TextCommentSerializer(read_only=True, many=True)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_validation_exclusions(self):
        exclusions = super(TextPunchlineSerializer, self) \
            .get_validation_exclusions()
        return exclusions + ['user']

    class Meta:
        model = TextPunchline
        fields = ('id', 'user', 'text', 'created', 'active', 'responses', 'score', 'comments')


class TextJokeSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True, many=False)
    category = JokeCategorySerializer(read_only=True, many=False)
    punchlines = TextPunchlineSerializer(read_only=True, many=True)
    user_has_voted = serializers.SerializerMethodField('test_has_voted')
    comments = TextCommentSerializer(read_only=True, many=True)

    def test_has_voted(self, obj):
        user = self.context['request'].user
        if user.is_anonymous() is True:
            return False
        else:
            # Determines whether or not the user has voted on a given joke.
            # time will tell whether or not this actually scales, but it's
            # not too bad schematically, using only filtered outputs of keys
            if user.pk in obj.joke_votes.filter(user=user).filter(joke=obj).values_list("user__id", flat=True):
                return True
            else:
                return False

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_validation_exclusions(self):
        exclusions = super(TextJokeSerializer, self).get_validation_exclusions()
        return exclusions + ['user']

    class Meta:
        model = TextJoke
        fields = ('id', 'category', 'user_has_voted', 'user', 'punchlines', 'text', 'created', 'active', 'responses', 'score', 'comments')


class TextJokeSerializerSimple(serializers.ModelSerializer):
    user = UserSerializer(read_only=True, many=False)
    punchlines = TextPunchlineSerializer(read_only=True, many=True)
    comments = TextCommentSerializer(read_only=True, many=True)

    class Meta:
        model = TextJoke
        fields = ('id', 'user', 'punchlines', 'text', 'created', 'active',
                  'responses', 'score', 'comments')


class JokeVoteSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True, many=False)
    joke = TextJokeSerializer(read_only=True, many=False)

    class Meta:
        model = JokeVotes
        fields = ('id', 'user', 'joke', 'vote')

    def get_validation_exclusions(self):
        exclusions = super(JokeVoteSerializer, self) \
            .get_validation_exclusions()
        return exclusions + ['user', ]

    def perform_create(self, serializer):
        print "I AM CREATING!"


class SimpleJokeVoteSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True, many=False)
    joke = TextJokeSerializerSimple(read_only=True, many=False)

    class Meta:
        model = JokeVotes
        fields = ('id', 'user', 'joke', 'vote')
