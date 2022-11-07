from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Article
from .serializers import ArticleSer, CommentSer, UserSer
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from .permissions import CostomPermision
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination
from django.contrib.auth.models import User
from rest_framework.viewsets import ModelViewSet


class ArticleView(APIView):
    def get(self, request):
        queryset = Article.objects.all()
        paginator = LimitOffsetPagination()
        result = paginator.paginate_queryset(queryset=queryset, request=request)
        serializer = ArticleSer(instance=result, many=True, context={"request": request})
        return Response(serializer.data)



class ArticleViewSet(ModelViewSet):
    queryset = Article.objects.all()
    serializer_class  = ArticleSer


class ArticleDetail(APIView):

    def post(self, request, pk):
        query_set = Article.objects.get(id=pk)
        serializer = ArticleSer(instance=query_set, context={"request": request})

        return Response(data=serializer.data)


class ArticleAddView(APIView):
    authentication_classes = [TokenAuthentication, IsAuthenticated]

    def post(self, request):

        serializer = ArticleSer(data=request.data)

        if serializer.is_valid():

            if request.user.is_authenticated:
                serializer.validated_data["user"] = request.user

            serializer.save()

            return Response({"message": "added"}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ArticleUpdateView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [CostomPermision]

    def put(self, request, pk):
        instance = Article.objects.get(id=pk)

        self.check_object_permissions(request, instance)

        serializer = ArticleSer(data=request.data, partial=True)

        if serializer.is_valid():
            serializer.update(instance=instance, validated_data=serializer.validated_data)
            serializer.save()

            return Response({"message": "Updated"}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ArticleDeleteView(APIView):

    def delete(self, request, pk):
        instance = Article.objects.get(id=pk)
        instance.delete()

        return Response({"message": "deleted"}, status=status.HTTP_200_OK)


class ArticleComments(APIView):

    def get(self, request, pk):
        instance = Article.objects.get(id=pk).comments.all()
        serializer = CommentSer(instance=instance, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)



class UserDetailView(APIView):
    def get(self, request):
        users = User.objects.all()
        serializer = UserSer(instance=users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)



# class ArticleViewSet(ViewSet):
#     permission_classes = [IsAuthenticated]

#     def list(self, request):
#         queryset = Article.objects.all()
#         serializer = ArticleSer(instance=queryset, many=True)

#         return Response(serializer.data, status=status.HTTP_202_ACCEPTED)

#     def retrieve(self, request, pk=None):

#         instance = Article.objects.get(id=pk)
#         serialize = ArticleSer(instance=instance)

#         return Response(serialize.data, status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)

#     def create(self, request):

#         serializer = ArticleSer(data=request.data)

#         if serializer.is_valid():

#             if request.user.is_authenticated:
#                 serializer.validated_data["user"] = request.user

#             serializer.save()

#             return Response({"message": "added"}, status=status.HTTP_200_OK)

#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     def delete(self, request, pk=None):
        
#         instance = Article.objects.get(id=pk)
#         instance.delete()

#         return Response({"message": "deleted"}, status=status.HTTP_200_OK)

#     def update(self, request, pk=None):

#         instance = Article.objects.get(id=pk)

#         self.check_object_permissions(request, instance)

#         serializer = ArticleSer(data=request.data, partial=True)

#         if serializer.is_valid():
#             serializer.update(instance=instance, validated_data=serializer.validated_data)
#             serializer.save()

#             return Response({"message": "Updated"}, status=status.HTTP_200_OK)

#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)