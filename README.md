# 프리온보드 [ASSIGNMENT1] 

## ✨ 배포(Base URL)

http://3.143.24.251:8000

<br>

---

## ✨ 멤버

이무현, 김훈태, 안다민

<br>

---

## ✨ 사용 스택
- **`mongodb atlas`**, **`django`**

<br>

---

## ✨ endpoints
| **METHOD** | **ENDPOINT**   | **body**   | **수행 목적** |
|:------|:-------------|:-----------------------:|:------------|
| POST   | /users/register | email, name, password | 회원가입    |
| POST   | /users/signin  | email, password       | 로그인        |
| POST    | /posts/newpost | title, content      | 게시글 작성 |
| GET   | /posts/main        |                   | 게시글 리스트   |
| GET    | /posts/post/<post_id>|                        | 게시글 보기 |
| PATCH  | /posts/post/manage/<post_id> | title, content | 게시글 수정 |
| DELETE | /posts/post/manage/<post_id> |               | 게시글 삭제 |
|  GET   | /posts/post/search          |                | 기능 별 검색 |
| POST | posts/<post_id>/comment | content, parent_comment_id | 대댓글작성 |
| GET | posts/<post_id>/comment |                           | 대댓글조회 |
| PATCH | posts/comment/<comment_id>| content              | 대댓글수정 |
| DELETE | posts/comment/<comment_id> |                    | 대댓글삭제 |

<br>

---

### 1. 회원가입

- endpoint: http://3.143.24.251:8000/users/register
- METHOD: POST

| **이름**       | **data type**  | **body input**                          | **처리**|
|:----------|--------|----------------------------|------------------------|
| name     | string | "name" : "peter"            | 영문/한글 2-30글자 사이의 값 입력 |
| email    | string | "email" : "dissgogo@gmail.com" | "@"와 "."을 기준으로 그 사이 2-3글자 포함|
| password | string | "password" : "dlangus123!"   | 영문/한글, 숫자, 특수문자를 각각 하나 이상 포함한 10-20글자 |

<br>

**SUCCESS EXAMPLE**
```
{
'MESSAGE':'SUCCESSFULLY REGISTERED'
}
```
**ERROR EXAMPLE**
```
# body의 일부 미입력 시
{
  'MESSAGE':'KEY_ERROR'
}
```
```
# body 자체가 없을 시
{
  'MESSAGE':'VALUE_ERROR'
}
``` 

---

### 2. 로그인

- endpoint: http://3.143.24.251:8000/users/signin
- METHOD: POST

| **이름**       | **data type**  | **body input**     | **처리**|
|:----------|--------|----------------------------|------------------------|
| email    | string | "email" : "dissgogo@gmail.com" | "@"와 "."을 기준으로 그 사이 2-3글자 포함|
| password | string | "password" : "dlangus123!"   | 영문/한글, 숫자, 특수문자를 각각 하나 이상 포함한 10-20글자 |

**SUCCESS EXAMPLE**
```
# 로그인 성공(200)
{
  "MESSAGE"   : "SUCCESS",
  "user_name" : "peter", // 로그인한 유저명 반환
  "auth_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6Mn0.OsMsy8bfdW_gIJetsU2-FjfeeBd5uaiIG2V92ThJiWA", // jwt 토큰
}
```

**ERROR EXAMPLE**
```
# body 일부 미입력 시(400)
{
  "MESSAGE": "KEY_ERROR"
}
```
```
# body 없을 시(400)
{
  "MESSAGE": "VALUE_ERROR"
}
```
```
# 가입된 이메일 존재하지 않을 시(403)
{
  "message": "EMAIL_DOES_NOT_EXISTS"
}
```
```
# 비밀번호가 일치하지 않을 시(403)
{
  "message": "INVALID_PASSWORD"
}
```

<br>

---

### 3. 게시글 작성
- endpoint: http://3.143.24.251:8000/posts/newpost
- METHOD: POST

