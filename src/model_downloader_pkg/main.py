#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
通用交互式模型下载工具
通过终端交互引导用户从 ModelScope 或 Hugging Face 下载任何模型。
"""
import os
import shutil
import time
from pathlib import Path
from typing import Optional, Dict


class UniversalModelDownloader:
    """交互式通用模型下载器"""

    def __init__(self):
        self.models_dir: Optional[Path] = None

    def print_banner(self):
        """打印欢迎横幅"""
        print("\n" + "=" * 60)
        print("🚀 通用交互式模型下载工具")
        print("=" * 60)
        print("该工具将帮助您从 ModelScope 或 Hugging Face 下载任何模型。")
        print("=" * 60 + "\n")

    def setup_models_directory(self) -> bool:
        """设置模型存储目录"""
        print("📁 设置模型存储根目录")
        print("-" * 30)

        # 建议的默认目录
        default_dir = Path.cwd() / "models"

        try:
            choice = input(
                f"请输入模型存储目录 (按 Enter 使用默认路径: {default_dir}): "
            ).strip()

            if not choice:
                self.models_dir = default_dir
            else:
                self.models_dir = Path(choice)

            # 创建目录
            self.models_dir.mkdir(parents=True, exist_ok=True)
            print(f"✅ 模型将存储在: {self.models_dir.resolve()}")
            return True

        except Exception as e:
            print(f"❌ 创建目录失败: {e}")
            return False

    def get_model_info_from_user(self) -> Optional[Dict]:
        """让用户输入模型ID并生成模型信息"""
        print("\n📝 请输入您想下载的模型信息")
        print("-" * 30)

        while True:
            model_id = input(
                "请输入 ModelScope 或 Hugging Face 的模型 ID\n(例如: Qwen/Qwen2-7B-Instruct): "
            ).strip()
            if model_id:
                # 将模型ID中的'/'替换为'_'，以创建安全的本地文件夹名
                local_name = model_id.replace("/", "_")

                model_info = {
                    "id": model_id,
                    "local_name": local_name,
                }
                print(f"✅ 准备下载模型: {model_id}")
                print(f"✅ 将保存到本地文件夹: {local_name}")
                return model_info
            else:
                print("❌ 模型 ID 不能为空，请重新输入。")

    def check_existing_model(self, model_name: str) -> str:
        """检查本地是否已存在模型"""
        model_dir = self.models_dir / model_name

        if not model_dir.exists():
            return "not_exist"

        print(f"\n🔍 发现已存在的目录，检查模型 '{model_name}' 的完整性...")

        if self.check_model_integrity(model_dir):
            return "complete"
        else:
            return "incomplete"

    def check_model_integrity(self, model_dir: Path) -> bool:
        """
        检查模型文件的完整性 (通用版本)。
        - 必须有 config.json
        - 必须有至少一个权重文件 (.safetensors 或 .bin)
        """
        config_file = model_dir / "config.json"
        if not config_file.exists():
            print("  ❌ 完整性检查失败: 缺少 'config.json' 文件。")
            return False

        # 检查是否存在任何权重文件
        has_weights = any(model_dir.glob("*.safetensors")) or any(
            model_dir.glob("*.bin")
        )
        if not has_weights:
            print("  ❌ 完整性检查失败: 缺少模型权重文件 (.safetensors 或 .bin)。")
            return False

        total_size = sum(f.stat().st_size for f in model_dir.rglob("*") if f.is_file())
        size_gb = total_size / (1024**3)
        print(
            f"  ✅ 完整性检查通过: 找到配置文件和权重文件 (总大小: {size_gb:.2f} GB)。"
        )
        return True

    def handle_existing_model(self, model_name: str, status: str) -> bool:
        """根据模型存在状态决定是否需要下载"""
        if status == "complete":
            print(f"✅ 模型 '{model_name}' 已完整存在。")
            choice = input(
                "选择操作:\n  1. 使用现有模型 (默认)\n  2. 删除并重新下载\n请选择 (1/2): "
            ).strip()

            if choice == "2":
                print("🔄 将删除并重新下载模型...")
                try:
                    shutil.rmtree(self.models_dir / model_name)
                    return True  # 需要下载
                except Exception as e:
                    print(f"❌ 删除目录失败: {e}")
                    return False  # 删除失败，无法继续
            else:
                print("✅ 将使用现有模型。")
                return False  # 不需要下载

        elif status == "incomplete":
            print(f"⚠️  发现不完整的模型: {model_name}")
            choice = input(
                "选择操作:\n  1. 删除不完整的文件夹并重新下载 (默认)\n  2. 取消\n请选择 (1/2): "
            ).strip()

            if choice == "2":
                print("❌ 已取消下载。")
                return False  # 不需要下载
            else:
                print("🗑️  正在删除不完整的模型...")
                try:
                    shutil.rmtree(self.models_dir / model_name)
                    return True  # 需要下载
                except Exception as e:
                    print(f"❌ 删除目录失败: {e}")
                    return False

        return True  # 模型不存在 (not_exist)，需要下载

    def select_download_source(self) -> str:
        """选择下载源"""
        print("\n📥 选择下载库和镜像源")
        print("-" * 30)
        print("1. ModelScope (国内推荐，下载 ModelScope 模型)")
        print("2. Hugging Face 官方 (下载 Hugging Face 模型)")
        print("3. Hugging Face 镜像 (hf-mirror.com，国内推荐)")
        print("4. 自动选择 (先尝试 ModelScope，失败后尝试 Hugging Face 镜像)")

        while True:
            choice = input("\n请选择下载源 (1-4): ").strip()
            if choice in ["1", "2", "3", "4"]:
                return {
                    "1": "modelscope",
                    "2": "hf_official",
                    "3": "hf_mirror",
                    "4": "auto",
                }[choice]
            print("❌ 无效选择，请输入 1-4 之间的数字。")

    def download_from_source(self, model_info: Dict, source: str) -> bool:
        """从指定源下载模型"""
        model_id = model_info["id"]
        local_dir = self.models_dir / model_info["local_name"]

        print(f"\n📥 开始下载: {model_id}")
        print(f"   保存至: {local_dir}")
        print("-" * 50)

        if source == "modelscope":
            return self._download_modelscope(model_id, local_dir)
        elif source == "hf_mirror":
            return self._download_huggingface(model_id, local_dir, use_mirror=True)
        elif source == "hf_official":
            return self._download_huggingface(model_id, local_dir, use_mirror=False)

        return False

    def _download_modelscope(self, model_id: str, local_dir: Path) -> bool:
        """从 ModelScope 下载"""
        try:
            from modelscope.hub.snapshot_download import snapshot_download

            print(f"🚀 正在从 ModelScope 下载: {model_id}")

            # 修正: 使用 `local_dir` 参数直接指定下载位置
            snapshot_download(
                model_id=model_id, local_dir=str(local_dir), revision="master"
            )

            print("✅ ModelScope 下载完成!")
            return True

        except ImportError:
            print("❌ 错误: 未安装 'modelscope' 库。")
            print("   请运行: pip install modelscope")
            return False
        except Exception as e:
            print(f"❌ ModelScope 下载失败: {e}")
            return False

    def _download_huggingface(
        self, repo_id: str, local_dir: Path, use_mirror: bool = True
    ) -> bool:
        """从 Hugging Face 下载"""
        original_endpoint = os.environ.get("HF_ENDPOINT")
        try:
            from huggingface_hub import snapshot_download

            if use_mirror:
                os.environ["HF_ENDPOINT"] = "https://hf-mirror.com"
                print(f"🚀 正在从 Hugging Face 镜像下载: {repo_id}")
            else:
                # 如果用户已设置全局镜像，我们在此处不覆盖它
                if "HF_ENDPOINT" in os.environ:
                    os.environ.pop("HF_ENDPOINT")
                print(f"🚀 正在从 Hugging Face 官方源下载: {repo_id}")

            snapshot_download(
                repo_id=repo_id,
                local_dir=str(local_dir),
                local_dir_use_symlinks=False,
                resume_download=True,
            )

            print("✅ Hugging Face 下载完成!")
            return True

        except ImportError:
            print("❌ 错误: 未安装 'huggingface_hub' 库。")
            print("   请运行: pip install huggingface-hub")
            return False
        except Exception as e:
            print(f"❌ Hugging Face 下载失败: {e}")
            return False
        finally:
            # 修正: 下载后恢复原始环境变量，避免副作用
            if original_endpoint:
                os.environ["HF_ENDPOINT"] = original_endpoint
            elif "HF_ENDPOINT" in os.environ:
                # If we set it, we remove it
                if use_mirror or not original_endpoint:
                    os.environ.pop("HF_ENDPOINT")

    def auto_download(self, model_info: Dict) -> bool:
        """自动按顺序尝试多个下载源"""
        # 自动模式优先尝试国内友好的源
        sources = [
            ("modelscope", "ModelScope"),
            ("hf_mirror", "HuggingFace 镜像"),
            ("hf_official", "HuggingFace 官方"),
        ]

        for source_key, source_name in sources:
            print(f"\n🔄 自动模式: 正在尝试 {source_name}...")
            if self.download_from_source(model_info, source_key):
                return True
            print(f"❌ {source_name} 下载失败，尝试下一个源...")

        return False

    def verify_download(self, model_name: str) -> bool:
        """下载后最终验证"""
        print("\n🔍 正在验证下载结果...")
        model_dir = self.models_dir / model_name

        if self.check_model_integrity(model_dir):
            print("✅ 模型下载并验证成功!")
            return True
        else:
            print("❌ 下载后的模型文件不完整或已损坏。")
            # 自动清理不完整下载
            if model_dir.exists():
                print("   正在清理损坏的文件夹...")
                try:
                    shutil.rmtree(model_dir)
                    print("   清理完成。")
                except Exception as e:
                    print(f"   清理失败: {e}")
            return False

    def show_summary(self, model_info: Dict, success: bool):
        """显示最终的总结信息"""
        print("\n" + "=" * 60)
        print("📊 下载总结")
        print("=" * 60)

        model_name = model_info["local_name"]
        model_id = model_info["id"]

        if success:
            model_dir = self.models_dir / model_name
            total_size = sum(
                f.stat().st_size for f in model_dir.rglob("*") if f.is_file()
            )
            size_gb = total_size / (1024**3)

            print(f"✅ 模型 ID: {model_id}")
            print(f"✅ 状态: 下载成功")
            print(f"✅ 本地路径: {model_dir.resolve()}")
            print(f"✅ 模型大小: {size_gb:.2f} GB")
            print("\n🎉 恭喜！模型已准备就绪，可以在您的代码中使用了。")
        else:
            print(f"❌ 模型 ID: {model_id}")
            print(f"❌ 状态: 下载失败")
            print("\n🔧 建议解决方案:")
            print("   - 检查网络连接是否正常。")
            print("   - 尝试选择其他下载源 (例如，如果官方源失败，尝试镜像源)。")
            print("   - 确认输入的模型 ID 是否正确且存在于相应的平台。")
            print("   - 确保磁盘有足够的可用空间。")

        print("=" * 60)

    def run(self):
        """运行交互式下载主流程"""
        try:
            self.print_banner()

            if not self.setup_models_directory():
                return

            model_info = self.get_model_info_from_user()
            if not model_info:
                print("❌ 未提供模型 ID，程序退出。")
                return

            model_name = model_info["local_name"]

            existing_status = self.check_existing_model(model_name)
            needs_download = self.handle_existing_model(model_name, existing_status)

            if not needs_download:
                print("\n程序结束。")
                self.show_summary(
                    model_info, success=True
                )  # 即使是使用现有模型，也显示成功总结
                return

            download_source = self.select_download_source()

            start_time = time.time()
            success = False

            if download_source == "auto":
                success = self.auto_download(model_info)
            else:
                success = self.download_from_source(model_info, download_source)

            if success:
                success = self.verify_download(model_name)

            end_time = time.time()

            self.show_summary(model_info, success)

            if success:
                duration = end_time - start_time
                print(f"⏱️  本次下载耗时: {duration:.1f} 秒")

        except KeyboardInterrupt:
            print("\n\n⚠️  用户中断操作，程序已退出。")
        except Exception as e:
            print(f"\n❌ 发生未知错误: {e}")
            print("   程序异常退出。")


def main():
    """主函数入口"""
    downloader = UniversalModelDownloader()
    downloader.run()


if __name__ == "__main__":
    main()
