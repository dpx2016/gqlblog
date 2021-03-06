import graphene
from graphene_django.types import DjangoObjectType, ObjectType

from ..models import Blog
from .authors import AuthorType


class BlogFields():
    title = graphene.String()
    body = graphene.String()


class BlogType(DjangoObjectType, BlogFields):
    class Meta:
        model = Blog

    id = graphene.ID(required=True)
    author = AuthorType()


class BlogInputType(graphene.InputObjectType, BlogFields):
    id = graphene.ID()
    author_id = graphene.ID()


class DeleteBlogInputType(graphene.InputObjectType):
    id = graphene.ID(required=True)


class Query(ObjectType):
    blog = graphene.Field(BlogType, id=graphene.ID(required=True))
    blogs = graphene.List(BlogType)

    def resolve_blog(self, info, **kwargs):
        id = kwargs.get("id")
        return Blog.objects.get(id=id)

    def resolve_blogs(self, info, **kwargs):
        return Blog.objects.all()


class CreateBlog(graphene.Mutation):
    class Arguments:
        input = BlogInputType(required=True)

    ok = graphene.Boolean()
    blog = graphene.Field(BlogType)

    @staticmethod
    def mutate(root, info, input):
        blog = Blog()
        for key, val in input.items():
            setattr(blog, key, val)
        blog.save()
        return CreateBlog(ok=True, blog=blog)


class UpdateBlog(graphene.Mutation):
    class Arguments:
        input = BlogInputType(required=True)

    ok = graphene.Boolean()
    blog = graphene.Field(BlogType)

    @staticmethod
    def mutate(root, info, input):
        id = input.get("id")
        blog = Blog.objects.get(id=id)
        for key, val in input.items():
            setattr(blog, key, val)
        blog.save()
        return UpdateBlog(ok=True, blog=blog)


class DeleteBlog(graphene.Mutation):
    class Arguments:
        input = DeleteBlogInputType(required=True)

    ok = graphene.Boolean()

    @staticmethod
    def mutate(root, info, input):
        id = input.get("id")
        blog = Blog.objects.get(id=id)
        blog.delete()
        return DeleteBlog(ok=True)


class Mutation(graphene.ObjectType):
    create_blog = CreateBlog.Field()
    update_blog = UpdateBlog.Field()
    delete_blog = DeleteBlog.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)