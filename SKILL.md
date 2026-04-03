# Poor Man's Router - 穷鬼智能模型路由

> 专为初学者和小用量用户设计的免费AI模型路由

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## 功能特点

- 🎯 **智能选择** - 根据任务类型自动选择最优免费模型
- 💰 **免费优先** - 专门聚合每日免费额度模型
- 📊 **额度监控** - 追踪使用量，用完自动切换
- 🔄 **自动切换** - 额度用完自动切到下一个最优模型
- 🌐 **无需代理** - 大部分模型不需要代理

## 支持的模型

### 文本模型 (Chat)

| 模型 | 提供商 | 每日免费额度 | 需要代理 |
|------|--------|-------------|---------|
| Llama 3.3 70B | Groq | 1440次/天 | ❌ |
| Mixtral 8x7B | Groq | 1440次/天 | ❌ |
| Gemma 2 9B | Groq | 1440次/天 | ❌ |
| Command R+ | Cohere | 1000次/月 | ❌ |
| Gemini Pro | Google | 60 RPM | ❌ |

### 图像模型 (Image)

| 模型 | 提供商 | 每日免费额度 | 需要代理 |
|------|--------|-------------|---------|
| Flux Dev | Fal | 100次/天 | ❌ |
| Imagen 3 | Google | 50次/天 | ❌ |
| DALL-E 3 | OpenAI | $5额度 | ✅ |

### 视频模型 (Video)

| 模型 | 提供商 | 免费额度 | 需要代理 |
|------|--------|---------|---------|
| Gen-3 Alpha | Runway | 125 credits | ❌ |
| Pika 1.0 | Pika | 150 credits | ❌ |

## 安装

```bash
pip install requests
```

或直接下载 `poor_mans_router.py` 单独使用。

## 快速开始

```python
from poor_mans_router import PoorManRouter

router = PoorManRouter()

# 1. 根据任务自动推荐
result = router.get_best_for_task("帮我写Python代码")
print(result['suggestion'])

# 2. 选择模型
model = router.select_model("chat")
print(f"使用: {model.name}")

# 3. 记录使用
router.record_usage("groq-llama-3.3-70b", tokens=100)
```

## 使用示例

### 例1：自动选择最优免费模型

```python
from poor_mans_router import PoorManRouter

router = PoorManRouter()

# 对于"写代码"任务
result = router.get_best_for_task("写一个排序算法")
# 输出: 推荐 Groq Llama 3.3 70B（剩余 1440 daily）

# 对于"画图"任务
result = router.get_best_for_task("画一幅风景画")
# 输出: 推荐 Fal Flux Dev（剩余 100 daily）
```

### 例2：查看所有模型状态

```python
router = PoorManRouter()
status = router.get_status()

for s in status:
    if s['available']:
        print(f"{s['provider']} {s['name']}: {s['percent']:.0f}%")
```

### 例3：任务路由

```python
# 简单任务 → 小模型（快）
# 复杂任务 → 大模型（准）

result = router.get_best_for_task("今天天气")
# → 选轻量快速的模型

result = router.get_best_for_task("分析这篇长文章的核心观点")
# → 选能力强的模型
```

## 配置

### 修改模型额度

编辑 `FREE_MODELS` 字典：

```python
FREE_MODELS = {
    "my-model": ModelInfo(
        name="我的模型",
        provider="我的提供商",
        api_type="chat",
        quota_type="daily",
        quota_limit=100,  # 每天100次
        requires_proxy=False,
    ),
}
```

### 修改数据目录

```python
from pathlib import Path
router = PoorManRouter(data_dir=Path("/my/data/path"))
```

## API 参考

### PoorManRouter

#### `select_model(task_type, prefer_provider)`

选择最合适的模型

- `task_type`: "chat" / "image" / "video"
- `prefer_provider`: 可选，偏好的提供商名称

返回 `ModelInfo` 或 `None`

#### `get_best_for_task(task_description)`

根据任务描述推荐模型

```python
result = router.get_best_for_task("写一篇科技文章")
# {
#     "task_type": "chat",
#     "recommend": {...},  # ModelInfo dict
#     "suggestion": "推荐 Groq Llama 3.3 70B"
# }
```

#### `record_usage(model_key, tokens)`

记录使用量

#### `get_status()`

获取所有模型的状态

### ModelInfo

```python
@dataclass
class ModelInfo:
    name: str           # 模型名称
    provider: str       # 提供商
    api_type: str       # "chat" / "image" / "video"
    quota_type: str     # "daily" / "monthly" / "one-time"
    quota_limit: float  # 额度上限
    quota_used: float   # 已用额度
    quota_remaining     # 属性，剩余额度
    requires_proxy: bool  # 是否需要代理
```

## 工作原理

```
用户任务
    ↓
解析任务类型（chat/image/video）
    ↓
根据关键词判断（代码/中文/画图等）
    ↓
筛选可用模型（额度>0）
    ↓
评分排序（额度多+无代理+匹配偏好）
    ↓
返回最优模型
```

## 适用人群

- ✅ 初学者（不想花太多钱）
- ✅ 小用量用户（每天几到几十次调用）
- ✅ 学生（学习和实验）
- ✅ 开发者（快速原型）

## 不适用

- ❌ 日均调用超过1000次（建议用付费API）
- ❌ 生产环境（建议用稳定付费服务）
- ❌ 需要高可用性（免费额度不稳定）

## 更新日志

### v1.0.0 (2026-04-02)
- 初始版本
- 支持 Groq、Cohere、Google AI Studio
- 支持图像和视频模型
- 额度追踪和自动切换

## 贡献

欢迎提交 Issue 和 PR！

## License

MIT License
