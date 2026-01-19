<div align="center">
<picture>
<source media="(prefers-color-scheme: dark)" srcset="https://s3.bmp.ovh/imgs/2026/01/10/91c0f891ee56c72e.png">
<img src="https://s3.bmp.ovh/imgs/2026/01/10/4a3a90eb41e5275b.png">
</picture>
<br>
<img src="https://img.shields.io/badge/Python-3776AB?style=flat&logo=Python&logoColor=ffffff">
<img src="https://img.shields.io/github/license/Wangs-official/CodemaoEDUTools.svg">
<img src="https://img.shields.io/github/stars/Wangs-official/CodemaoEDUTools.svg?style=social&label=Star&maxAge=2592000">
<a href="https://shequ.codemao.cn/user/1458227103"><img src="https://img.shields.io/badge/关注WangZixu的编程猫-white"></a><br>

| **📝 项目说明**       | **🖥️ 命令行文档**      | **🧰 函数文档**           | **🔧 开发文档**         | **⚠️ 免责声明**         |
|:-----------------:|:------------------:|:---------------------:|:-------------------:|:-------------------:|
| [点击进入](README.md) | [点击进入](doc/cli.md) | [点击进入](doc/import.md) | [点击进入](doc/code.md) |[点击前往](README.md#-免责声明) |

</div>

## 👋🏻 欢迎使用 CodemaoEDUTools！

全新版本，全新体验，欢迎使用 CodemaoEDUTools V2！

为编程猫社区的”老师“们提供更便捷的API调用方案，且用且珍惜

> [!TIP]
>
> 为了更好的发展，我们已在 2026.01.19 将项目许可证更新为 **Apache 2.0**
>
> 同时，我们也更新了免责声明，如果开始使用本程序，则默认为你同意免责声明

## 🔧 安装

1. 直接安装：`pip install CodemaoEDUTools`
2. 本地Wheel安装：
   - 在 Relese 界面下载最新的 Wheel 包
   - 使用 `pip install <wheel包路径>` 进行安装
3. 远古方式（这种方式不能使用命令行）：
   - 在 Release 界面下载最新的压缩包
   - 将 **CodemaoEDUTools** 文件夹放入到你的项目里

## 😎 使用

这个程序不仅可以在CLI（命令行）环境中使用，还可以作为一个库被调用

### 在命令行中使用

在安装 CodemaoEDUTools 后，你可以在命令行中直接输入：`cet` 来使用这个工具

例如：`cet version`

当然，你也可以在运行 `uv pip install -e .` 后通过 `uv run CodemaoEDUTools` 来使用这个工具

我们在 2.1.0 版本中将项目管理器变更为了 uv，这意味着你无法像往常那样使用CET了

### 作为库调用

在安装 CodemaoEDUTools 后，你可以在代码中使用：`import CodemaoEDUTools` 来导入这个工具

如果你正在制作分发给他人的程序，请要求对方安装 CodemaoEDUTools

## 📃 文件格式

程序不是活人，所以你得知道文件格式

### Token 文件格式

每行一个 Token，纯文本格式，无后缀名要求，建议设置为 `tokens.txt`

### 表格文件格式

批量登录 EDU 账号时，程序需要一个包含账号密码的表格，这个表格可以由 `MergeStudentXls()` 函数生成

不要带标题，直接就是 **账号名-账号-密码**，下面这个表格一看就知道了：

| {账号名} | {账号} | {密码} |
|:-----:|:----:|:----:|
| {账号名} | {账号} | {密码} |

仅接受 `.xlsx` 后缀文件

## 👍🏻 程序默认值

程序默认值在 `__init__.py` 内，有注释说明。由于是旧时代的产物，没有办法在直接安装时自定义，之后会加上的

只有 CLI 才能使用程序默认值

## 📂 版本更新/分支

- `main` 主分支，在此分支的代码为最新版本代码，会自动生成 Wheel 包以及压缩包
- `dev` 分支是开发分支，如果你要对本程序进行开发，请在此分支进行
- `old` 分支为极早之前的版本，现已不再更新

我们会定期合并 `dev` 分支到 `main` 分支，以完成更新

## ⚠️ 免责声明



## 😇 感谢以下项目的支持！

给我和他们一个 **⭐Star️** 哦

[Aumiao](https://github.com/Aurzex/Aumiao)

[CodemaoLV5](https://github.com/Wangs-official/CodemaoLV5)

[编程猫API文档](https://api.docs.codemao.work/)

本项目是以下项目的改体：

- CodemaoCommunityHistory/CodemaoEduAutoReg
- CodemaoCommunityHistory/CodemaoPL

## ❤️ 感谢各位贡献者

<a href="https://github.com/wangs-official/codemaoedutools/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=wangs-official/codemaoedutools" />
</a><br/><br/>

> *結ばれた絆に 裏切ることない愛情 を*
> 
> *为相连的牵绊 带来了永不背叛的爱情*
>
> 《LOVETOXIN》- https://music.163.com/song?id=2077776113