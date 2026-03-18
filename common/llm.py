"""LLM Chat API 公共封装（Ollama OpenAI 兼容接口）。"""

from __future__ import annotations

import os

import requests

from common.config import load_dotenv

load_dotenv()


def chat(
    messages: list[dict[str, str]],
    *,
    model: str | None = None,
    temperature: float = 0.7,
    max_tokens: int = 1024,
) -> str:
    """调用 LLM Chat API，返回模型回复的文本。

    Parameters
    ----------
    messages : list[dict]
        OpenAI 格式的消息列表，每条 {"role": "system"|"user"|"assistant", "content": "..."}
    model : str, optional
        模型名称，默认读 LLM_MODEL 环境变量，兜底 "qwen3:8b"
    temperature : float
        生成温度，越高越随机
    max_tokens : int
        最大生成 token 数

    Returns
    -------
    str
        模型回复的文本内容
    """
    url = os.getenv("LLM_URL", "http://localhost:11434/v1/chat/completions")
    model = model or os.getenv("LLM_MODEL", "qwen3:8b")
    api_key = os.getenv("LLM_API_KEY", "ollama")

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    body = {
        "model": model,
        "messages": messages,
        "temperature": temperature,
        "max_tokens": max_tokens,
    }

    timeout = float(os.getenv("LLM_TIMEOUT_SECONDS", "120"))
    response = requests.post(url, headers=headers, json=body, timeout=timeout)

    try:
        response.raise_for_status()
    except requests.HTTPError as exc:
        detail = response.text.strip()
        raise requests.HTTPError(
            f"LLM 请求失败: status={response.status_code}, model={model}, url={url}, body={detail}",
            response=response,
        ) from exc

    result = response.json()
    return result["choices"][0]["message"]["content"]
