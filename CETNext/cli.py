"""命令行接口"""
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
# 修改日期：2026-06-07
# 新增功能：支持 --wid / --user-id 传入逗号分隔、JSON数组、Python列表格式

import click
import json
import logging
import ast

from . import __version__, student_names
from .user import (
    GetUserToken as _GetUserToken,
    CheckToken as _CheckToken,
    SignatureUser as _SignatureUser,
    FollowUser as _FollowUser,
)
from .work import (
    GetUserWork as _GetUserWork,
    GetStudioWork as _GetStudioWork,
    LikeWork as _LikeWork,
    LikeReview as _LikeReview,
    CollectionWork as _CollectionWork,
    ReportWork as _ReportWork,
    SendReviewToWork as _SendReviewToWork,
    TopReview as _TopReview,
    UnTopReview as _UnTopReview,
    ViewWork as _ViewWork,
    ForkWork as _ForkWork,
    report_readtoken_line as _ReportReadtokenLine,
)
from .edu import (
    CreateClassOnEdu as _CreateClassOnEdu,
    CreateStudentOnEdu as _CreateStudentOnEdu,
    MergeStudentXls as _MergeStudentXls,
    LoginUseEdu as _LoginUseEdu,
)
from .api import set_default_headless

logger = logging.getLogger(__name__)


def _parse_ids(ids_tuple):
    """
    将click的multiple元组解析为ID列表。
    支持以下格式：
    - 多次使用选项：--id 1 --id 2 -> [1,2]
    - 逗号分隔：--id 1,2,3 -> [1,2,3]
    - JSON数组：--id [1,2,3] -> [1,2,3]
    - Python列表：--id ['1','2','3'] -> ['1','2','3']
    """
    if not ids_tuple:
        return []
    # 如果用户多次使用了该选项，直接返回所有值
    if len(ids_tuple) > 1:
        return list(ids_tuple)

    s = ids_tuple[0].strip()
    if not s:
        return []

    # 尝试解析为 Python 列表（支持单引号）
    if s.startswith("[") and s.endswith("]"):
        try:
            parsed = ast.literal_eval(s)
            if isinstance(parsed, list):
                return [str(item) for item in parsed]
        except Exception:
            pass
        # 回退到 JSON 解析（双引号）
        try:
            parsed = json.loads(s)
            if isinstance(parsed, list):
                return [str(item) for item in parsed]
        except Exception:
            pass

    # 尝试按逗号分隔（同时移除每个元素两边的引号）
    if "," in s:
        parts = [p.strip().strip("'\"") for p in s.split(",") if p.strip()]
        if parts:
            return parts

    # 最后作为单个ID
    return [s]


# ------------------------------------------------------------
# 全局上下文，用于存储 --token-file 等公共选项
# ------------------------------------------------------------
@click.group()
@click.option(
    "--token-file",
    "-tf",
    default="tokens.txt",
    help="Token文件路径，用于需要批量Token的命令",
    show_default=True,
)
@click.option(
    "--headless",
    "-hl",
    default=True,
    help="启用无头浏览器模式，但会增加被WAF拦截的概率",
    show_default=True,
)
@click.pass_context
def cli(ctx: click.Context, token_file: str, headless: bool):
    """
    CETNext

    为编程猫社区的“老师”们提供更便捷的API调用方案，且用且珍惜
    """
    set_default_headless(headless)
    ctx.obj = {"token_file": token_file}


# ------------------------------------------------------------
# 用户相关命令
# ------------------------------------------------------------
@cli.command("check-token")
@click.pass_obj
def check_token(obj: dict):
    """查看一个Token文件内有多少个Token（读取行数）"""
    token_file = obj["token_file"]
    count = _CheckToken(token_file)
    click.echo(f"可用Token数量: {count}")


@cli.command("get-token")
@click.option("--username", "-u", required=True, help="用户名（手机号）")
@click.option("--password", "-p", required=True, help="密码")
def get_token(username: str, password: str):
    """登录以获取一个用户的Token"""
    token = _GetUserToken(username, password)
    if token:
        click.echo(token)
    else:
        click.echo("获取Token失败", err=True)
        raise click.Abort()


