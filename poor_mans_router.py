#!/usr/bin/env python3
"""
GMS Poor Man's Router - 穷鬼智能模型路由

专为初学者和小用量用户设计
每天自动领取免费额度，自动切换最优模型
"""

import os
import json
import time
from pathlib import Path
from typing import Optional, Dict, List
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta


@dataclass
class ModelInfo:
    """模型信息"""
    name: str
    provider: str
    api_type: str  # "chat" / "image" / "video"
    quota_type: str  # "daily" / "monthly" / "one-time"
    quota_limit: float
    quota_used: float = 0
    reset_at: str = ""  # 重置时间
    is_available: bool = True
    requires_proxy: bool = False
    strengths: List[str] = None
    weaknesses: List[str] = None

    def __post_init__(self):
        if self.strengths is None:
            self.strengths = []
        if self.weaknesses is None:
            self.weaknesses = []

    @property
    def quota_remaining(self) -> float:
        return max(0, self.quota_limit - self.quota_used)

    @property
    def quota_percent(self) -> float:
        if self.quota_limit == 0:
            return 0
        return (self.quota_remaining / self.quota_limit) * 100


# 每日免费额度模型数据库（2026年4月）
# 参考：唐斩AI编程系列指南
FREE_MODELS = {
    # ===== 文本模型 =====
    # --- 性价比之选 ---
    "deepseek-v3.2": ModelInfo(
        name="DeepSeek V3.2",
        provider="DeepSeek",
        api_type="chat",
        quota_type="api",
        quota_limit=0,  # 按量付费，但性价比最高
        requires_proxy=False,
        strengths=["性价比最高", "编程能力强", "数理逻辑好"],
        weaknesses=["需要付费"]
    ),
    "glm-4.7": ModelInfo(
        name="GLM-4.7",
        provider="智谱AI",
        api_type="chat",
        quota_type="coding-plan",
        quota_limit=0,
        requires_proxy=False,
        strengths=["编程能力强", "数理逻辑好", "中文优化"],
        weaknesses=["需要订阅"]
    ),
    "kimi-k2.5": ModelInfo(
        name="Kimi K2.5",
        provider="Kimi",
        api_type="chat",
        quota_type="coding-plan",
        quota_limit=0,
        requires_proxy=False,
        strengths=["便宜够用", "官方支持", "网页端会员"],
        weaknesses=["需要订阅"]
    ),
    "minimax-2.1": ModelInfo(
        name="MiniMax 2.1",
        provider="MiniMax",
        api_type="chat",
        quota_type="coding-plan",
        quota_limit=0,
        requires_proxy=False,
        strengths=["能力强", "官方支持"],
        weaknesses=["需要订阅"]
    ),
    # --- 免费额度 ---
    "groq-llama-3.3-70b": ModelInfo(
        name="Llama 3.3 70B",
        provider="Groq",
        api_type="chat",
        quota_type="daily",
        quota_limit=1440,  # 每天1440次请求
        requires_proxy=False,
        strengths=["免费额度多", "速度快", "代码强"],
        weaknesses=["中文一般"]
    ),
    "groq-mixtral-8x7b": ModelInfo(
        name="Mixtral 8x7B",
        provider="Groq",
        api_type="chat",
        quota_type="daily",
        quota_limit=1440,
        requires_proxy=False,
        strengths=["免费额度多", "速度快"],
        weaknesses=["中文一般"]
    ),
    "groq-gemma2-9b": ModelInfo(
        name="Gemma 2 9B",
        provider="Groq",
        api_type="chat",
        quota_type="daily",
        quota_limit=1440,
        requires_proxy=False,
        strengths=["轻量快速", "免费额度多"],
        weaknesses=["复杂任务一般"]
    ),
    "nvidia-nim": ModelInfo(
        name="NVIDIA NIM",
        provider="NVIDIA",
        api_type="chat",
        quota_type="daily",
        quota_limit=999999,  # 无限但限速40rpm
        requires_proxy=False,
        strengths=["额度无限", "注册免费"],
        weaknesses=["限速40rpm", "需配置"]
    ),
    "opencode-zen": ModelInfo(
        name="OpenCode Zen",
        provider="OpenCode",
        api_type="chat",
        quota_type="free",
        quota_limit=0,  # 有免费额度
        requires_proxy=False,
        strengths=["k2.5免费额度", "官方直接接入"],
        weaknesses=["需要配置"]
    ),
    # --- 其他免费 ---
    "cohere-command-r-plus": ModelInfo(
        name="Command R+",
        provider="Cohere",
        api_type="chat",
        quota_type="monthly",
        quota_limit=1000,  # 每月1000次
        requires_proxy=False,
        strengths=["RAG优化", "搜索强", "中文较好"],
        weaknesses=["创意写作一般"]
    ),
    "google-gemini-pro": ModelInfo(
        name="Gemini Pro",
        provider="Google AI Studio",
        api_type="chat",
        quota_type="daily",
        quota_limit=60,  # RPM限制
        requires_proxy=False,
        strengths=["多模态", "中文好", "额度独立"],
        weaknesses=["需要申请"]
    ),
    "siliconflow-glm-4": ModelInfo(
        name="GLM-4",
        provider="硅基流动",
        api_type="chat",
        quota_type="one-time",
        quota_limit=10,  # ¥10体验金
        requires_proxy=False,
        strengths=["便宜", "中文好"],
        weaknesses=["额度有限"]
    ),

    # --- 不推荐 ---
    "anthropic-claude": ModelInfo(
        name="Claude",
        provider="Anthropic",
        api_type="chat",
        quota_type="subscription",
        quota_limit=0,
        requires_proxy=True,
        strengths=["能力强"],
        weaknesses=["❌政策严易封号", "不推荐接入第三方"]
    ),

    # ===== 图像模型 =====
    "flux-dev": ModelInfo(
        name="Flux Dev",
        provider="Fal",
        api_type="image",
        quota_type="daily",
        quota_limit=100,
        requires_proxy=False,
        strengths=["高质量", "逼真"],
        weaknesses=["需要申请"]
    ),
    "google-imagen-3": ModelInfo(
        name="Imagen 3",
        provider="Google",
        api_type="image",
        quota_type="daily",
        quota_limit=50,
        requires_proxy=False,
        strengths=["高质量", "文字渲染好"],
        weaknesses=["新模型"]
    ),

    # ===== 视频模型 =====
    "runway-gen3": ModelInfo(
        name="Gen-3 Alpha",
        provider="Runway",
        api_type="video",
        quota_type="free-tier",
        quota_limit=125,
        requires_proxy=False,
        strengths=["AI视频", "特效强"],
        weaknesses=["额度有限"]
    ),
    "pika-1": ModelInfo(
        name="Pika 1.0",
        provider="Pika",
        api_type="video",
        quota_type="free-tier",
        quota_limit=150,
        requires_proxy=False,
        strengths=["文字转视频", "易用"],
        weaknesses=["质量一般"]
    ),

    # ===== 聚合平台 =====
    "openrouter": ModelInfo(
        name="OpenRouter",
        provider="OpenRouter",
        api_type="aggregator",
        quota_type="multi",
        quota_limit=0,
        requires_proxy=False,
        strengths=["聚合50+模型", "方便切换", "可设每日上限"],
        weaknesses=["需要付费", "第三方"]
    ),
}