| **이름**       | **data type**  | **body input**   | **처리**|
|:----------|:--------:|:----------------------------|:------------------------|
| title    | string | "title" : "post1's title is here" | 글자를 하나 이상 포함해야 한다(공백 불가) |
| content | string | "content" : "content of the post1"   | 글자를 하나 이상 포함해야 하며, 공백 제외 11글자 이상 작성|
| category | string | "category": "유머", "시사", "스포츠" 중 선택 | 유머, 시사, 스포츠 중 한 가지를 입력, 이외에는 에러 처리|

**SUCCESS EXAMPLE**
```
# 생성 성공 시(201)
{
  "MESSAGE": "SUCCESS"
}
```
**ERROR EXAMPLE**
```
# body 일부 미입력 시(400)
{
  'MESSAGE':'KEY_ERROR'
}
```
```
# body 미입력 시(400)
{
  "message": "INVALID DATA FORMAT"
}
```
```
# title 공백만 있고 글자 없을 시(404)
{
  "MESSAGE": "TITLE MUST CONTAIN WORDS"
}
```
```
# content(본문) 공백만 있고 글자 없을 시(404)
{
  {"MESSAGE": "MUST CONTAIN WORDS"}
}
```
```
# content의 길이가 공백 제외 10글자 이하일 시(404)
{
  "MESSAGE": "NEED_MORE_THAN_10_WORDS"
}
```
```
# 존재하지 않는 category 입력 시
{
    "MESSAGE": "CATEGORY DOES NOT EXIST"
}
```

<br>

---

### 4. 게시글 리스트 조회
- endpoint: http://3.143.24.251:8000/posts/main
- METHOD: GET

| **이름**       | **data type**  | **endpoint**   | **처리**|
|:----------|:--------:|:----------------------------|:------------------------|
| page    | string |  posts/main?page=1 | page 위치를 int형으로 입력받는다. 미입력 시 자동으로 1, 0 이하의 숫자 받으면 에러처리 |
  
- page를 query parameter로 전달 받으면 LIMIT을 통해 한 페이지 당 20개의 게시물을 보여줄 수 있게끔 구현

**SUCCESS EXAMPLE**
```
{
    "RESULT": {
        "data": [
            {
                "title": "testtitle2dasd",
                "author": "jack",
                "written": "2021.11.03 04:08",
                "post_id": 3,
                "user_id": 2
                "view_count": 0,
                "category_id": 3,
                "category": "스포츠"
            },
            {
                "title": "타이틀만 수정해보는중입니다1",
                "author": "peter",
                "written": "2021.11.03 04:08",
                "post_id": 1,
                "user_id": 1
                "view_count": 0,
                "category_id": 2,
                "category": "시사"
            }
        ],
        "post_count": 2 // 포스트 개수 카운트하여 전달 
    }
}
```
**ERROR EXAMPLE**
```
# query parameter가 0 또는 음수가 전달되었을 시(404)
{
  "MESSAGE": "MUST START WITH GREATER THAN 0"
}
```
---

### 5. 게시글 상세 조회
- endpoint: http://3.143.24.251:8000/posts/post/1
- METHOD: GET

| **이름**       | **data type**  | **endpoint**   | **처리**|
|:----------|:--------:|:----------------------------|:------------------------|
| post_id    | string |  posts/post/1 | path parameter로 post_id을 전달받아서 게시글이 존재하는 지 파악한 후 있으면 반환 |

- 중복 조회수 제거: 쿠키를 사용하여 hits: |1|2| 와 같은 방법으로 사용자에게 방문한 게시글의 id를 쿠키에 붙여서 반환함.
- 쿠키 사용 이유: 중복 제거에는 ip, local strage 등 여러 기법이 존재하지만 db 하중이 가장 적다고 판단한 쿠키를 사용하였음.
- 쿠키는 자정이 지나면 사라지며 다시 조회수를 올리는 것이 가능함.

