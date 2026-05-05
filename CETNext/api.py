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
# 优化史山
# 修改日期：2026-05-05

import logging
import atexit
import time
import json
import threading
import queue
import uuid
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError

_browser = None
_context = None
_playwright = None

_request_queue = queue.Queue()
_response_queues = {}
_worker_thread = None
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


def _init_browser(headless: bool = None):
    global _playwright, _browser, _context
    if _browser is not None:
        _browser_ready.set()
        return

    try:
        logger.info("正在启动 Playwright...")
        _playwright = sync_playwright().start()
        logger.info("正在启动 Chromium 浏览器...")
        _browser = _playwright.chromium.launch(
            headless=headless,
            args=[
                "--disable-blink-features=AutomationControlled",
                "--no-sandbox",
                "--disable-gpu",
            ],
        )
        logger.info("正在创建浏览器上下文...")
        _context = _browser.new_context(
            user_agent=USER_AGENT,
            viewport={"width": 1920, "height": 1080},
            locale="zh-CN",
            timezone_id="Asia/Shanghai",
        )
        _context.add_init_script("""
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


def _worker(headless: bool = None):
    global _context, _browser, _playwright
    _init_browser(headless)
    try:
        while True:
            logger.debug("Worker 等待任务...")
            task = _request_queue.get()
            if task is None:
                logger.info("Worker 收到退出信号")
                break

            request_id, method, url, headers, retry, post_data = task
            logger.info(f"处理请求 [{request_id[:8]}] {method} {url}")
            result = None

            for i in range(retry):
                page = None
                try:
                    logger.debug(f"第 {i + 1} 次尝试: 创建新页面")
                    page = _context.new_page()
                    logger.debug("新页面已创建，正在发起请求")

                    request_options = {
                        "method": method,
                        "headers": headers or {},
                        "timeout": 30000,
                    }
                    if (
                        post_data is not None
                    ):  # 当 post_data 是 {} 时，条件为 True，执行
                        request_options["data"] = json.dumps(
                            post_data, ensure_ascii=False
                        )
                        request_options["headers"]["Content-Type"] = "application/json"

                    response = page.request.fetch(url, **request_options)
                    status_code = response.status
                    response_text = response.text()
                    logger.debug(f"请求完成，状态码: {status_code}")
                    logger.debug(f"请求完成，返回: {response_text}")

                    # 检查 WAF 拦截
                    if (
                        "renderData" not in response_text
                        and "aliyun_waf" not in response_text
                    ):
                        result = PlaywrightResponse(status_code, response_text, url)
                        logger.info(f"请求成功: {status_code}")
                        break

                    logger.warning(f"请求被WAF拦截，重试 {i + 1}/{retry}")
                    time.sleep((i + 1) * 2)

                except PlaywrightTimeoutError:
                    logger.warning(f"请求超时，重试 {i + 1}/{retry}")
                    time.sleep((i + 1) * 2)
                except Exception as e:
                    logger.warning(f"请求异常: {e}，重试 {i + 1}/{retry}")
                    time.sleep((i + 1) * 2)
                finally:
                    if page:
                        try:
                            page.close()
                            logger.debug("页面已关闭")
                        except Exception:
                            pass

            if request_id in _response_queues:
                _response_queues[request_id].put(result)
                logger.debug(f"结果已返回给请求者 [{request_id[:8]}]")
    finally:
        logger.info("正在关闭浏览器…")
        if _context:
            try:
                _context.close()
            except Exception:
                pass
        if _browser:
            try:
                _browser.close()
            except Exception:
                pass
        if _playwright:
            try:
                _playwright.stop()
            except Exception:
                pass
        _context = _browser = _playwright = None
        _browser_ready.clear()


def _start_worker(headless: bool = None):
    global _worker_thread
    if _worker_thread is None or not _worker_thread.is_alive():
        _worker_thread = threading.Thread(target=_worker, args=(headless,), daemon=True)
        _worker_thread.start()
        if not _browser_ready.wait(timeout=30):
            raise RuntimeError("浏览器启动超时")
        if _browser is None:
            raise RuntimeError("浏览器初始化失败")


def _close_browser():
    global _worker_thread
    if _request_queue:
        _request_queue.put(None)
    if _worker_thread and _worker_thread.is_alive():
        _worker_thread.join(timeout=10)


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
    _start_worker(headless)
    post_data = kwargs.get("json")
    request_id = str(uuid.uuid4())
    result_queue = queue.Queue()
    _response_queues[request_id] = result_queue
    _request_queue.put((request_id, method, url, headers, retry, post_data))

    try:
        result = result_queue.get(timeout=60)
    except queue.Empty:
        logger.error(f"主线程等待超时: {method} {url}")
        result = None
    finally:
        _response_queues.pop(request_id, None)
    return result


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
        "GET", f"https://api.codemao.cn{Path}", get_headers(Token), headless
    )


def GetWithoutTokenAPI(Path, headless=None):
    if headless is None:
        headless = _default_headless
    return _request(
        "GET",
        f"https://api.codemao.cn{Path}",
        get_headers(include_auth=False),
        headless,
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