class PoorManRouter:
    """
    穷鬼智能模型路由

    特点：
    - 只用免费额度
    - 自动选择最优模型
    - 额度用完自动切换
    - 监控使用量
    """

    def __init__(self, data_dir: Optional[Path] = None):
        if data_dir is None:
            data_dir = Path.home() / ".openclaw" / "workspace" / ".router"
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.state_file = self.data_dir / "state.json"
        self.log_file = self.data_dir / "usage_log.json"
        self.state = self._load_state()
        self.models = {k: v for k, v in FREE_MODELS.items()}

    def _load_state(self) -> Dict:
        if self.state_file.exists():
            return json.loads(self.state_file.read_text())
        return {
            "usage": {},
            "last_reset": datetime.now().isoformat(),
            "total_requests": 0
        }

    def _save_state(self):
        self.state_file.write_text(json.dumps(self.state, ensure_ascii=False, indent=2))

    def select_model(self, task_type: str = "chat", prefer_provider: str = "") -> Optional[ModelInfo]:
        """
        为任务选择最合适的免费模型

        Args:
            task_type: "chat" / "image" / "video"
            prefer_provider: 偏好提供商（可选）

        Returns:
            ModelInfo 或 None（没有可用模型）
        """
        # 筛选可用模型
        candidates = []
        for key, model in self.models.items():
            if model.api_type != task_type:
                continue
            if not model.is_available:
                continue
            if model.quota_remaining <= 0:
                continue

            score = 0

            # 偏好提供商
            if prefer_provider and model.provider == prefer_provider:
                score += 10

            # 额度越多越好
            score += model.quota_remaining / 10

            # 有墙的扣分
            if model.requires_proxy:
                score -= 5

            candidates.append((score, key, model))

        if not candidates:
            return None

        # 选择得分最高的
        candidates.sort(reverse=True)
        return candidates[0][2]

    def record_usage(self, model_key: str, tokens: int = 1):
        """记录使用量"""
        if model_key not in self.state["usage"]:
            self.state["usage"][model_key] = 0
        self.state["usage"][model_key] += tokens
        self.state["total_requests"] += 1
        self._save_state()

    def get_status(self) -> Dict:
        """获取所有模型状态"""
        status = []
        for key, model in self.models.items():
            status.append({
                "key": key,
                "name": model.name,
                "provider": model.provider,
                "type": model.api_type,
                "quota_type": model.quota_type,
                "remaining": model.quota_remaining,
                "limit": model.quota_limit,
                "percent": model.quota_percent,
                "available": model.quota_remaining > 0,
                "requires_proxy": model.requires_proxy
            })
        return status

    def get_best_for_task(self, task: str) -> Dict:
        """
        根据任务描述推荐模型

        Returns:
            推荐的模型和使用建议
        """
        task_lower = task.lower()

        # 判断任务类型
        if any(kw in task_lower for kw in ["画", "图片", "image", "生成图"]):
            api_type = "image"
        elif any(kw in task_lower for kw in ["视频", "video"]):
            api_type = "video"
        else:
            api_type = "chat"

        # 根据关键词判断偏好
        prefer = ""
        if any(kw in task_lower for kw in ["代码", "编程", "code", "program"]):
            prefer = "Groq"
        elif any(kw in task_lower for kw in ["中文", "写作", "文章"]):
            prefer = "硅基流动"

        model = self.select_model(api_type, prefer)

        if not model:
            return {
                "task_type": api_type,
                "recommend": None,
                "suggestion": "所有模型额度已用完，请明天再来"
            }

        return {
            "task_type": api_type,
            "recommend": asdict(model),
            "suggestion": f"推荐 {model.provider} {model.name}（剩余 {model.quota_remaining:.0f} {model.quota_type}）"
        }


def main():
    """演示"""
    print("=" * 60)
    print("GMS 穷鬼智能模型路由")
    print("=" * 60)

    router = PoorManRouter()

    # 显示状态
    print("\n📊 模型额度状态:")
    status = router.get_status()

    by_type = {"chat": [], "image": [], "video": []}
    for s in status:
        by_type[s["type"]].append(s)

    for t, models in by_type.items():
        print(f"\n【{t.upper()}】")
        for m in models[:5]:  # 每类显示5个
            icon = "✅" if m["available"] else "❌"
            proxy = "(需代理)" if m["requires_proxy"] else ""
            print(f"  {icon} {m['provider']} {m['name']} {proxy}")
            print(f"      剩余: {m['remaining']:.0f}/{m['limit']} ({m['percent']:.0f}%)")

    # 任务测试
    print("\n" + "=" * 60)
    print("🔍 任务推荐测试:")
    print("=" * 60)

    tests = ["帮我写一段Python代码", "画一幅风景画", "写一篇中文文章"]
    for t in tests:
        result = router.get_best_for_task(t)
        print(f"\n任务: {t}")
        print(f"  类型: {result['task_type']}")
        print(f"  建议: {result['suggestion']}")


if __name__ == "__main__":
    main()
