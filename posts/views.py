import json
from json.decoder     import JSONDecodeError
from datetime         import date, datetime, timedelta

from django.views     import View
from django.http      import JsonResponse
from django.db.models import Q
from django.core.paginator import Paginator ,EmptyPage, PageNotAnInteger

from users.utils      import login_decorator
from posts.models     import Category, Post, Comment
from users.models     import User


class PostDetailView(View):
    def get(self, request, post_id):
        if not Post.objects.filter(id=post_id).exists():
            return JsonResponse({"MESSAGE": "POST DOES NOT EXIST"}, status=404)
        
        cookie = request.COOKIES.get('hits', '|')
        post = Post.objects.select_related('author').get(id=post_id)
        temp = post.view_count

        if f'{post_id}' not in cookie:
            temp += 1
        
        post_list = {
                "title": post.title,
                "author": post.author.name,
                "user_id": post.author.id,
                "content": post.content,
                "written": post.created_at.strftime("%Y.%m.%d %H:%M"),
                "category": post.category.name,
                "category_id": post.category_id,
                "view_count": temp,
            }

        if f'{post_id}' in cookie:
            return JsonResponse({"RESULT": post_list}, status=200)
        
        else:
            res = JsonResponse({"RESULT": post_list}, status=200)
            
            expire_date, time_now = datetime.now(), datetime.now()
            expires = (expire_date + timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0) - time_now
            max_age = expires.total_seconds()
            cookie += f'{post_id}|'
            res.set_cookie('hits', value=cookie, max_age=max_age)
            post.view_count += 1
            post.save()
                
            return res

class PostListView(View):
    def get(self, request):
        posts = Post.objects.select_related('author').order_by('-created_at')
        OFFSET = request.GET.get('page', 1)
        LIMIT = 20

        if int(OFFSET) <= 0:
            return JsonResponse({"MESSAGE": "MUST START WITH GREATER THAN 0"}, status=404)
        
        START = (int(OFFSET)-1) * LIMIT

        post_list = [{
            "title"     : post.title,
            "author"    : post.author.name,
            "written"   : post.created_at.strftime('%Y.%m.%d %H:%M'),
            "post_id"   : post.id,
            "user_id"   : post.author.id,
            "category": post.category.name,
            "category_id": post.category_id,
            "view_count": post.view_count 
        }for post in posts[START:START+LIMIT]]

        return JsonResponse({
            "RESULT": {
                "data": post_list,
                "post_count": len(post_list)
            }
        }, status=200)

class PostView(View):
    @login_decorator
    def post(self, request):
        try:
            data = json.loads(request.body)
            if not Category.objects.filter(name=data['category']).exists():
                return JsonResponse({"MESSAGE": "CATEGORY DOES NOT EXIST"}, status=404)
            category = Category.objects.get(name=data['category'])
            
            if data["title"].strip() == "":
                return JsonResponse({"MESSAGE": "TITLE MUST CONTAIN WORDS"}, status=404)
            
            if data["content"].strip() == "":
                return JsonResponse({"MESSAGE": "MUST CONTAIN WORDS"}, status=404)    
            elif len(data["content"].strip()) <= 10:
                return JsonResponse({"MESSAGE": "NEED_MORE_THAN_10_WORDS"}, status=404)
            
            user_id = request.user.id
            
            Post.objects.create(
                category  = category,
                title     = data['title'],
                content   = data['content'],
                author_id = user_id
            )
            
            return JsonResponse({"MESSAGE": "SUCCESS"}, status=201)
        
        except KeyError:
            return JsonResponse({'MESSAGE':'KEY_ERROR'}, status = 400)
        except JSONDecodeError:
            return JsonResponse({"message": "INVALID DATA FORMAT"}, status=400)

class PostManageView(View):
    @login_decorator
    def delete(self, request, post_id):
        if not Post.objects.filter(id=post_id).exists():
            return JsonResponse({"MESSAGE": "POST DOES NOT EXIST"}, status=404)
        
        post = Post.objects.get(id=post_id)
        id = request.user.id
        
        if post.author.id == id:
            post.delete()
        else:
            return JsonResponse({"MESSAGE": "INVALID USER"}, status=403)

        return JsonResponse({"MESSAGE": "SUCCESSFULLY DELETED"}, status=204)

    @login_decorator
    def patch(self, request, post_id):
        try:
            data = json.loads(request.body)
            
            try:
                title = data["title"]
            except:
                title = False
            try:
                content = data["content"]
            except:
                content = False
            
            if content:
                if data["content"].strip() == "":
                    return JsonResponse({"MESSAGE": "MUST CONTAIN WORDS"}, status=404)    
                elif len(data["content"].strip()) <= 10:
                    return JsonResponse({"MESSAGE": "NEED_MORE_THAN_10_WORDS"}, status=404)
            
            if title:
                if data["title"].strip() == "":
                    return JsonResponse({"MESSAGE": "TITLE MUST CONTAIN WORDS"}, status=404)
            
            if not Post.objects.filter(id=post_id).exists():
                return JsonResponse({"MESSAGE": "POST DOES NOT EXIST"}, status=404)
            
            post = Post.objects.get(id=post_id)
            id = request.user.id
            
            if post.author.id == id:
                if content and title:
                    post.content = content
                    post.title   = title
                elif not content and title:
                    post.title = title
                elif not title and content:
                    post.content = content
                
                post.save()
            else:
                return JsonResponse({"MESSAGE": "INVALID USER"}, status=404)
            
            return JsonResponse({"MESSAGE": "SUCCESSFULLY UPDATED"}, status=201)
        
        except KeyError:
            return JsonResponse({"MESSAGE": "KEY_ERROR"}, status=404)
        except JSONDecodeError:
            return JsonResponse({"message": "INVALID DATA FORMAT"}, status=400)