**SUCCESS EXAMPLE**
```
{
    "RESULT": {
        "title": "타이틀만 수정해보는중입니다1", // 게시글 제목
        "author": "peter", // 작성자
        "user_id": 1, // 작성자 id
        "content": "dasdasdasdasd", // 게시글 내용
        "written": "2021.10.20 18:27" // 작성 시간
        "view_count": 1, // 조회수
        "category_id": 1, 
        "category": "유머" // 카테고리 명
    }
}
```
**ERROR EXAMPLE**
```
# 게시글이 존재하지 않을 시(404)
{
  "MESSAGE": "POST DOES NOT EXIST"
}
```

<br>

---

### 6. 게시글 수정
- endpoint: http://3.143.24.251:8000/posts/post/manage/1
- METHOD: PATCH

| **이름**       | **data type**  | **endpoint**   | **처리**|
|:----------|:--------:|:----------------------------|:------------------------|
| post_id   | string |  posts/post/manage/1 | path parameter로 post_id을 전달받아서 게시글이 존재하는 지 파악한 후 있으면  |
| title | string | "title": "hi this is updated post"| 타이틀을 수정할 경우 공백을 제외한 글자가 존재하여야 한다 |
| content | string |"content": "hi this is new post content"| 본문을 수정할 경우 공백을 제외한 글자가 11글자 이상 존재하여야 한다|

- PATCH METHOD 사용
- title, content 둘 중 하나만 body에 실어보내도 된다. (title, content 중 하나 선택하여 수정하거나 모두 수정 가능)

**SUCCESS EXAMPLE**
```
# 성공적으로 수정 시(201)
{
  "MESSAGE": "SUCCESSFULLY UPDATED"
}
```

**ERROR EXAMPLE**
```
# body 없을 시(400)
{
  "message": "INVALID DATA FORMAT"
}
```
```
# 해당 게시글이 존재하지 않을 시(404)
{
  "MESSAGE": "POST DOES NOT EXIST"
}
```
```
# 권한이 없는 사용자가 수정하려 할 시(404)
{
  "MESSAGE": "INVALID USER"
}
```
```
# title이 공백만 있고 글자가 없을 시(404)
{
  "MESSAGE": "TITLE MUST CONTAIN WORDS"
}
```
```
# content가 공백만 있고 글자가 없을 시(404)
{
  "MESSAGE": "MUST CONTAIN WORDS"
}
```
```
# content가 공백 제외 10글자 이하일 시(404)
{
  "MESSAGE": "NEED_MORE_THAN_10_WORDS"
}
```

---
 
### 7. 게시글 삭제
- endpoint: http://3.143.24.251:8000/posts/post/manage/1
- METHOD: DELETE

| **이름**       | **data type**  | **endpoint**   | **처리**|
|:----------|:--------:|:----------------------------|:------------------------|
| post_id    | string |  posts/post/manage/1 | path parameter로 post_id을 전달받아서 게시글이 존재하는 지 파악한 후 있으면 삭제 |

- delete METHOD 사용

**SUCCESS EXAMPLE**
```
# 성공 시(204)
{
  "MESSAGE": "SUCCESSFULLY DELETED"
}
```
**ERROR EXAMPLE**
```
# 해당 게시글이 없을 시(404)
{
  "MESSAGE": "POST DOES NOT EXIST"
}
```
```
# 권한없는 사용자가 삭제하려 할 시(404)
{
  "MESSAGE": "INVALID USER"
}
```
### 8. 검색 기능
- endpoint: http://3.143.24.251:8000/posts/post/search?search-type=author&search=peter
- METHOD: GET

| **이름**       | **data type**  | **endpoint**   | **처리**|
|:----------|:--------:|:----------------------------|:------------------------|
| search-type    | string |  posts/post/search?search-type='' | query parameter로 검색 대주제를 입력, all = 전체, author = 작가명, category = 카테고리 명, title_content = 제목 + 내용 |
| search | string |posts/post/search?search-type=''&search='' | query parameter로 검색 대주제에 따른 검색어를 입력 |

