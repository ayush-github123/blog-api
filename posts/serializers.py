from rest_framework import serializers
from django.contrib.contenttypes.models import ContentType
from posts.models import Post, Comment, Tag, Category, LikeDislike

class CommentSerializer(serializers.ModelSerializer):
    post = serializers.PrimaryKeyRelatedField(read_only=True)
    like_count = serializers.SerializerMethodField()
    dislike_count = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ('id', 'post', 'content', 'like_count', 'dislike_count', 'created_at')
        read_only_fields = ['like_count', 'dislike_count']

    def get_like_count(self, obj):
        return LikeDislike.objects.filter(content_type=ContentType.objects.get_for_model(obj), object_id=obj.id, value=1).count()

    def get_dislike_count(self, obj):
        return LikeDislike.objects.filter(content_type=ContentType.objects.get_for_model(obj), object_id=obj.id, value=-1).count()


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name')


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id', 'name')


class PostSerializer(serializers.ModelSerializer):
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all(), required=False)
    tags = serializers.ListField(child=serializers.CharField(), write_only=True, required=False)
    comments = CommentSerializer(many=True, read_only=True)
    user = serializers.CharField(read_only=True)
    like_count = serializers.SerializerMethodField()
    dislike_count = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = '__all__'
        read_only_fields = ['like_count', 'dislike_count']

    def get_like_count(self, obj):
        return LikeDislike.objects.filter(content_type=ContentType.objects.get_for_model(obj), object_id=obj.id, value=1).count()

    def get_dislike_count(self, obj):
        return LikeDislike.objects.filter(content_type=ContentType.objects.get_for_model(obj), object_id=obj.id, value=-1).count()

    def create(self, validated_data):
        tags_data = validated_data.pop('tags', [])  
        post = Post.objects.create(**validated_data)

        for tag_name in tags_data:
            tag, created = Tag.objects.get_or_create(name=tag_name)
            post.tags.add(tag)

        return post


class LikeDislikeSerializers(serializers.ModelSerializer):
    user = serializers.CharField(read_only=True)
    content_type = serializers.SlugRelatedField(queryset=ContentType.objects.all(), slug_field='model')

    class Meta:
        model = LikeDislike
        fields = '__all__'

    def validate(self, data):
        """ Validate that user can't like or dislike the same post twice """
        request = self.context['request']
        user = request.user

        existing_reaction = LikeDislike.objects.filter(
            user=user,
            content_type=data['content_type'],
            object_id=data['object_id'],
        ).first()

        if existing_reaction:
            if existing_reaction.value == data['value']:
                existing_reaction.delete()
                raise serializers.ValidationError("Reaction removed.")
            else:
                existing_reaction.value = data['value']
                existing_reaction.save()
                return data

        return data  # ✅ Always return data

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)
