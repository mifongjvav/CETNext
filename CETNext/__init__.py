"""
CETNext
==================================
作者: Argon
GitHub: https://github.com/mifongjvav/CETNext

欢迎使用 CETNext!
这是一个Python包，你可以使用 import CETNext 来导入它

开发者不对您使用本项目造成的风险负责，请自行考虑是否使用，谢谢！
"""
# 版权所有 (C) 2026 Argon
# 根据 Apache 2.0 许可证发布
#
# 修改声明：
# 本文件基于原作者 WangZixu（2025）的作品修改而来。
# 主要修改内容：
# 将原有的 argparse CLI 完全重写为 click 库实现
# 添加 @click.group() 主命令组及所有子命令装饰器
# 使用 click.option 和 click.pass_context 替代 argparse.ArgumentParser
# 将全局参数 --token-file 通过上下文对象传递给子命令
# 修改 __main__.py 入口调用方式
# 加入新功能
# 新增功能：支持用户搜索
# 修改日期：2026-06-21

from importlib.metadata import version, PackageNotFoundError

try:
    __version__ = version("CETNext")
except PackageNotFoundError:
    __version__ = "1.2.1"
__author__ = "Argon"
__description__ = "为编程猫社区的“老师”们提供更便捷的API调用方案，且用且珍惜"

# 线程配置
max_workers = 8

# 举报配置
report_readtoken_line = 20

# 学生名字列表
student_names = [
    "xvbnmklq",
    "asdfghjk",
    "qwertyui",
    "zxcvbnml",
    "poiuytre",
    "lkjhgfds",
    "mnbvcxza",
    "plokmijn",
    "uhbygvtd",
    "crfvtgby",
    "edcrfvtg",
    "qazwsxed",
    "rfvtgbyh",
    "nujmikol",
    "zxasqwde",
    "plmnkoij",
    "bvcdxsza",
    "qwermnbp",
    "asxcvgfr",
    "lpoikmju",
    "yhnujmik",
    "tgbzdxew",
    "rfvgyhuj",
    "edcwsxqa",
    "zaqxswcd",
    "vfrcdews",
    "bgtnhyuj",
    "mkiopluj",
    "nhybtgvr",
    "cdexswza",
    "qwerfdsa",
    "zxcvfdsa",
    "poiuytrw",
    "lkjhgfda",
    "mnbvcxzs",
    "asdfqwer",
    "zxcvqwer",
    "poiulkjh",
    "mnbvcxas",
    "qwertzui",
    "yxcvbnmq",
    "plokmnji",
    "uhbgyvft",
    "crfvtgyn",
    "edcrfvbg",
    "qazwsxrf",
    "rfvtgbyu",
    "nujmiklp",
    "zxasqwed",
    "plmnkoji",
    "bvcdxsaz",
    "qwermnbo",
    "asxcvfgd",
    "lpoikmjn",
    "yhnujmki",
    "tgbzdxec",
    "rfvgyhuk",
    "edcwsxqz",
    "zaqxswce",
    "vfrcdewa",
    "bgtnhyum",
    "mkioplun",
    "nhybtgvf",
    "cdexswzb",
    "qwerfdsz",
    "zxcvfdsz",
    "poiuytrq",
    "lkjhgfdz",
    "mnbvcxzc",
    "asdfqwez",
    "zxcvqwez",
    "poiulkjm",
    "mnbvcxaq",
    "qwertzuy",
    "yxcvbnmr",
    "plokmnjh",
    "uhbgyvfr",
    "crfvtgyb",
    "edcrfvbn",
    "qazwsxre",
    "rfvtgbyi",
    "nujmiklj",
    "zxasqweg",
    "plmnkojh",
    "bvcdxsay",
    "qwermnbu",
    "asxcvfgh",
    "lpoikmjh",
    "yhnujmko",
    "tgbzdxer",
    "rfvgyhun",
    "edcwsxqv",
    "zaqxswec",
    "vfrcdewq",
    "bgtnhyup",
    "mkiopluh",
    "nhybtgvc",
    "cdexswzg",
    "qwerfdsx",
    "zxcvfdsx",
]

