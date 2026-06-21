# 版权所有 (C) 2026 Argon
# 根据 Apache 2.0 许可证发布
#
# 修改声明：
# 精简优化
# 移除多余
# 修改日期：2026-06-21

import coloredlogs

from CETNext.cli import cli

coloredlogs.install(level="INFO", fmt="%(asctime)s - %(levelname)s - %(funcName)s: %(message)s")

def main():
    cli()

if __name__ == "__main__":
    main()