"""用户搜索"""

from .api import GetWithoutTokenAPI as GetAPI
from . import max_workers
import logging
import math
import os
import json
from concurrent.futures import ThreadPoolExecutor

logger = logging.getLogger(__name__)


def download_user_list() -> list:
    """下载用户列表"""
    response = GetAPI(
        "/creation-tools/v1/user/followers?user_id=117275661&offset=9999999&limit=200"
    )
    total = int(response.json()["total"])
    length = math.ceil(total / 200)
    os.makedirs("user_list", exist_ok=True)
    with open("user_list/index.json", "w", encoding="utf-8") as f:
        json.dump(int(length), f)

    logger.info("正在下载用户列表，请稍后...")

    offsets = list(range(0, int(length) * 200, 200))

    def _fetch_page(offset):
        try:
            response = GetAPI(
                f"/creation-tools/v1/user/followers?user_id=117275661&offset={offset}&limit=200"
            )
            if response.status_code == 200:
                user_list = [item for item in response.json()["items"]]
                with open(f"./user_list/{offset}.json", "w", encoding="utf-8") as f:
                    json.dump(user_list, f)
                return True
            else:
                logger.error(
                    f"请求失败，状态码: {response.status_code}, 响应: {response.text[:100]}"
                )
                return False
        except Exception as e:
            logger.error(f"请求异常: {str(e)}")
            return False

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        list(executor.map(_fetch_page, offsets))


def search_user(nickname: str) -> list:
    """搜索用户"""
    search_user_list = []
    try:
        with open("user_list/index.json", "r", encoding="utf-8") as f:
            index = json.load(f)
        for idx in range(0, int(index) * 200, 200):
            try:
                with open(f"./user_list/{idx}.json", "r", encoding="utf-8") as f:
                    
                    user_list = json.load(f)
                    for item in user_list:
                        if nickname in item.get("nickname", ""):
                            search_user_list.append(
                                [item["id"], item["nickname"], item["description"], idx]
                            )
            except Exception as e:
                logger.error(f"读取文件异常: {str(e)}")
                continue
        return search_user_list
    except Exception as e:
        logger.error(f"异常: {str(e)}")
        return []
