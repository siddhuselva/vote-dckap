from django.shortcuts import render
from .models import Post, Vote, User
from django.http import JsonResponse, HttpResponse
from django.db.models import F
from django.db.models import Q
# Create your views here.


# def index(request):
#     post = Post.objects.all()
#     context = {"posts": post}
#     return render(request, "index.html", context)


def user_post(request, user_id):
    all_posts = Post.objects.all()
    user = User.objects.filter(id=user_id)
    if not user.exists():
        user = User(user_name=f"user{user_id}")
        user.save()
    posts = []
    item = {}
    for post in all_posts:
        item['id'] = post.id
        item['post'] = post.post
        item['title'] = post.title
        item['up_vote'] = post.up_vote
        item['down_vote'] = post.down_vote
        item['type'] = 2
        if post.user_vote.filter(id=user_id).exists():
            q = Vote.objects.get(
                Q(post_id=post.id) & Q(user_id=user_id))
            current_vote = q.vote
            item['type'] = 1 if q.vote else 0
        posts.append(item)
        item = {}

    context = {"posts": posts, "user_id": user_id}
    return render(request, "index.html", context)


def vote(request, user_id):
    id = int(request.POST.get('postid'))
    vote = request.POST.get('vote')
    post_vote = Post.objects.get(id=id)

    if post_vote.user_vote.filter(id=user_id).exists():

        q = Vote.objects.get(
            Q(post_id=id) & Q(user_id=user_id))
        current_vote = q.vote

        if current_vote == True: # noqa

            if vote == 'up_vote':
                post_vote.up_vote = post_vote.up_vote - 1
                post_vote.user_vote.remove(User.objects.get(id=user_id))
                post_vote.save()
                post_vote.refresh_from_db()
                up = post_vote.up_vote
                down = post_vote.down_vote
                q.delete()

                return JsonResponse({'up': up, 'down': down, 'remove': 'none'})

            if vote == 'down_vote':

                post_vote.up_vote = post_vote.up_vote - 1
                post_vote.down_vote = post_vote.down_vote + 1
                post_vote.save()

                q.vote = False

                q.save(update_fields=['vote'])

                post_vote.refresh_from_db()
                up = post_vote.up_vote
                down = post_vote.down_vote

                return JsonResponse({'up': up, 'down': down})

        if current_vote == False: # noqa

            if vote == 'up_vote':
                # Change vote in Post
                post_vote.up_vote = post_vote.up_vote + 1
                post_vote.down_vote = post_vote.down_vote - 1
                post_vote.save()

                q.vote = True
                q.save(update_fields=['vote'])

                post_vote.refresh_from_db()
                up = post_vote.up_vote
                down = post_vote.down_vote

                return JsonResponse({'up': up, 'down': down})

            if vote == 'down_vote':
                post_vote.down_vote = post_vote.down_vote - 1
                post_vote.user_vote.remove(User.objects.get(id=user_id))
                post_vote.save()
                post_vote.refresh_from_db()
                up = post_vote.up_vote
                down = post_vote.down_vote
                q.delete()

                return JsonResponse({'up': up, 'down': down, 'remove': 'none'})
    else:
        if vote == 'up_vote':
            post_vote.up_vote = post_vote.up_vote + 1
            post_vote.user_vote.add(User.objects.get(id=user_id))
            post_vote.save()
            vote_data = Vote(post_id=id, user_id=user_id, vote=True)#, vote_type=True)
            vote_data.save()
        else:
            post_vote.down_vote = post_vote.down_vote + 1
            post_vote.user_vote.add(User.objects.get(id=user_id))
            post_vote.save()
            new = Vote(post_id=id, user_id=user_id, vote=False)#, vote_type=False)
            new.save()

    post_vote.refresh_from_db()
    up_count = post_vote.up_vote
    down_count = post_vote.down_vote

    return JsonResponse({'up': up_count, 'down': down_count})

