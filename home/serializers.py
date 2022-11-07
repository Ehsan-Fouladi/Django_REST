from rest_framework import serializers
from .models import Article, Comment
from django.utils.timezone import now
from persiantools.jdatetime import JalaliDate
from django.contrib.auth.models import User



class CommentSer(serializers.ModelSerializer):
    # days_age = serializers.SerializerMethodField()
    # date = serializers.SerializerMethodField()

#  'days_age', model comment
# 'date' model comment

    class Meta:
        model = Comment
        fields = ('id', 'text',)

        def get_days(self, obj):
            return (now().date() - obj.date).days

        def get_date(self, obj):
            date = JalaliDate(obj.date, locale="fa")
            return date.strftime('%c')


class CheckTitle:
    def __call__(self, data):
        if data['title'] == 'html':
            return serializers.ValidationError({'title': "this is title not No"})

def check_title(data):
    if data['title'] == 'html':
        raise serializers.ValidationError({'title': 'this is html not found'})


class ArticleSer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()
    user = serializers.SlugRelatedField(read_only=True,slug_field="username")
    class Meta:
        model = Article
        fields = ('id', 'status', 'title', 'user', 'image')
        validators = [
            CheckTitle()
        ]

    def get_image(self, obj):
        request = self.context.get("request")
        if obj.image:
            image_url = obj.image.url 
            return request.build_absolute_uri(image_url)
        return None


class UserSer(serializers.ModelSerializer):
    article  = ArticleSer(many=True)
    class Meta:
        model = User
        fields = "__all__"