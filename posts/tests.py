from django.test import TestCase

# Create your tests here.
import re
from django.http import response
import jwt
import json 
import unittest
from django.test import TestCase, Client, client
from users.models import User 
from posts.models import Category, Post,Comment
from my_settings import ALGORITHM, SECRET_KEY

class PostTest(TestCase):
    def setUp(self):
        User.objects.create(
            id       = 1,
            name     = "peter",
            email    = "dissgogo@gmail.com",
            password = "dlangus1234!",
        )
        
        self.token1 = jwt.encode({'id': User.objects.get(id=1).id}, SECRET_KEY, algorithm = ALGORITHM)
        
        User.objects.create(
            id       = 2,
            name     = "kim",
            email    = "kimkim@naver.com",
            password = "iamkim123123!",
        )
        
        self.token2 = jwt.encode({'id': User.objects.get(id=2).id}, SECRET_KEY, algorithm = ALGORITHM)
        Category.objects.create(
            id = 1,
            name = '유머'
        )
        Category.objects.create(
            id = 2,
            name = '시사'
        )
        Category.objects.create(
            id = 3,
            name = '스포츠'
        )
        Post.objects.create(
            id      = 1,
            title   = "title for post1",
            content = "this is peter's post",
            author_id  = User.objects.get(id = 1).id,
            category_id = Category.objects.get(name='유머').id
        )

        Post.objects.create(
            id      = 2,
            title   = "title for post2",
            content = "this is peter's second post",
            author_id  = User.objects.get(id = 1).id,
            category_id = Category.objects.get(name='시사').id
        )

        Post.objects.create(
            id      = 3,
            title   = "title for post3",
            content = "this is peter's third post",
            author_id  = User.objects.get(id = 1).id,
            category_id = Category.objects.get(name='스포츠').id
        )
        Comment.objects.create(
            id = 1,
            content = '하이요',
            post = Post.objects.get(id=1),
            author_id = User.objects.get(id = 1).id,
        )
        Comment.objects.create(
            id = 2,
            content = '바이요',
            parent_comment_id = 1,
            post = Post.objects.get(id=1),
            author_id = User.objects.get(id = 1).id,
        )
        Comment.objects.create(
            id = 3,
            content = '안녕',
            parent_comment_id = 1,
            post = Post.objects.get(id=1),
            author_id = User.objects.get(id = 1).id,
        )

    def tearDown(self):
        User.objects.all().delete()
        Category.objects.all().delete()
        Post.objects.all().delete()
        Comment.objects.all().delete()
    
    def test_create_newpost_post_success(self):
        client  = Client()
        header  = {"HTTP_Authorization" : self.token2}
        token   = header["HTTP_Authorization"]
        payload = jwt.decode(token, SECRET_KEY, algorithms = ALGORITHM)
        user    = User.objects.get(id = payload['id'])
        
        newpost = {
            "id"     : 4,
            "title"  : "title for post1",
            "content": "this is kim's first post",
            "author" : User.objects.get(id = user.id).id,
            "category": "스포츠"
        }
        
        response = client.post('/posts/newpost', json.dumps(newpost), **header, content_type='application/json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json(), {"MESSAGE": "SUCCESS"})

    def test_create_newpost_post_keyerror(self):
        client  = Client()
        header  = {"HTTP_Authorization" : self.token2}
        token   = header["HTTP_Authorization"]
        payload = jwt.decode(token, SECRET_KEY, algorithms = ALGORITHM)
        user    = User.objects.get(id = payload['id'])
        
        newpost = {
            "id"     : 4,
            "content": "this is kim's first post",
            "author" : User.objects.get(id = user.id).id
        }
        
        response = client.post('/posts/newpost', json.dumps(newpost), **header, content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {"MESSAGE": "KEY_ERROR"})
    
    def test_create_newpost_post_jsondecodeerror(self):
        client  = Client()
        header  = {"HTTP_Authorization" : self.token2}
        token   = header["HTTP_Authorization"]
        payload = jwt.decode(token, SECRET_KEY, algorithms = ALGORITHM)
        user    = User.objects.get(id = payload['id'])
        
        response = client.post('/posts/newpost', **header)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {"message": "INVALID DATA FORMAT"})

    def test_create_newpost_post_title_no_word(self):
        client  = Client()
        header  = {"HTTP_Authorization" : self.token2}
        token   = header["HTTP_Authorization"]
        payload = jwt.decode(token, SECRET_KEY, algorithms = ALGORITHM)
        user    = User.objects.get(id = payload['id'])
        
        newpost = {
            "id"     : 4,
            "title"  : " ",
            "content": "this is kim's first post",
            "author" : User.objects.get(id = user.id).id,
            "category": "스포츠" 
        }
        
        response = client.post('/posts/newpost', json.dumps(newpost), **header, content_type='application/json')
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), {"MESSAGE": "TITLE MUST CONTAIN WORDS"})

    def test_create_newpost_post_content_no_word(self):
        client  = Client()
        header  = {"HTTP_Authorization" : self.token2}
        token   = header["HTTP_Authorization"]
        payload = jwt.decode(token, SECRET_KEY, algorithms = ALGORITHM)
        user    = User.objects.get(id = payload['id'])
        
        newpost = {
            "id"     : 4,
            "title"  : "title for post1",
            "content": "      ",
            "author" : User.objects.get(id = user.id).id,
            "category": "스포츠"
        }
        
        response = client.post('/posts/newpost', json.dumps(newpost), **header, content_type='application/json')
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), {"MESSAGE": "MUST CONTAIN WORDS"})
    
    def test_create_newpost_post_content_too_short(self):
        client  = Client()
        header  = {"HTTP_Authorization" : self.token2}
        token   = header["HTTP_Authorization"]
        payload = jwt.decode(token, SECRET_KEY, algorithms = ALGORITHM)
        user    = User.objects.get(id = payload['id'])
        
        newpost = {
            "id"     : 4,
            "title"  : "title for post1",
            "content": "tooshort",
            "author" : User.objects.get(id = user.id).id,
            "category": "스포츠"
        }
        
        response = client.post('/posts/newpost', json.dumps(newpost), **header, content_type='application/json')
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), {"MESSAGE": "NEED_MORE_THAN_10_WORDS"})
    
    def test_create_newpost_post_content_category_not_exist(self):
        client  = Client()
        header  = {"HTTP_Authorization" : self.token2}
        token   = header["HTTP_Authorization"]
        payload = jwt.decode(token, SECRET_KEY, algorithms = ALGORITHM)
        user    = User.objects.get(id = payload['id'])
        
        newpost = {
            "id"     : 4,
            "title"  : "title for post1",
            "content": "tooshort",
            "author" : User.objects.get(id = user.id).id,
            "category": "스리랑카"
        }
        
        response = client.post('/posts/newpost', json.dumps(newpost), **header, content_type='application/json')
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), {"MESSAGE": "CATEGORY DOES NOT EXIST"})
    

    def test_post_delete_success(self):
        client  = Client()
        header  = {"HTTP_Authorization" : self.token1}
        
        response = client.delete('/posts/post/manage/1', **header)
        self.assertEqual(response.status_code, 204)
    
    def test_post_delete_does_not_exist(self):
        client  = Client()
        header  = {"HTTP_Authorization" : self.token1}
        
        response = client.delete('/posts/post/manage/111', **header)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), {"MESSAGE": "POST DOES NOT EXIST"})
    
    def test_post_delete_invalid_user(self):
        client  = Client()
        header  = {"HTTP_Authorization" : self.token2}
        
        response = client.delete('/posts/post/manage/1', **header)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.json(), {"MESSAGE": "INVALID USER"})
    
    def test_post_update_success(self):
        client  = Client()
        header  = {"HTTP_Authorization" : self.token1}
        
        update_post = {
            "title": "update peter's post1",
            "content": "update peter's title",
        }

        response = client.patch('/posts/post/manage/1', json.dumps(update_post), **header, content_type="application/json")
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json(), {"MESSAGE": "SUCCESSFULLY UPDATED"})
    
    def test_post_update_content_no_word(self):
        client  = Client()
        header  = {"HTTP_Authorization" : self.token1}
        
        update_post = {
            "title": "update peter's post1",
            "content": "   ",
        }

        response = client.patch('/posts/post/manage/1', json.dumps(update_post), **header, content_type="application/json")
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), {"MESSAGE": "MUST CONTAIN WORDS"})
    
    def test_post_update_content_too_short(self):
        client  = Client()
        header  = {"HTTP_Authorization" : self.token1}
        
        update_post = {
            "title": "update peter's post1",
            "content": "tooshort",
        }

        response = client.patch('/posts/post/manage/1', json.dumps(update_post), **header, content_type="application/json")
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), {"MESSAGE": "NEED_MORE_THAN_10_WORDS"})
    
    def test_post_update_title_no_word(self):
        client  = Client()
        header  = {"HTTP_Authorization" : self.token1}
        
        update_post = {
            "title": "    ",
            "content": "update peter's title",
        }

        response = client.patch('/posts/post/manage/1', json.dumps(update_post), **header, content_type="application/json")
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), {"MESSAGE": "TITLE MUST CONTAIN WORDS"})
    
    def test_post_update_post_not_exist(self):
        client  = Client()
        header  = {"HTTP_Authorization" : self.token1}
        
        update_post = {
            "title": "update peter's post1",
            "content": "update peter's title",
        }

        response = client.patch('/posts/post/manage/111', json.dumps(update_post), **header, content_type="application/json")
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), {"MESSAGE": "POST DOES NOT EXIST"})
    
    def test_post_update_jsondecodeerror(self):
        client  = Client()
        header  = {"HTTP_Authorization" : self.token1}
        
        response = client.patch('/posts/post/manage/1', **header)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {"message": "INVALID DATA FORMAT"})
    
    def test_post_update_invalid_user(self):
        client  = Client()
        header  = {"HTTP_Authorization" : self.token2}
        
        update_post = {
            "title": "update peter's post1",
            "content": "hihihihihihihi",
        }

        response = client.patch('/posts/post/manage/1', json.dumps(update_post),**header, content_type="application/json")
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), {"MESSAGE": "INVALID USER"})
    
    def test_postdetail_get_success(self):
        client = Client()
        response = client.get('/posts/post/1')

        written = Post.objects.get(id=1).created_at.strftime('%Y.%m.%d %H:%M')

        test = {
            "RESULT": {
                "title"   : "title for post1",
                "author"  : "peter",
                "content" : "this is peter's post",
                "user_id" : 1,
                "written" : written,
                "view_count": 1,
                "category_id": 1,
                "category": "유머"
            }
        }
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), test)
    
    def test_postdetail_get_post_not_exist(self):
        client = Client()
        response = client.get('/posts/post/111')

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), {"MESSAGE": "POST DOES NOT EXIST"})
    
    def test_postlist_get_success(self):
        client = Client()
        response = client.get('/posts/main')
        written1 = Post.objects.get(id=1).created_at.strftime('%Y.%m.%d %H:%M')
        written2 = Post.objects.get(id=2).created_at.strftime('%Y.%m.%d %H:%M')
        written3 = Post.objects.get(id=3).created_at.strftime('%Y.%m.%d %H:%M')
        
        test = {
            "RESULT": {
                "data":[
                    {
                        "title": "title for post3",
                        "author": "peter",
                        "written": written3,
                        "post_id": 3,
                        "user_id": 1,
                        "view_count": 0,
                        "category_id": 3,
                        "category": "스포츠"
                    },
                    {
                        "title": "title for post2",
                        "author": "peter",
                        "written": written2,
                        "post_id": 2,
                        "user_id": 1,
                        "view_count": 0,
                        "category_id": 2,
                        "category": "시사"
                    },
                    {
                        "title": "title for post1",
                        "author": "peter",
                        "written": written1,
                        "post_id": 1,
                        "user_id": 1,
                        "view_count": 0,
                        "category_id": 1,
                        "category": "유머"
                    }
                ],
                "post_count": 3,
            }
        }

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), test)

    def test_postlist_get_page_number_negative(self):
        client = Client()
        response = client.get('/posts/main?page=-2')
        
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), {"MESSAGE": "MUST START WITH GREATER THAN 0"})

    def test_search_no_word(self):
        client = Client()
        header = {"HTTP_Authorization": self.token1}

        search_target = {
            "title"      : "주간 스포츠",
            "author"     : "가나다",
            "written"    : "2021.11.02 13:00",
            "post_id"    : 1,
            "user_id"    : 1,
            "category"   : "스포츠",
            "category_id": 3,
            "view_count" : 3
        }

        response = client.patch('/posts/post/search', json.dumps(search_target), **header,
                                content_type="application/json")
        self.assertEqual(response.status_code, 405)
        self.assertEqual(response.json(), {"MESSAGE": "MUST CONTAIN WORDS"})

    def test_search_not_exist(self):
        client = Client()
        header = {"HTTP_Authorization": self.token1}

        search_target = {
            "title"      : "주간 스포츠",
            "author"     : "가나다",
            "written"    : "2021.11.02 13:00",
            "post_id"    : 1,
            "user_id"    : 1,
            "category"   : "스포츠",
            "category_id": 3,
            "view_count" : 3
        }

        response = client.patch('/posts/post/search', json.dumps(search_target), **header,
                                content_type="application/json")
        self.assertEqual(response.status_code, 405)
        self.assertEqual(response.json(), {"MESSAGE": "SEARCH DOES NOT EXIST"})
    def test_comments_post_success(self):
        client = Client()
        headers  = {'HTTP_Authorization': self.token1}
        body = {
            'content' : '안녕하세요'
        }

        response = client.post('/posts/1/comment', json.dumps(body), content_type='application/json', **headers)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json(), {
            "MESSAGE":"COMMENT_SUCCESS"
        })

    def test_comments_post_fail(self):
        client = Client()
        headers  = {'HTTP_Authorization': self.token1}
        body = {
            'contentsss' : '안녕하세요!!!'
        }
        response = client.post('/posts/2/comment', json.dumps(body), content_type='application/json', **headers)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {
            "MESSAGE": "KEY_ERROR"
        })
    def test_comments_post_not_comment_fail(self):
        client = Client()
        headers  = {'HTTP_Authorization': self.token1}
        body = {
            "content" : ""
        }
        response = client.post('/posts/1/comment',json.dumps(body), content_type='application/json', **headers)
        self.assertEqual(response.json(),
            {
                "MESSAGE": "NOT_COMMENT"
                }
        )
        self.assertEqual(response.status_code, 400)

    def test_comments_ppst_invalid_posting_fail(self):
        client = Client()
        headers  = {'HTTP_Authorization': self.token2}
        body = {
            "content" : "하나둘"
        }
        response = client.post('/posts/5/comment',json.dumps(body), content_type='application/json', **headers)
        self.assertEqual(response.json(),
            {
                "MESSAGE": "INVALID_POSTING"
                }
        )
        self.assertEqual(response.status_code, 400)
    def test_comments_get_success(self):
        client = Client()
        response = client.get('/posts/1/comment')
        written1 = Comment.objects.get(id=1).created_at.strftime('%Y.%m.%d %H:%M')
        written2 = Comment.objects.get(id=2).created_at.strftime('%Y.%m.%d %H:%M')
        written3 = Comment.objects.get(id=3).created_at.strftime('%Y.%m.%d %H:%M')

        test={
            "COMMENT": [
                {
                    "id"            : 1,
                    "post_id"       : 1,
                    "name"          : "peter",
                    "content"       : "하이요",
                    "created_at"    : written1,
                    "parent_comment": [
                        {
                            "id": 2,
                            "parent_comment_id": 1,
                            "name": "peter",
                            "content": "바이요",
                            "created_at": written2
                        },
                        {
                            "id": 3,
                            "parent_comment_id": 1,
                            "name": "peter",
                            "content": "안녕",
                            "created_at": written3
                        }
                    ]
                }
            ]
        }
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), test)

    def test_comments_get_no_post_fail(self):
        client = Client()
        response = client.get('/posts/4/comment')
        self.assertEqual(response.json(),
            {
                "MESSAGE": "NOT_EXISTS"
                }
        )
        self.assertEqual(response.status_code, 404)
        
    
    def test_comments_patch_success(self):
        client = Client()
        headers  = {'HTTP_Authorization': self.token1}
        body = {
            "content" : "안녕히가세요"
        }
        response = client.patch('/posts/comment/1',json.dumps(body), content_type='application/json', **headers)
        self.assertEqual(response.json(),
            {
                "MESSAGE": "UPDATE_SUCCESS"
                }
        )
        self.assertEqual(response.status_code, 200)

    def test_comments_patch_not_exists_fail(self):
        client = Client()
        headers  = {'HTTP_Authorization': self.token1}
        body = {
            "content" : '오하이요'
        }
        response = client.patch('/posts/comment/5',json.dumps(body), content_type='application/json', **headers)
        self.assertEqual(response.json(),
            {
                "MESSAGE": "NOT_EXISTS"
                }
        )
        self.assertEqual(response.status_code, 400)

    def test_comments_patch_Key_error_fail(self):
        client = Client()
        headers  = {'HTTP_Authorization': self.token1}
        body = {
            "contents" : '오하이요'
        }
        response = client.patch('/posts/comment/1',json.dumps(body), content_type='application/json', **headers)
        self.assertEqual(response.json(),
            {
                "MESSAGE": "KEY_ERROR"
                }
        )
        self.assertEqual(response.status_code, 400)

    def test_comments_patch_not_comment_fail(self):
        client = Client()
        headers  = {'HTTP_Authorization': self.token1}
        body = {
            "content" : ""
        }
        response = client.patch('/posts/comment/5',json.dumps(body), content_type='application/json', **headers)
        self.assertEqual(response.json(),
            {
                "MESSAGE": "NOT_COMMENT"
                }
        )
        self.assertEqual(response.status_code, 400)

    def test_comments_delete_success(self):
        client = Client()
        headers  = {'HTTP_Authorization': self.token1}
        response = client.delete('/posts/comment/1', **headers)
        self.assertEqual(response.json(),
            {
                "MESSAGE": "DELETE_SUCCESS"
                }
        )
        self.assertEqual(response.status_code, 200)

    def test_comments_delete_not_exists_fail(self):
        client = Client()
        headers  = {'HTTP_Authorization': self.token1}
        response = client.delete('/posts/comment/5', **headers)
        self.assertEqual(response.json(),
            {
                "MESSAGE": "INVALID_COMMENT"
                }
        )
        self.assertEqual(response.status_code, 404)
