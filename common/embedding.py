"""Embedding API 公共封装。"""

from __future__ import annotations

import json

import requests

from common.config import get_embedding_config


def get_embeddings(texts: list[str], *, debug_response: bool = False) -> list[list[float]]:
    """调用 Embedding API，返回每段文本的向量。"""
    config = get_embedding_config()
    headers = {
        "Authorization": config.auth_header,
        "Content-Type": "application/json",
    }
    body = {"input": texts, "model": config.model}
    response = requests.post(
        config.url,
        headers=headers,
        json=body,
        timeout=config.timeout_seconds,
    )
    response.raise_for_status()
    result = response.json()

    if debug_response:
        print(json.dumps(result, indent=2, ensure_ascii=False))

    return [item["embedding"] for item in result["data"]]
