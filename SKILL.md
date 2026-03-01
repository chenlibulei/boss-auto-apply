---
name: boss-auto-apply
description: BOSS 直聘自动投递 Agent。自动筛选并投递符合用户条件的岗位。支持个性化配置（称呼、薪资、城市等）。
metadata:
  {
    "openclaw":
      {
        "emoji": "💼",
        "requires": { "config": ["browser.enabled"] }
      }
  }
---

# BOSS 直聘自动投递 Agent

**版本：** v1.0.4  
**状态：** ✅ 可用（Alpha）  
**适用：** OpenClaw 用户

---

## 🎯 功能

- ✅ 自动识别岗位信息
- ✅ 智能筛选（薪资、城市、公司、学历）
- ✅ 个性化招呼语生成
- ✅ 自动投递
- ✅ HR 消息检查与回复
- ✅ 投递记录保存

---

## 🚀 使用方式

### 前置条件

1. **安装 Python 依赖**
   ```bash
   cd skills/boss-auto-apply
   pip install -r requirements.txt
   ```

2. **配置 API Key（可选）**
   ```bash
   cp config/.env.example config/.env
   # 编辑 .env 填入 DASHSCOPE_API_KEY
   ```

3. **个性化配置**
   ```bash
   cp config/user_config.example.json config/user_config.json
   # 编辑 user_config.json 填入你的信息
   ```

4. **校准坐标**
   ```bash
   # 编辑 config/coordinates.json
   # 根据实际屏幕分辨率调整坐标
   ```

### 命令

**测试模式：**
```
测试 BOSS 直聘自动投递，测试 5 个岗位
```

**正式投递：**
```
开始正式投递，投递 6 个岗位
```

**查看投递记录：**
```
查看今天的投递记录
```

---

## ⚙️ 配置说明

### 1. 用户配置 (`config/user_config.json`)

**可配置项：**

```json
{
  "user": {
    "name": "黎哥",              // 你的称呼
    "title": "前端开发组长",       // 当前职位
    "years_of_experience": 11,   // 工作年限
    "dev_years": 6               // 开发年限
  },
  "job_preferences": {
    "salary": {
      "min_upper_limit": 14000   // 最低薪资上限（元）
    },
    "cities": {
      "preferred": ["杭州", "宁波"]  // 期望城市
    },
    "education": {
      "friendly": ["不限", "大专", "本科"]
    }
  },
  "skills": {
    "proficient": ["React", "Vue"],  // 熟练掌握
    "familiar": ["Node.js"]          // 熟悉
  },
  "greeting_style": {
    "assistant_name": "小虾"         // AI 助手名称
  }
}
```

### 2. 坐标配置 (`config/coordinates.json`)

```json
{
  "coordinates": {
    "jobCard": { "x": 432, "y": 340 },
    "immediateChat": { "x": 1336, "y": 333 },
    "chatInput": { "x": 845, "y": 1299 }
  },
  "scroll": {
    "distance": 180
  }
}
```

### 3. API 配置 (`config/.env`)

```bash
DASHSCOPE_API_KEY=sk-your-api-key-here
IMAGE_MODEL=qwen-vl-plus
TEXT_MODEL=qwen3.5-plus
```

---

## 📋 筛选条件

| 条件 | 默认值 | 配置项 |
|------|--------|--------|
| 💰 薪资 | 上限≥14k | `job_preferences.salary.min_upper_limit` |
| 📍 城市 | 杭州及周边 | `job_preferences.cities.preferred` |
| ❌ 公司类型 | 排除大厂/外包 | `blacklist` |
| ❌ 岗位类型 | 正式岗 | `job_preferences.job_types` |
| 📚 学历 | 不要求硕士以上 | `job_preferences.education` |

### 公司黑名单

**大厂：** 阿里、腾讯、字节、华为、美团、京东、拼多多、网易、快手、哔哩哔哩

**外包：** 中软国际、软通动力、文思海辉、法本信息、外服、人瑞、中科软、海隆软件

---

## 🤖 招呼语生成

### 生成方式

**大模型生成（推荐）：**
- 需要配置 API Key
- 基于岗位 + 简历个性化生成
- 自动匹配技能点

**模板生成（回退）：**
- 无需 API Key
- 使用通用模板

### 招呼语风格

在 `user_config.json` 中配置：

```json
{
  "greeting_style": {
    "assistant_name": "小虾",
    "tone": "专业、真诚",
    "avoid_words": ["精通", "专家", "大师"],
    "preferred_words": ["熟练掌握", "熟悉", "有经验"]
  }
}
```

---

## 📁 文件结构

```
boss-auto-apply/
├── SKILL.md                          # 本文件
├── README.md                         # 详细文档
├── requirements.txt                  # Python 依赖
├── config/
│   ├── .env.example                  # API 配置模板
│   ├── coordinates.json              # 坐标配置
│   └── user_config.example.json      # 用户配置模板 ⭐
├── scripts/
│   ├── boss_auto_apply.py            # 主脚本
│   ├── salary_parser.py              # 薪资解析
│   ├── logger.py                     # 日志系统
│   ├── greeting_generator.py         # 招呼语生成
│   └── api_client.py                 # API 客户端
└── templates/
    └── greeting-template.md          # 招呼语模板
```

---

## ⚠️ 注意事项

1. **首次使用前**必须校准坐标
2. **API Key 配置** - 将 `.env` 添加到 `.gitignore`
3. **个人信息** - 将 `user_config.json` 添加到 `.gitignore`
4. **每日投递限制** - 建议不超过 20 个
5. **屏幕分辨率** - 变化后需重新校准坐标

---

## 📝 更新日志

### v1.0.4 (2026-03-01)
- ✅ 新增：用户配置文件（称呼、薪资等可配置）
- ✅ 新增：薪资解析功能
- ✅ 新增：日志系统
- ✅ 新增：大模型招呼语生成
- ⏳ 待开发：错误处理

### v1.0.0-v1.0.3
- 初始版本及修复

---

## 🔗 链接

- **GitHub:** https://github.com/chenlibulei/boss-auto-apply
- **OpenClaw 文档:** https://docs.openclaw.ai
- **百炼 API:** https://dashscope.console.aliyun.com

---

**维护者：** @chenlibulei  
**最后更新：** 2026-03-01
