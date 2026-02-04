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

| **📝 简体中文**       | **🖥️ CLI Documentation** | **🧰 Function Documentation** | **🔧 Development Documentation** | **⚠️ Disclaimer** |
|:-----------------:|:----------------------:|:---------------------------:|:------------------------------:|:----------------:|
| [点击前往](README.md) | [View](doc/cli.md) | [View](doc/import.md) | [View](doc/code.md) | [View](README_EN.md#️-disclaimer) |

</div>

## 👋🏻 Welcome to CodemaoEDUTools!

A brand-new version, a brand-new experience — welcome to CodemaoEDUTools V2!

CodemaoEDUTools is designed to provide teachers in the Codemao community with a more convenient way to interact with APIs. Use it responsibly and cherish the convenience it brings.

> [!TIP]
>
> To support better long-term development, the project license was updated to **Apache 2.0** on 2026-01-19.
>
> At the same time, the disclaimer has been updated. By starting to use this program, you are deemed to have agreed to the disclaimer.

## 🔧 Installation

1. Direct installation: `pip install CodemaoEDUTools`
2. Local Wheel installation:
   - Download the latest Wheel package from the Release page
   - Install it using `pip install <path-to-wheel>`
3. Legacy method (this method does not support CLI usage):
   - Download the latest archive from the Release page
   - Place the **CodemaoEDUTools** folder into your project directory

> [!WARNING]
>
> **Compatibility Notice: If you plan to use CET in environments where stability is critical, please use version `2.1.0`. This version provides a complete and stable core feature set and is suitable for reliable long-term use. This is especially important for unattended scripts where CET must be installed every time.**

## 😎 Usage

This program can be used both as a CLI (command-line) tool and as an importable library.

### Using from the command line

After installing CodemaoEDUTools, you can invoke the tool directly from the command line using:

`cet`

For example:

`cet version`

Alternatively, after running `uv pip install -e .`, you may also use the tool via:

`uv run CodemaoEDUTools`

Starting from version 2.1.0, the project manager has been migrated to **uv**, which means CET can no longer be used in the same way as before.

### Using as a library

After installing CodemaoEDUTools, you can import it in your code using:

`import CodemaoEDUTools`

If you are developing a program intended for distribution, please ensure that end users install CodemaoEDUTools separately.

## 📃 File Formats

Programs are not humans, so file formats matter.

### Token file format

One token per line, plain text format, no file extension required. It is recommended to name the file `tokens.txt`.

### Spreadsheet file format

When performing batch login for EDU accounts, the program requires a spreadsheet containing account credentials. This spreadsheet can be generated using the `MergeStudentXls()` function.

Do not include a header row. The format should be **Account Name – Account – Password**, as shown below:

| {Account Name} | {Account} | {Password} |
|:-------------:|:---------:|:----------:|
| {Account Name} | {Account} | {Password} |

Only `.xlsx` files are supported.

## 👍🏻 Default Configuration Values

The program’s default values are defined in `__init__.py` and documented via inline comments. Due to legacy design limitations, these values cannot be customized during installation at this time; this capability may be added in the future.

Default values are only applicable when using the CLI.

## 📂 Versioning / Branches

- `main`: The primary branch. Code in this branch represents the latest stable version and automatically generates Wheel packages and archives.
- `dev`: The development branch. If you intend to contribute to or extend this project, please work on this branch.
- `old`: An archive of very early versions; this branch is no longer maintained.

The `dev` branch is periodically merged into `main` to deliver updates.

## ⚠️ Disclaimer

To the maximum extent permitted by applicable law, the project author and contributors shall not be liable for any losses arising from the use of, inability to use, or reliance on this project. Such losses include, but are not limited to, direct, indirect, incidental, special, punitive, or consequential damages, whether arising under contract, tort (including negligence), or any other legal theory, even if advised of the possibility of such damages. This disclaimer applies equally to all scenarios in which the project is used, including use as a dependency library or as a CLI tool.

This project may be used in various environments and scenarios, including but not limited to development, testing, production, and automation scripts. Users are responsible for independently evaluating the suitability, accuracy, security, and compliance of the project for their specific use cases and for assuming all associated risks.  
Any issues arising from third-party systems, platforms, data sources, API changes, API limitations, or configuration errors are outside the responsibility of this project and its author.

All APIs used by this project are officially provided by Codemao and are publicly accessible through conventional means. This project does not use any third-party APIs, nor does it bypass, circumvent, crack, or interfere with any security mechanisms, access controls, or technical protections implemented by Codemao.

Any repositories created by forking, deriving from, or further developing this project are not under the direct management or control of the original author. The author cannot continuously or effectively supervise changes in code, functionality, release behavior, or maintenance of forked repositories and assumes no responsibility for any consequences arising therefrom.

Furthermore, the author does not assume any obligation to supervise or regulate the specific usage behavior of any individual or organization using this project. Although the author has explicitly stated and repeatedly warned against using this project for any illegal or non-compliant purposes, any legal liability or consequences resulting from violations of applicable laws or improper use shall be borne solely by the user and shall have no association with this project or its author.

This project is licensed under the **Apache License, Version 2.0**.

This disclaimer does not supplement, modify, or replace any terms of the Apache License 2.0. In the event of any inconsistency between this disclaimer and the Apache License 2.0, the terms of the Apache License 2.0 shall prevail.

## 😇 Acknowledgements

Please give both me and these projects a **⭐Star️** if you find them useful.

[Aumiao](https://github.com/Aurzex/Aumiao)

[CodemaoLV5](https://github.com/Wangs-official/CodemaoLV5)

[编程猫API文档](https://api.docs.codemao.work/)

This project is derived from the following projects:

- CodemaoCommunityHistory/CodemaoEduAutoReg
- CodemaoCommunityHistory/CodemaoPL

## ❤️ Thanks to All Contributors

<a href="https://github.com/wangs-official/codemaoedutools/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=wangs-official/codemaoedutools" />
</a><br/><br/>

> *結ばれた絆に 裏切ることない愛情 を*
> 
> *为相连的牵绊 带来了永不背叛的爱情*
>
> 《LOVETOXIN》- https://music.163.com/song?id=2077776113
