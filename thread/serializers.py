from rest_framework import serializers

from thread.models import Category, Thread, Answer, Image, Comment, Comment_Image, Awareness
from thread.tasks import send_comment
from thread.utils import average_func


class CategorySerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Category
        fields = '__all__'


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ['image']


class CommentImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment_Image
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    images = CommentImageSerializer(many=True, read_only=True)

    class Meta:
        model = Comment
        fields = '__all__'

    def create(self, validated_data):
        requests = self.context.get('request')
        images = requests.FILES
        comment = Comment.objects.create(**validated_data)
        for image in images.getlist('images'):
            Comment_Image.objects.create(comment=comment, image=image)
        answer = validated_data['answer']
        author = validated_data['owner']
        body = validated_data['text']
        send_comment.delay(answer=str(answer), author=str(author), body=str(body))
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
        try:
            representation['rating'] = average_func(instance)
        except ZeroDivisionError:
            pass
        return representation


class ThreadSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')
    answers = AnswerSerializer(many=True, read_only=True)

    class Meta:
        model = Thread
        fields = '__all__'


class RatingSerializer(serializers.Serializer):
    rating = serializers.IntegerField(required=True, min_value=1, max_value=5)


class AwarenessSerializer(serializers.ModelSerializer):
    class Meta:
        model = Awareness
        fields = '__all__'
