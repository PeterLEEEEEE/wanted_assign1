# 프리온보드 [ASSIGNMENT1] 

## ✨ 배포(Base URL)

http://3.143.24.251:8000

<br>

---

## ✨ 멤버

이무현, 김훈태, 안다민

<br>

---

## 사용 스택
- mongodb atlas, python django

<br>

---

## endpoints
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
| POST  | /posts/<int:post_id>/comment|               |     댓글 작성  | 
| GET   | /posts/comment/<comment_id>|                |     댓글 가져오기 |

<br>

---

**1. 회원가입**

endpoint: http://3.143.24.251:8000/users/register

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

**2. 로그인**

endpoint: http://3.143.24.251:8000/users/signin

| **이름**       | **data type**  | **body input**                          | **처리**|
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

**3. 게시글 작성**
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

**4. 게시글 리스트 조회**
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
                "written": "2021.10.21 11:34",
                "post_id": 3,
                "user_id": 2
            },
            {
                "title": "타이틀만 수정해보는중입니다1",
                "author": "peter",
                "written": "2021.10.20 18:27",
                "post_id": 1,
                "user_id": 1
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

**5. 게시글 상세 조회**
| **이름**       | **data type**  | **endpoint**   | **처리**|
|:----------|:--------:|:----------------------------|:------------------------|
| post_id    | string |  posts/post/1 | path parameter로 post_id을 전달받아서 게시글이 존재하는 지 파악한 후 있으면 반환 |
  
**SUCCESS EXAMPLE**
```
{
    "RESULT": {
        "title": "타이틀만 수정해보는중입니다1", // 게시글 제목
        "author": "peter", // 작성자
        "user_id": 1, // 작성자 id
        "content": "dasdasdasdasd", // 게시글 내용
        "written": "2021.10.20 18:27" // 작성 시간
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