@cli.command("signature")
@click.pass_obj
def signature(obj: dict):
    """批量签订友好协议（使用Token文件中的所有Token）"""
    token_file = obj["token_file"]
    click.echo("请稍后...")
    if _SignatureUser(token_file):
        click.echo("执行成功")
    else:
        click.echo("执行失败", err=True)
        raise click.Abort()


@cli.command("follow-user")
@click.option(
    "--user-id",
    "-uid",
    required=True,
    multiple=True,
    help="训练师编号（可多次使用，也支持逗号分隔或JSON/Python列表）",
)
@click.pass_obj
def follow_user(obj: dict, user_id: tuple):
    """批量关注一个或多个用户（每个用户使用Token文件中所有Token关注）"""
    token_file = obj["token_file"]
    for uid in _parse_ids(user_id):
        click.echo(f"请稍后，正在执行：{uid}")
        if _FollowUser(token_file, uid):
            click.echo(f"关注 {uid} 执行成功")
        else:
            click.echo(f"关注 {uid} 执行失败", err=True)
            raise click.Abort()


# ------------------------------------------------------------
# 作品相关命令
# ------------------------------------------------------------
@cli.command("get-work")
@click.option(
    "--user-id",
    "-uid",
    required=True,
    multiple=True,
    help="训练师编号（可多次使用，也支持逗号分隔或JSON/Python列表）",
)
def get_work(user_id: tuple):
    """获取一个或多个用户的所有作品ID"""
    for uid in _parse_ids(user_id):
        click.echo(f"请稍后，正在执行：{uid}")
        work_ids = _GetUserWork(uid)
        if work_ids:
            click.echo(f"用户 {uid} 的作品列表：{work_ids} 共 {len(work_ids)} 个")
        else:
            click.echo(f"获取用户 {uid} 作品失败", err=True)


@cli.command("get-studio-work")
@click.option(
    "--studio-id",
    "-sid",
    required=True,
    multiple=True,
    help="工作室编号（可多次使用，也支持逗号分隔或JSON/Python列表）",
)
def get_studio_work(studio_id: tuple):
    """获取一个或多个工作室的所有作品ID"""
    for sid in _parse_ids(studio_id):
        click.echo(f"请稍后，正在执行：{sid}")
        work_ids = _GetStudioWork(sid)
        if work_ids:
            click.echo(f"工作室 {sid} 的作品列表：{work_ids} 共 {len(work_ids)} 个")
        else:
            click.echo(f"获取工作室 {sid} 作品失败", err=True)


@cli.command("like-work")
@click.option(
    "--work-id",
    "-wid",
    required=True,
    multiple=True,
    help="作品ID（可多次使用，也支持逗号分隔或JSON/Python列表）",
)
@click.pass_obj
def like_work(obj: dict, work_id: tuple):
    """批量点赞一个或多个作品（使用Token文件中所有Token）"""
    token_file = obj["token_file"]
    for wid in _parse_ids(work_id):
        click.echo(f"请稍后，正在执行：{wid}")
        if _LikeWork(token_file, wid):
            click.echo(f"点赞 {wid} 执行成功")
        else:
            click.echo(f"点赞 {wid} 执行失败", err=True)
            raise click.Abort()


@cli.command("like-review")
@click.option("--work-id", "-wid", required=True, help="作品ID")
@click.option(
    "--comment-id",
    "-cid",
    required=True,
    multiple=True,
    help="评论ID（可多次使用，也支持逗号分隔或JSON/Python列表）",
)
@click.pass_obj
def like_review(obj: dict, work_id: str, comment_id: tuple):
    """批量点赞一个作品下的多个评论（使用Token文件中所有Token）"""
    token_file = obj["token_file"]
    for cid in _parse_ids(comment_id):
        click.echo(f"请稍后，正在执行：{cid}")
        if _LikeReview(token_file, work_id, cid):
            click.echo(f"点赞评论 {cid} 执行成功")
        else:
            click.echo(f"点赞评论 {cid} 执行失败", err=True)
            raise click.Abort()


@cli.command("collect-work")
@click.option(
    "--work-id",
    "-wid",
    required=True,
    multiple=True,
    help="作品ID（可多次使用，也支持逗号分隔或JSON/Python列表）",
)
@click.pass_obj
def collect_work(obj: dict, work_id: tuple):
    """批量收藏一个或多个作品（使用Token文件中所有Token）"""
    token_file = obj["token_file"]
    for wid in _parse_ids(work_id):
        click.echo(f"请稍后，正在执行：{wid}")
        if _CollectionWork(token_file, wid):
            click.echo(f"收藏 {wid} 执行成功")
        else:
            click.echo(f"收藏 {wid} 执行失败", err=True)
            raise click.Abort()


