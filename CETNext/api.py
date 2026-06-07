"""
API调用
"""
# 版权所有 (C) 2026 Argon
# 根据 Apache 2.0 许可证发布
#
# 修改声明：
# 本文件基于原作者 WangZixu（2025）的作品修改而来。
# 主要修改内容：
# 将 requests 改为 playwright
# 将 UA 改为常量
# 将同步实现改为异步实现
# 修改日期：2026-06-07

import logging
import atexit
import asyncio
import json
import threading
from concurrent.futures import TimeoutError as FutureTimeoutError
from playwright.async_api import (
    async_playwright,
    TimeoutError as PlaywrightTimeoutError,
)

_browser = None
_context = None
_playwright = None
_loop = None
_loop_thread = None
_loop_ready = threading.Event()
_loop_lock = threading.Lock()
_browser_ready = threading.Event()

logger = logging.getLogger(__name__)


USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/147.0.0.0 Safari/537.36"
)

_default_headless = True


def set_default_headless(value: bool):
    """设置全局无头浏览器模式"""
    global _default_headless
    _default_headless = value


async def _init_browser(headless: bool = None):
    global _playwright, _browser, _context

    if _browser is not None:
        return

    if headless is None:
        headless = _default_headless

    try:
        logger.info("正在启动 Playwright...")
        _playwright = await async_playwright().start()
        logger.info("正在启动 Chromium 浏览器...")
        _browser = await _playwright.chromium.launch(
            headless=headless,
            args=[
                "--disable-blink-features=AutomationControlled",
                "--no-sandbox",
                "--disable-gpu",
            ],
        )
        logger.info("正在创建浏览器上下文...")
        _context = await _browser.new_context(
            user_agent=USER_AGENT,
            viewport={"width": 1920, "height": 1080},
            locale="zh-CN",
            timezone_id="Asia/Shanghai",
        )
        await _context.add_init_script("""
            Object.defineProperty(navigator, 'webdriver', { get: () => false });
            Object.defineProperty(navigator, 'plugins', { get: () => [1, 2, 3, 4, 5] });
            Object.defineProperty(navigator, 'languages', { get: () => ['zh-CN', 'zh', 'en'] });
            window.chrome = { runtime: {}, loadTimes: function(){}, csi: function(){}, app: {} };
        """)
        logger.info("浏览器初始化完成")
        _browser_ready.set()
    except Exception:
        logger.exception("浏览器初始化失败，请 playwright install chromium 安装浏览器")
        _browser_ready.set()
        raise


async def _request_async(
    method, url, headers=None, retry=3, headless: bool = None, **kwargs
):
    global _context, _browser

    if headless is None:
        headless = _default_headless

    # 确保浏览器已初始化
    if _browser is None:
        await _init_browser(headless)

    if _browser is None or _context is None:
        raise RuntimeError("浏览器初始化失败")

    result = None
    post_data = kwargs.get("json")

    for i in range(retry):
        page = None
        try:
            logger.debug(f"第 {i + 1} 次尝试: 创建新页面")
            page = await _context.new_page()
            logger.debug("新页面已创建，正在发起请求")

            request_options = {
                "method": method,
                "headers": headers or {},
                "timeout": 30000,
            }
            if post_data is not None:
                request_options["data"] = json.dumps(post_data, ensure_ascii=False)
                request_options["headers"]["Content-Type"] = "application/json"

            response = await page.request.fetch(url, **request_options)
            status_code = response.status
            response_text = await response.text()
            logger.debug(f"请求完成，状态码: {status_code}")

            if status_code != 200:
                logger.warning(
                    f"非 200 状态码: {status_code}, 返回内容预览: {response_text[:500]}"
                )

            if "renderData" not in response_text and "aliyun_waf" not in response_text:
                result = PlaywrightResponse(status_code, response_text, url)
                logger.info(f"请求成功: {status_code}")
                break

            logger.warning(
                f"请求被 WAF 拦截，状态码: {status_code}, 返回内容预览: {response_text[:500]}"
            )
            await asyncio.sleep((i + 1) * 2)

        except PlaywrightTimeoutError:
            logger.warning(f"请求超时，重试 {i + 1}/{retry}")
            await asyncio.sleep((i + 1) * 2)
        except Exception as e:
            error_msg = str(e)
            response_preview = ""
            if hasattr(e, "response") and e.response:
                try:
                    response_preview = await e.response.text()
                    response_preview = response_preview[:500]
                except Exception:
                    response_preview = "<无法读取响应内容>"
            logger.warning(
                f"请求异常: {error_msg}, 响应预览: {response_preview}, 重试 {i + 1}/{retry}"
            )
            await asyncio.sleep((i + 1) * 2)
        finally:
            if page:
                try:
                    await page.close()
                    logger.debug("页面已关闭")
                except Exception:
                    pass

    return result


async def _close_browser_async():
    global _context, _browser, _playwright
    logger.info("正在关闭浏览器…")
    if _context:
        try:
            await _context.close()
        except Exception:
            pass
    if _browser:
        try:
            await _browser.close()
        except Exception:
            pass
    if _playwright:
        try:
            await _playwright.stop()
        except Exception:
            pass

    _context = _browser = _playwright = None
    _browser_ready.clear()


