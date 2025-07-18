# Universal Model Downloader (通用交互式模型下载工具)

[![PyPI Version](https://img.shields.io/pypi/v/universal-model-downloader.svg)](https://pypi.org/project/universal-model-downloader)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python Versions](https://img.shields.io/pypi/pyversions/universal-model-downloader.svg)](https://pypi.org/project/universal-model-downloader)
![Built with uv](https://img.shields.io/badge/built%20with-uv-4C8E93.svg)

一个用户友好的、交互式的命令行工具，旨在帮助开发者轻松地从 **ModelScope** 和 **Hugging Face** 下载机器学习模型。

A user-friendly, interactive command-line tool to easily download machine learning models from **ModelScope** and **Hugging Face**.

---

### 效果演示 (Demo)
```bash
============================================================
🚀 通用交互式模型下载工具
============================================================
该工具将帮助您从 ModelScope 或 Hugging Face 下载任何模型。
============================================================

📁 设置模型存储根目录
------------------------------
请输入模型存储目录 (按 Enter 使用默认路径: /data/models): 
✅ 模型将存储在: /data/models

📝 请输入您想下载的模型信息
------------------------------
请输入 ModelScope 或 Hugging Face 的模型 ID
(例如: Qwen/Qwen2-7B-Instruct): OpenBMB/MiniCPM4-8B
✅ 准备下载模型: OpenBMB/MiniCPM4-8B
✅ 将保存到本地文件夹: OpenBMB_MiniCPM4-8B

📥 选择下载库和镜像源
------------------------------
1. ModelScope (国内推荐，下载 ModelScope 模型)
2. Hugging Face 官方 (下载 Hugging Face 模型)
3. Hugging Face 镜像 (hf-mirror.com，国内推荐)
4. 自动选择 (先尝试 ModelScope，失败后尝试 Hugging Face 镜像)

请选择下载源 (1-4): 
```

### ✨ 主要特性 (Features)

- **交互式界面**：无需记忆复杂命令，通过问答交互即可完成操作。
- **多平台支持**：同时支持国内最流行的 ModelScope (魔搭) 和国际上最常用的 Hugging Face。
- **路径自定义**：灵活指定模型的存储位置。
- **现代 & 高效**：使用现代化的 Python 工具链构建 (`uv`, `pyproject.toml`)，安装和执行都非常迅速。

### 📦 安装 (Installation)

推荐使用 `uv` 或 `pipx` 进行安装，这可以将命令行工具安装在独立的环境中，避免与系统或其他项目的依赖产生冲突。

**方法一: 使用 uv (强烈推荐)**

```bash
uv tool install git+https://github.com/wsstudent/ModelDownloader.git
```

**方法二: 使用 pipx**

```bash
pipx install git+https://github.com/wsstudent/ModelDownloader.git

```

### 🚀 如何使用 (Usage)

安装完成后，直接在终端执行以下命令即可启动交互式下载工具：

```bash
model-downloader
```

然后根据提示，依次选择平台、输入模型 ID 和指定存储路径即可。

### 🛠️ 为开发者 (For Developers)

如果你想对这个项目进行二次开发或贡献代码，请遵循以下步骤：

1. **克隆仓库 (Clone the repository)**

    ```bash
    git clone [https://github.com/](https://github.com/)<your-username>/<your-repo-name>.git
    cd <your-repo-name>
    ```

2. **创建虚拟环境并安装依赖 (Create venv and sync dependencies)**
    我们推荐使用 `uv` 来管理开发环境。

    ```bash
    # 创建虚拟环境
    uv venv

    # 激活虚拟环境
    source .venv/bin/activate

    # 安装依赖 (uv 会读取 pyproject.toml 文件)
    uv sync
    ```

3. **在开发模式下运行 (Run in development mode)**

    ```bash
    uv run model-downloader
    ```

### 🤝 贡献 (Contributing)

欢迎任何形式的贡献！无论是提交 issue、请求新功能，还是提交 Pull Request。

1. Fork 本仓库
2. 创建你的新分支 (`git checkout -b feature/AmazingFeature`)
3. 提交你的更改 (`git commit -m 'Add some AmazingFeature'`)
4. 将你的分支推送到远程 (`git push origin feature/AmazingFeature`)
5. 创建一个 Pull Request

### 📄 许可证 (License)

本项目采用 MIT 许可证。详情请见 [LICENSE](LICENSE) 文件。