@cli.command(
    "report-work",
    short_help=f"批量举报一个或多个作品（使用Token文件中的前{_ReportReadtokenLine}行Token）",
    help=f"批量举报一个或多个作品（使用Token文件中的前{_ReportReadtokenLine}行Token）",
)
@click.option(
    "--work-id",
    "-wid",
    required=True,
    multiple=True,
    help="作品ID（可多次使用，也支持逗号分隔或JSON/Python列表）",
)
@click.option("--report-reason", "-r", required=True, help="原因")
@click.option("--report-describe", "-d", required=True, help="举报理由")
@click.pass_obj
def report_work(obj: dict, work_id: tuple, report_reason: str, report_describe: str):
    """批量举报一个或多个作品（默认使用Token文件中的前20行Token）"""
    token_file = obj["token_file"]
    if (
        input(
            "警告：这是一个高危功能，请确保你知道你在做什么，这可能对他人造成严重的损失！包括但不限于：作品消失、作品被删除等[y/N]"
        ).lower()
        == "y"
    ):
        for wid in _parse_ids(work_id):
            click.echo(f"请稍后，正在执行：{wid}")
            if _ReportWork(token_file, wid, report_reason, report_describe):
                click.echo(f"举报 {wid} 执行成功")
            else:
                click.echo(f"举报 {wid} 执行失败", err=True)
                raise click.Abort()


@cli.command("review-work")
@click.option(
    "--work-id",
    "-wid",
    required=True,
    multiple=True,
    help="作品ID（可多次使用，也支持逗号分隔或JSON/Python列表）",
)
@click.option(
    "--review-text",
    "-r",
    required=True,
    multiple=True,
    help="评论内容（可多次使用，每条评论将依次发送到每个作品）",
)
@click.pass_obj
def review_work(obj: dict, work_id: tuple, review_text: tuple):
    """在一个或多个作品下批量发送评论（每个作品发送所有评论内容）"""
    token_file = obj["token_file"]
    work_ids = _parse_ids(work_id)
    for wid in work_ids:
        for text in review_text:
            click.echo(f"请稍后，正在执行：{wid} | 发送内容：{text}")
            if _SendReviewToWork(token_file, wid, text):
                click.echo(f"评论 {wid} 发送成功")
            else:
                click.echo(f"评论 {wid} 发送失败", err=True)
                raise click.Abort()


@cli.command("review-top")
@click.option("--one-token", "-t", required=True, help="一个可用Token")
@click.option("--work-id", "-wid", required=True, help="作品ID")
@click.option("--comment-id", "-cid", required=True, help="评论ID")
def review_top(one_token: str, work_id: str, comment_id: str):
    """越权置顶某个评论（使用单个Token）"""
    click.echo("请稍后...")
    if _TopReview(one_token, work_id, comment_id):
        click.echo("执行成功")
    else:
        click.echo("执行失败", err=True)
        raise click.Abort()


@cli.command("review-untop")
@click.option("--one-token", "-t", required=True, help="一个可用Token")
@click.option("--work-id", "-wid", required=True, help="作品ID")
@click.option("--comment-id", "-cid", required=True, help="评论ID")
def review_untop(one_token: str, work_id: str, comment_id: str):
    """越权取消置顶某个评论（使用单个Token）"""
    click.echo("请稍后...")
    if _UnTopReview(one_token, work_id, comment_id):
        click.echo("执行成功")
    else:
        click.echo("执行失败", err=True)
        raise click.Abort()


@cli.command("view-work")
@click.option("--one-token", "-t", required=True, help="一个可用Token")
@click.option("--work-id", "-wid", required=True, help="作品ID")
def view_work(one_token: str, work_id: str):
    """给作品加一个浏览（使用单个Token）"""
    click.echo("请稍后...")
    if _ViewWork(one_token, work_id):
        click.echo("执行成功")
    else:
        click.echo("执行失败", err=True)
        raise click.Abort()


