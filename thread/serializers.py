from rest_framework import serializers

from thread.models import Category, Thread, Answer, Image, Comment


class CategorySerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Category
        fields = '__all__'


class ThreadSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')

    class Meta:
        model = Thread
        fields = '__all__'


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ['image']


class CommentSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    images = ImageSerializer(many=True, read_only=True)

    class Meta:
        model = Comment
        fields = '__all__'

    def create(self, validated_data):
        requests = self.context.get('request')
        images = requests.FILES
        comment = Comment.objects.create(**validated_data)

        for image in images.getlist('images'):
            Image.objects.create(comment=comment, image=image)

        return comment


class AnswerSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    images = ImageSerializer(many=True, read_only=True)
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Answer
        fields = '__all__'

    def create(self, validated_data):
        requests = self.context.get('request')
        images = requests.FILES
        answer = Answer.objects.create(**validated_data)

        for image in images.getlist('images'):
            Image.objects.create(answer=answer, image=image)
        return answer

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['likes'] = instance.likes.filter(like=True).count()
        rating_result = 0
        for rating in instance.ratings.all():
            rating_result += int(rating.rating)
        try:
            representation['rating'] = rating_result / instance.ratings.all().count()
        except ZeroDivisionError:
            pass
        return representation


class RatingSerializer(serializers.Serializer):
    rating = serializers.IntegerField(required=True, min_value=1, max_value=5)