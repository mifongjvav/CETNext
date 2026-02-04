# 🧰 函数文档

这里是 **CodemaoEDUTools** 函数文档，在此文档中，你可以了解所有已定义的函数

## API 调用函数

这些函数位于 `api.py` 内，用于调用编程猫API

UA 使用 `fake_useragent` 库自动生成

所有的 `Path` 参数均不包含域名，从 `/` 开始

`*API`

### POST 方式调用 API

`PostAPI(Path: str, PostData: dict, Token: str) -> requests.Response`

### POST 方式匿名请求 API

`def PostWithoutTokenAPI(Path: str, PostData: dict) -> requests.Response`

此函数请求时，无需携带令牌

### POST 方式调用教育 API

`PostEduAPI(Path: str, PostData: dict, Token: str) -> requests.Response`

此函数调用的是 `https://eduzone.codemao.cn{Path}"`

### GET 方式调用 API

`GetAPI(Path: str, Token: str) -> requests.Response`

### GET 方式匿名调用 API

`GetWithoutTokenAPI(Path: str) -> requests.Response`

此函数请求时，无需携带令牌

### PUT 方式调用 API

`PutAPI(Path: str, Token: str) -> requests.Response`

## 用户函数

这些函数位于 `user.py` 内，是一些与用户有关的函数

`*User`

### 登录并获取用户 Token

`GetUserToken(Username: str, Password: str) -> str | bool`

### 确定 Token 数量

`CheckToken(Path: str) -> int`

### 签订友好协议

`SignatureUser(Path: str) -> bool`

### 关注用户

`FollowUser(Path: str, UserID: str) -> bool`

## 作品函数

这些函数位于 `work.py` 内，是一些与作品互动的函数

`*Work`

### 获取用户所有的作品

`GetUserWork(UserID: str) -> str | bool`

### 点赞作品

`LikeWork(Path: str, WorkID: str) -> bool`

### 点赞评论

`def LikeReview(Path: str, WorkID: str, CommentID: str) -> bool:`

### 收藏作品

`CollectionWork(Path: str, WorkID: str) -> bool`

### 举报作品

`ReportWork(Path: str, WorkID: str, Reason: str, Describe: str) -> bool`

举报要求参见[此处](cli.md#举报作品)

推荐只输入20个令牌

### 评论作品

`SendReviewToWork(Path: str, WorkID: str, ReviewText: str) -> bool`

### 置顶评论（越权）

`TopReview(Token: str, WorkID: str, CommentID: str) -> bool`

### 取消置顶评论（越权）

`UnTopReview(Token: str, WorkID: str, CommentID: str) -> bool`

### 浏览作品（单刷）

`ViewWork(Token: str, WorkID: str) -> bool`

> [!WARNING]
>
> 编程猫官方已对此API做出限制，具体信息：[点击此处](https://shequ.codemao.cn/community/1645000)

### 再创作作品

`ForkWork(Path: str, WorkID: str) -> bool`

## EDU函数

这些函数位于 `edu.py` 内，是一些关于编程猫教育平台的功能

注：这部分的Token需要从编程猫教育平台（[https://edu.codemao.cn](https://edu.codemao.cn)）抓取，注册请自行寻法

`*EDU`

### 添加新的班级

`CreateClassOnEdu(Token: str, ClassName: str) -> str`

### 添加学生到班级

`CreateStudentOnEdu(Token: str, ClassID: str, StudentNameList: list[str]`

### 合并生成的表格

`MergeStudentXls(InputFolder: str, OutputFile: str) -> bool`

### 登录 EDU 账号

`LoginUseEdu(InputXlsx: str, OutputFile: str, Signature: bool = False) -> bool`