**Example**
```
# 검색어에 해당하는 내용이 있을 시 
{
    "MESSAGE": [
        {
            "title": "testtitle1ㅇㅁㄴ",
            "author": "peter",
            "written": "2021.11.02 15:31",
            "post_id": 7,
            "user_id": 1,
            "category": "스포츠",
            "category_id": 3,
            "view_count": 0
        }
    ],
    "posts_count": 1
}
```
```
# 검색에 부합하는 내용이 없을 시 
{
    "RESULT": []
}
```

### 9. 대댓글 
- Endpoint

| **METHOD** | **ENDPOINT**   | **body**   | **수행 목적** |
|:------|:-------------|:-----------------------:|:------------|
| POST | posts/<post_id>/comment | content, parent_comment_id | 대댓글작성 |
| GET | posts/<post_id>/comment |                           | 대댓글조회 |
| PATCH | posts/comment/<comment_id>| content              | 대댓글수정 |
| DELETE | posts/comment/<comment_id> |                    | 대댓글삭제 |

#### 대댓글 작성
- endpoint : http://3.143.24.251:8000/posts/<post_id>/comment

**SUCCESS EXAMPLE**
```
{
  "MESSAGE": "COMMENT_SUCCESS"
}
```
**ERROR EXAMPLE**
```
#body 일부 미입력(400)
{
"MESSAGE": "KEY_ERROR"
}
```
```
# Post_id 가 없을때 (404)
{
  "MESSAGE": "INVALID_POSTING"
}
```
```
# 빈값일때(400)
{
 "MESSAGE": "NOT_COMMENT"
}
```
#### 대댓글 조회
- endpoint : http://3.143.24.251:8000/posts/<post_id>/comment?page=1
page를 query parameter로 전달 받으면 LIMIT을 통해 한 페이지 당 3개의 게시물을 보여줄 수 있게끔 구현

**SUCCESS EXAMPLE**
```
{
"COMMENT": [
    {
      "id": 1, // 댓글 Id
      "post_id": 1,
      "name": "김훈태", //작성자 이름
      "content": "하이요", //댓글 내용
      "created_at": "2021.11.02 08:30", //작성시간
      "parent_comment": [ // 대댓글
        {
          "id": 2,
          "parent_comment_id": 1, // 부모 댓글 id
          "name": "김태훈" , //작성자 이름
          "content": "바이요", //대댓글 내용
          "created_at": "2021.11.02 08:52" //작성시간
        }
	]
}
```
**ERROR EXAMPLE**
```
# Pagination 파라미터가 0보다 작을때
{
  "MESSAGE": "MUST START WITH GREATER THAN 0" // 404
}
```
```
# Post_id 가 없을때 (404)
{
  "MESSAGE": "NOT_EXISTS"
}
```

#### 대댓글 수정
- endpoint : http://3.143.24.251:8000/posts/comment/<comment_id>

**SUCCESS EXAMPLE**
```
# 성공(200)
{
  "MESSAGE": "UPDATE_SUCCESS"
}
```
**ERROR EXAMPLE**
```
# body 일부 미입력(400)
{
  "MESSAGE": "KEY_ERROR"
}
```
```
# comment_id 가 없을때 (404)
{
  "MESSAGE": "NOT_EXISTS"
}
```
```
# 빈값일때(400)
{
  "MESSAGE": "NOT_COMMENT"
}
```
#### 대댓글 삭제
- endpoint : http://3.143.24.251:8000/posts/comment/<comment_id> 

**SUCCESS EXAMPLE**
```
# 성공(200)
{
  "MESSAGE": "DELETE_SUCCESS"
}
```
**ERROR EXAMPLE**
```
# comment_id 가 없을때 (404)
{
  "MESSAGE": "INVALID_COMMENT"
}
```
