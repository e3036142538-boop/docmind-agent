"""
core/client.py
DeepSeek API 客户端封装，兼容 OpenAI 接口协议
"""

import os
import time
from openai import OpenAI
from dataclasses import dataclass


@dataclass
class UsageStats:
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int
    model: str
    latency_ms: float


class DeepSeekClient:
    """DeepSeek API 统一客户端，记录 Token 使用情况"""

    BASE_URL = "https://api.deepseek.com"

    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.environ.get("DEEPSEEK_API_KEY")
        if not self.api_key:
            raise ValueError("请设置 DEEPSEEK_API_KEY 环境变量")
        self.client = OpenAI(api_key=self.api_key, base_url=self.BASE_URL)
        self.total_usage = UsageStats(0, 0, 0, "", 0)

    def chat(
        self,
        messages: list[dict],
        model: str = "deepseek-v4-pro",
        temperature: float = 0.3,
        max_tokens: int = 8192,
    ) -> tuple[str, UsageStats]:
        """
        发送对话请求，返回 (回复内容, 用量统计)
        """
        start = time.time()
        response = self.client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
        )
        latency = (time.time() - start) * 1000

        usage = UsageStats(
            prompt_tokens=response.usage.prompt_tokens,
            completion_tokens=response.usage.completion_tokens,
            total_tokens=response.usage.total_tokens,
            model=model,
            latency_ms=round(latency, 2),
        )

        # 累计统计
        self.total_usage.prompt_tokens += usage.prompt_tokens
        self.total_usage.completion_tokens += usage.completion_tokens
        self.total_usage.total_tokens += usage.total_tokens

        content = response.choices[0].message.content
        return content, usage

    def print_usage(self, usage: UsageStats):
        print(f"  ├─ 模型: {usage.model}")
        print(f"  ├─ 输入 tokens: {usage.prompt_tokens:,}")
        print(f"  ├─ 输出 tokens: {usage.completion_tokens:,}")
        print(f"  ├─ 总计 tokens: {usage.total_tokens:,}")
        print(f"  └─ 延迟: {usage.latency_ms} ms")

    def print_total_usage(self):
        print("\n" + "="*50)
        print("📊 本次任务 Token 使用汇总")
        print("="*50)
        print(f"  输入 tokens:  {self.total_usage.prompt_tokens:,}")
        print(f"  输出 tokens:  {self.total_usage.completion_tokens:,}")
        print(f"  总计 tokens:  {self.total_usage.total_tokens:,}")
        print("="*50)