# 请在创建新功能后更新此处！

_LAZY_IMPORTS = {
    # API
    "PostAPI": (".api", "PostAPI"),
    "PostWithoutTokenAPI": (".api", "PostWithoutTokenAPI"),
    "PostEduAPI": (".api", "PostEduAPI"),
    "GetAPI": (".api", "GetAPI"),
    "GetWithoutTokenAPI": (".api", "GetWithoutTokenAPI"),
    "PutAPI": (".api", "PutAPI"),
    "DeleteAPI": (".api", "DeleteAPI"),
    # 用户
    "GetUserToken": (".user", "GetUserToken"),
    "CheckToken": (".user", "CheckToken"),
    "SignatureUser": (".user", "SignatureUser"),
    "FollowUser": (".user", "FollowUser"),
    # 作品
    "GetUserWork": (".work", "GetUserWork"),
    "GetStudioWork": (
        ".work",
        "GetStudioWork",
    ),
    "LikeWork": (".work", "LikeWork"),
    "CollectionWork": (".work", "CollectionWork"),
    "ReportWork": (".work", "ReportWork"),
    "SendReviewToWork": (".work", "SendReviewToWork"),
    "TopReview": (".work", "TopReview"),
    "UnTopReview": (".work", "UnTopReview"),
    "ViewWork": (".work", "ViewWork"),
    "ForkWork": (".work", "ForkWork"),
    # CodemaoEDU
    "CreateClassOnEdu": (".edu", "CreateClassOnEdu"),
    "CreateStudentOnEdu": (".edu", "CreateStudentOnEdu"),
    "MergeStudentXls": (".edu", "MergeStudentXls"),
    "LoginUseEdu": (".edu", "LoginUseEdu"),
    # 搜索用户
    "search_user": (".search_user", "search_user"),
    "download_user_list": (".search_user", "download_user_list"),
}

# 请在创建新功能后更新此处！导入控制
__all__ = [
    # 配置
    "__version__",
    "__author__",
    "__description__",
    "max_workers",
    "student_names",
    "report_readtoken_line",
    # API
    "PostAPI",
    "PostWithoutTokenAPI",
    "PostEduAPI",
    "GetAPI",
    "GetWithoutTokenAPI",
    "PutAPI",
    "DeleteAPI",
    # 用户
    "GetUserToken",
    "CheckToken",
    "SignatureUser",
    "FollowUser",
    # 作品
    "GetUserWork",
    "GetStudioWork",
    "LikeWork",
    "LikeReview",
    "CollectionWork",
    "ReportWork",
    "SendReviewToWork",
    "TopReview",
    "UnTopReview",
    "ViewWork",
    "ForkWork",
    # CodemaoEDU
    "CreateClassOnEdu",
    "CreateStudentOnEdu",
    "MergeStudentXls",
    "LoginUseEdu",
    # 搜索用户
    "search_user",
    "download_user_list",
]


def __getattr__(name: str):
    if name in _LAZY_IMPORTS:
        module_name, attr_name = _LAZY_IMPORTS[name]
        from importlib import import_module

        module = import_module(module_name, package=__name__)
        value = getattr(module, attr_name)
        globals()[name] = value
        return value
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


def __dir__() -> list[str]:
    return sorted(list(globals().keys()) + list(_LAZY_IMPORTS.keys()))


# 包函数
def get_version() -> str:
    """获取版本号"""
    return __version__


def info() -> str:
    """显示包信息"""
    return f"""
CETNext v{__version__}
作者: {__author__}
GitHub: https://github.com/mifongjvav/CETNext/

导入方式:
    import CETNext
    from CETNext import * # 不推荐

命令行使用:
    python main.py check-token

注意事项:
    请合理使用本工具，遵守编程猫平台的使用规则。
    开发者不对滥用本工具造成的后果负责。
"""


def about() -> str:
    """显示关于信息"""
    return f"""
CETNext v{__version__}
作者: {__author__}
GitHub: https://github.com/mifongjvav/CETNext/
"""