class CommentView(View):
    @login_decorator
    def post(self,request,post_id):
        try:
            user              = request.user
            data              = json.loads(request.body)
            content           = data['content']
            parent_comment_id = data.get('parent_comment',None)

            if not Post.objects.filter(id=post_id).exists():
                return JsonResponse({"MESSAGE":"INVALID_POSTING"},status=400)
            
            if content == "":
                return JsonResponse({"MESSAGE":"NOT_COMMENT"},status=400)

            post = Post.objects.get(id=post_id)

            Comment.objects.create(
                author            = user,
                post              = post,
                content           = content,
                parent_comment_id = parent_comment_id 
            )
            return JsonResponse({"MESSAGE":"COMMENT_SUCCESS"},status = 201)
        except KeyError:
            return JsonResponse({"MESSAGE": "KEY_ERROR"}, status=400)
    
    def get(self,request,post_id):        
        offset = request.GET.get('page', 1)
        limit = 3
        start = (int(offset)-1) * limit

        if not Comment.objects.filter(post=post_id).exists():
            return JsonResponse({"MESSAGE": "NOT_EXISTS"}, status=404)

        if int(offset) <= 0:
            return JsonResponse({"MESSAGE": "MUST START WITH GREATER THAN 0"}, status=404)
        
        post     = Post.objects.select_related('author').get(id=post_id)
        comments = Comment.objects.filter(post=post_id,parent_comment_id=None).order_by('created_at')

        comment_list=[{
            'id'            : comment.id,
            'post_id'       : post.id,
            'name'          : post.author.name,
            'content'       : comment.content,
            'created_at'    : comment.created_at.strftime("%Y.%m.%d %H:%M"),
            'parent_comment': [{
                'id'               : recomment.id,
                'parent_comment_id': recomment.parent_comment_id,
                'name'             : post.author.name,
                'content'          : recomment.content,
                'created_at'       : recomment.created_at.strftime("%Y.%m.%d %H:%M"),
            }for recomment in Comment.objects.filter(post=post_id, parent_comment_id=comment.id)\
                                             .order_by('created_at')[start:start+limit]] or '없음' 
        }for comment in comments]
        
        
        return JsonResponse({"COMMENT":comment_list},status = 200)

    @login_decorator
    def patch(self,request,comment_id):
        try:
            user = request.user
            data = json.loads(request.body)
            content = data['content']

            if content == "":
                    return JsonResponse({"MESSAGE":"NOT_COMMENT"},status=400)

            if not Comment.objects.filter(id=comment_id, author=user).exists():
                return JsonResponse({'MESSAGE':'NOT_EXISTS'},status=400)

            Comment.objects.filter(id=comment_id).update(content=content)
            return JsonResponse({"MESSAGE":"UPDATE_SUCCESS"},status = 200)
        except KeyError:
            return JsonResponse({"MESSAGE": "KEY_ERROR"}, status=400)

    @login_decorator
    def delete(self,request,comment_id):
        user = request.user

        if not Comment.objects.filter(id=comment_id).exists():
            return JsonResponse({"MESSAGE":"INVALID_COMMENT"}, status=404)
        
        comment = Comment.objects.filter(id=comment_id, author=user)
        comment.delete()

        return JsonResponse({"MESSAGE":"DELETE_SUCCESS"},status = 200)

class SearchView(View):
    def get(self, request):
        q = Q()
        search_target = request.GET.get('search-type', '')
        target = request.GET.get('search', '')

        search_filter = {
            'all'     : Q(author__name__icontains = target) | Q(category__name__icontains = target) | Q(title__icontains = target) | Q(content__icontains = target),
            'author'  : Q(author__name__icontains = target),
            'category': Q(category__name__icontains = target),
            'title_content': Q(title__icontains = target) | Q(content__icontains = target),
        }

        posts = Post.objects.filter(search_filter[search_target]).select_related('author', 'category').distinct()

        if not posts:
            return JsonResponse({"RESULT": []},status=200)
        
        posts_list = [{
            "title"      : post.title,
            "author"     : post.author.name,
            "written"    : post.created_at.strftime('%Y.%m.%d %H:%M'),
            "post_id"    : post.id,
            "user_id"    : post.author.id,
            "category"   : post.category.name,
            "category_id": post.category_id,
            "view_count" : post.view_count 
        }for post in posts]

        return JsonResponse({
            "MESSAGE": posts_list,
            "posts_count": len(posts)
        }, status=200)