def _run_loop():
    global _loop
    asyncio.set_event_loop(_loop)
    _loop_ready.set()
    try:
        _loop.run_forever()
    except Exception as e:
        logger.error(f"事件循环异常: {e}")


def _start_loop(headless: bool = None):
    global _loop, _loop_thread
    with _loop_lock:
        if _loop_thread is not None and _loop_thread.is_alive() and _loop is not None:
            # 事件循环已经运行，直接等待浏览器就绪或继续初始化
            if not _browser_ready.is_set():
                future = asyncio.run_coroutine_threadsafe(
                    _init_browser(headless), _loop
                )
                try:
                    future.result(timeout=120)
                except Exception as e:
                    logger.error(f"浏览器初始化失败: {e}")
                    raise
            return

        # 创建新的事件循环
        _loop = asyncio.new_event_loop()
        if hasattr(asyncio, "WindowsSelectorEventLoopPolicy"):
            asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

        _loop_ready.clear()
        _loop_thread = threading.Thread(target=_run_loop, daemon=True)
        _loop_thread.start()

        if not _loop_ready.wait(timeout=30):
            raise RuntimeError("事件循环启动超时")

        # 初始化浏览器
        future = asyncio.run_coroutine_threadsafe(_init_browser(headless), _loop)
        try:
            future.result(timeout=120)
        except Exception as e:
            logger.error(f"浏览器初始化失败: {e}")
            raise


def _close_browser():
    global _loop, _loop_thread
    if _loop is None:
        return

    try:
        future = asyncio.run_coroutine_threadsafe(_close_browser_async(), _loop)
        future.result(timeout=30)
    except Exception as exc:
        logger.warning(f"关闭浏览器时发生异常: {exc}")
    finally:
        with _loop_lock:
            if _loop and _loop.is_running():
                _loop.call_soon_threadsafe(_loop.stop)
            if _loop_thread and _loop_thread.is_alive():
                _loop_thread.join(timeout=10)
            _loop = None
            _loop_thread = None
            _loop_ready.clear()


class PlaywrightResponse:
    def __init__(self, status_code, text, url):
        self._status_code = status_code
        self._text = text
        self.url = url
        self.ok = 200 <= status_code < 300

    @property
    def status_code(self):
        return self._status_code

    @property
    def text(self):
        return self._text

    def json(self):
        return json.loads(self._text)

    @property
    def code(self):
        return self._status_code


def _request(method, url, headers=None, retry=3, headless: bool = None, **kwargs):
    _start_loop(headless)
    post_data = kwargs.get("json")
    future = asyncio.run_coroutine_threadsafe(
        _request_async(
            method, url, headers=headers, retry=retry, headless=headless, json=post_data
        ),
        _loop,
    )

    try:
        return future.result(timeout=60)
    except FutureTimeoutError:
        logger.error(f"主线程等待超时: {method} {url}")
        return None
    except Exception as exc:
        logger.error(f"请求执行失败: {exc}", exc_info=True)
        return None


def get_headers(token=None, include_auth=True):
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json, text/plain, */*",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
        "Origin": "https://shequ.codemao.cn",
        "Referer": "https://shequ.codemao.cn/",
        "User-Agent": USER_AGENT,
        "sec-ch-ua": '"Google Chrome";v="147", "Not.A/Brand";v="8", "Chromium";v="147"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
    }
    if include_auth and token:
        headers["authorization"] = token
    return headers


def GetAPI(Path, Token, headless=None):
    if headless is None:
        headless = _default_headless
    return _request(
        "GET", f"https://api.codemao.cn{Path}", get_headers(Token), headless=headless
    )


def GetWithoutTokenAPI(Path, headless=None):
    if headless is None:
        headless = _default_headless
    return _request(
        "GET",
        f"https://api.codemao.cn{Path}",
        get_headers(include_auth=False),
        headless=headless,
    )


def PostAPI(Path, PostData, Token, headless=None):
    if headless is None:
        headless = _default_headless
    return _request(
        "POST",
        f"https://api.codemao.cn{Path}",
        get_headers(Token),
        json=PostData,
        headless=headless,
    )


def PostWithoutTokenAPI(Path, PostData, headless=None):
    if headless is None:
        headless = _default_headless
    return _request(
        "POST",
        f"https://api.codemao.cn{Path}",
        get_headers(include_auth=False),
        json=PostData,
        headless=headless,
    )


def PostEduAPI(Path, PostData, Token, headless=None):
    if headless is None:
        headless = _default_headless
    h = get_headers(Token)
    h.update(
        {
            "Origin": "https://eduzone.codemao.cn",
            "Referer": "https://eduzone.codemao.cn/",
            "authorization": f"Bearer {Token}",
        }
    )
    return _request(
        "POST", f"https://eduzone.codemao.cn{Path}", h, json=PostData, headless=headless
    )


def PutAPI(Path, Token, headless=None):
    if headless is None:
        headless = _default_headless
    return _request(
        "PUT", f"https://api.codemao.cn{Path}", get_headers(Token), headless=headless
    )


def DeleteAPI(Path, Token, headless=None):
    if headless is None:
        headless = _default_headless
    return _request(
        "DELETE", f"https://api.codemao.cn{Path}", get_headers(Token), headless=headless
    )


def close():
    _close_browser()


atexit.register(close)
