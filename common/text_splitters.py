"""文本分块公共函数。"""

from __future__ import annotations


def chunk_by_fixed_length(text: str, chunk_size: int = 200) -> list[str]:
    """按固定字符数切分文本。"""
    if chunk_size <= 0:
        raise ValueError("chunk_size 必须大于 0")
    if not text:
        return []
    return [text[start : start + chunk_size] for start in range(0, len(text), chunk_size)]



def chunk_by_paragraph(text: str) -> list[str]:
    """按空行切分文本，并过滤空段落。"""
    return [paragraph.strip() for paragraph in text.split("\n\n") if paragraph.strip()]



def chunk_by_sliding_window(
    text: str, window_size: int = 200, overlap: int = 50
) -> list[str]:
    """按滑动窗口切分文本。"""
    if window_size <= 0:
        raise ValueError("window_size 必须大于 0")
    if overlap < 0:
        raise ValueError("overlap 不能小于 0")
    if overlap >= window_size:
        raise ValueError("overlap 必须小于 window_size")
    if not text:
        return []

    step = window_size - overlap
    return [text[start : start + window_size] for start in range(0, len(text), step)]
