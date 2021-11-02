# 프리온보드 [ASSIGNMENT1] 

## ✨ 배포(Base URL)

http://3.143.24.251:8000


## ✨ 멤버

이무현, 김훈태, 안다민

<br>

## 사용 스택
- mongodb atlas, python django

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