@cli.command("fork-work")
@click.option(
    "--work-id",
    "-wid",
    required=True,
    multiple=True,
    help="作品ID（可多次使用，也支持逗号分隔或JSON/Python列表）",
)
@click.pass_obj
def fork_work(obj: dict, work_id: tuple):
    """再创作一个或多个作品（使用Token文件中所有Token）"""
    token_file = obj["token_file"]
    for wid in _parse_ids(work_id):
        click.echo(f"请稍后，正在执行：{wid}")
        if _ForkWork(token_file, wid):
            click.echo(f"再创作 {wid} 执行成功")
        else:
            click.echo(f"再创作 {wid} 执行失败", err=True)
            raise click.Abort()


# ------------------------------------------------------------
# Edu相关命令
# ------------------------------------------------------------
@cli.command("create-class")
@click.option("--token", "-t", required=True, help="Edu Token")
@click.option("--class-name", "-cn", required=True, help="班级名称")
def create_class(token: str, class_name: str):
    """在Edu里添加一个新的班级"""
    click.echo("请稍后...")
    class_id = _CreateClassOnEdu(token, class_name)
    if class_id != "0":
        click.echo(f"Class ID: {class_id}")
    else:
        click.echo("创建班级失败", err=True)
        raise click.Abort()


@cli.command("create-student")
@click.option("--token", "-t", required=True, help="Edu Token")
@click.option("--class-id", "-cid", required=True, help="班级ID")
@click.option(
    "--student-name-list",
    "-sl",
    default=json.dumps(student_names),
    help="学生名字列表，JSON格式（默认使用内置列表）",
)
@click.option(
    "--output-xls",
    "-o",
    default="student_passwords.xls",
    help="输出的xls文件路径",
    show_default=True,
)
def create_student(token: str, class_id: str, student_name_list: str, output_xls: str):
    """批量创建学生账户并添加到班级，保存密码表为xls文件"""
    try:
        name_list = json.loads(student_name_list)
    except json.JSONDecodeError:
        click.echo("错误：--student-name-list 必须是有效的JSON数组", err=True)
        raise click.Abort()

    click.echo("请稍后...")
    try:
        xls_content = _CreateStudentOnEdu(token, class_id, name_list)
        if xls_content:
            with open(output_xls, "wb") as f:
                f.write(xls_content)
            click.echo(f"执行成功，学生密码表已保存到: {output_xls}")
        else:
            click.echo("创建学生失败", err=True)
            raise click.Abort()
    except Exception as e:
        click.echo(f"执行失败: {e}", err=True)
        raise click.Abort()


@cli.command("merge-xls")
@click.option(
    "--input-xls-folder", "-if", required=True, help="含有多个.xls文件的文件夹"
)
@click.option(
    "--output-xlsx",
    "-o",
    default="output.xlsx",
    help="输出xlsx文件名",
    show_default=True,
)
def merge_xls(input_xls_folder: str, output_xlsx: str):
    """合并多个xls文件为一个xlsx文件"""
    click.echo("请稍后...")
    if _MergeStudentXls(input_xls_folder, output_xlsx):
        click.echo(f"执行成功，合并的文件已保存到：{output_xlsx}")
    else:
        click.echo("合并失败", err=True)
        raise click.Abort()


@cli.command("login-edu")
@click.option("--input-xlsx", "-i", required=True, help="含有账号密码的xlsx文件路径")
@click.option("--signature-user", "-s", is_flag=True, help="是否同时签署友好协议")
@click.option(
    "--output-txt", "-o", default="tokens.txt", help="输出Token文件", show_default=True
)
def login_edu(input_xlsx: str, signature_user: bool, output_txt: str):
    """批量登录xlsx内的Edu账号，保存Token到文件"""
    click.echo("请稍后...")
    if _LoginUseEdu(input_xlsx, output_txt, signature_user):
        click.echo(f"执行成功，已将登录的Token保存到：{output_txt}")
    else:
        click.echo("登录过程出现错误", err=True)
        raise click.Abort()


# ------------------------------------------------------------
# 其它命令
# ------------------------------------------------------------
@cli.command("version")
def version():
    """获取CET版本"""
    click.echo(f"CET版本: v{__version__}")
    click.echo("https://github.com/mifongjvav/CETNext/")


if __name__ == "__main__":
    cli()
