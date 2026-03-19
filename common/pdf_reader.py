"""PDF 文本提取公共模块。"""

from __future__ import annotations

import re
from pathlib import Path

import fitz  # noqa: F401 — TODO 实现时需要此 import


def read_pdf(file_path: str) -> str:
    """读取 PDF 文件，返回全文纯文本。

    - 逐页提取文本（使用 page.get_text("blocks") 按文本块提取）
    - 同一页内的文本块之间用双换行分隔
    - 不同页之间用双换行分隔
    - 清理多余空行（连续 3+ 空行合并为 2 个换行）
    - 不做分块（分块交给 text_splitters）

    Parameters
    ----------
    file_path : str
        PDF 文件路径

    Returns
    -------
    str
        提取的全文纯文本

    Raises
    ------
    FileNotFoundError
        文件不存在时抛出
    """
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"PDF 文件不存在: {file_path}")

    # TODO：自己实现
    # 提示：
    # 1. 用 fitz.open(file_path) 打开 PDF
    # 2. 遍历每一页，用 page.get_text("blocks") 获取文本块列表
    #    - 每个 block 是一个元组，block[4] 是文本内容，block[6] 是类型（0=文本）
    #    - 只取 block[6] == 0 的文本块
    # 3. 同一页内的文本块用双换行 "\n\n" 连接
    # 4. 不同页的文本用双换行 "\n\n" 连接
    # 5. 用 _clean_text() 清理多余空行
    # 6. 返回清理后的文本
    raise NotImplementedError("请在这里实现 read_pdf")


def read_pdf_pages(file_path: str) -> list[dict]:
    """逐页读取 PDF，返回带页码的文本列表。

    Parameters
    ----------
    file_path : str
        PDF 文件路径

    Returns
    -------
    list[dict]
        [{"page": 1, "text": "..."}, {"page": 2, "text": "..."}, ...]

    Raises
    ------
    FileNotFoundError
        文件不存在时抛出
    """
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"PDF 文件不存在: {file_path}")

    # TODO：自己实现
    # 提示：
    # 1. 用 fitz.open(file_path) 打开 PDF
    # 2. 遍历每一页（enumerate 从 1 开始计数）
    # 3. 用 page.get_text("blocks") 获取文本块，过滤 block[6] == 0
    # 4. 将文本块用双换行连接，再用 _clean_text() 清理
    # 5. 构造 {"page": 页码, "text": 清理后文本} 字典
    # 6. 返回字典列表
    raise NotImplementedError("请在这里实现 read_pdf_pages")


def _clean_text(text: str) -> str:
    """清理提取的文本：将连续 3+ 个换行合并为 2 个。

    Parameters
    ----------
    text : str
        待清理的文本

    Returns
    -------
    str
        清理后的文本
    """
    return re.sub(r"\n{3,}", "\n\n", text).strip()
