# 🪓 Poor Man's Router - 穷鬼智能模型路由

> 专为初学者和小用量用户设计的免费AI模型路由

[English](README_EN.md) | 中文

## ✨ 功能特点

- 🎯 **智能选择** - 根据任务类型自动选择最优免费模型
- 💰 **免费优先** - 专门聚合每日免费额度模型
- 📊 **额度监控** - 追踪使用量，用完自动切换
- 🔄 **自动切换** - 额度用完自动切到下一个最优模型
- 🌐 **无需代理** - 大部分模型不需要代理

## 🚀 快速开始

```bash
pip install poor-mans-router
```

```python
from poor_mans_router import PoorManRouter

router = PoorManRouter()

# 根据任务推荐模型
result = router.get_best_for_task("帮我写Python代码")
print(result['suggestion'])
```

## 📦 支持的模型

### 文本模型 (每日免费额度)

| 模型 | 提供商 | 每日额度 | 无代理 |
|------|--------|---------|--------|
| Llama 3.3 70B | Groq | 1440次/天 | ✅ |
| Mixtral 8x7B | Groq | 1440次/天 | ✅ |
| Gemma 2 9B | Groq | 1440次/天 | ✅ |
| Command R+ | Cohere | 1000次/月 | ✅ |
| Gemini Pro | Google | 60 RPM | ✅ |

### 图像模型

| 模型 | 提供商 | 每日额度 | 无代理 |
|------|--------|---------|--------|
| Flux Dev | Fal | 100次/天 | ✅ |
| Imagen 3 | Google | 50次/天 | ✅ |

### 视频模型

| 模型 | 提供商 | 免费额度 | 无代理 |
|------|--------|---------|--------|
| Gen-3 Alpha | Runway | 125 credits | ✅ |
| Pika 1.0 | Pika | 150 credits | ✅ |

## 📚 使用示例

```python
from poor_mans_router import PoorManRouter

router = PoorManRouter()

# 1. 任务推荐
result = router.get_best_for_task("写一篇科技文章")
# → 推荐 Groq Llama 3.3 70B（剩余 1440 daily）

# 2. 查看状态
status = router.get_status()
for s in status:
    if s['available']:
        print(f"{s['provider']} {s['name']}: {s['percent']:.0f}%")

# 3. 记录使用
router.record_usage("groq-llama-3.3-70b", tokens=100)
```

## 🎯 适用人群

- ✅ 初学者（不想花太多钱）
- ✅ 小用量用户（每天几到几十次调用）
- ✅ 学生（学习和实验）
- ✅ 开发者（快速原型）

## ❌ 不适用

- ❌ 日均调用超过1000次（建议用付费API）
- ❌ 生产环境（建议用稳定付费服务）

## 📂 项目结构

```
poor-mans-router/
├── SKILL.md              # 详细文档
├── README.md             # 本文件
├── poor_mans_router.py   # 核心代码
├── setup.py              # pip安装配置
└── examples.py           # 使用示例
```

## 🤝 贡献

欢迎提交 Issue 和 PR！

## 📄 License

MIT License

---

**声明：** 本项目仅供学习和研究使用。模型额度信息可能随提供商政策变化而变化，请以官方为准。
