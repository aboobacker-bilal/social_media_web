import graphene
from graphene_django import DjangoObjectType

from post.models import Post, Like, Comment
from user.models import UserProfile, Follow


class UserProfileType(DjangoObjectType):
    class Meta:
        model = UserProfile
        fields = ("user", "bio", "name", "profile_pic")


class PostType(DjangoObjectType):
    class Meta:
        model = Post
        fields = ("id", "image", "user", "caption")


class Query(graphene.ObjectType):
    all_posts = graphene.List(PostType)
    user_post = graphene.Field(PostType, id=graphene.Int())
    user_profile = graphene.Field(UserProfileType,
                                  username=graphene.String(required=True))

    def resolve_all_posts(self, info):
        return Post.objects.all()

    def resolve_user_post(self, info, id):
        return Post.objects.get(pk=id)

    def resolve_user_profile(self, info, username):
        return UserProfile.objects.get(user__username=username)


class CreateMutation(graphene.Mutation):
    class Arguments:
        user = graphene.String(required=True)
        image = graphene.String(required=True)
        caption = graphene.String(required=True)

    post = graphene.Field(PostType)

    @classmethod
    def mutate(cls, root, info, **kwargs):
        user = kwargs.get('user')
        image = kwargs.get('image')
        caption = kwargs.get('caption')
        user_profile = UserProfile.objects.get(user__username=user)
        posts = Post(user=user_profile, image=image, caption=caption)
        posts.save()
        return CreateMutation(post=posts)


class UpdateMutation(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)
        caption = graphene.String(required=True)

    post = graphene.Field(PostType)

    @classmethod
    def mutate(cls, root, info, id, caption):
        post = Post.objects.get(pk=id)
        post.caption = caption
        post.save()
        return UpdateMutation(post=post)


class DeleteMutation(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)

    post = graphene.Field(PostType)

    @classmethod
    def mutate(cls, root, info, id):
        post = Post.objects.get(pk=id)
        post.delete()
        return DeleteMutation(post=post)


class Mutation(graphene.ObjectType):
    new_post = CreateMutation.Field()
    update_caption = UpdateMutation.Field()
    delete_post = DeleteMutation.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
