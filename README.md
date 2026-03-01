# BOSS 直聘自动投递 Agent

💼 自动筛选并投递符合前端开发条件的 BOSS 直聘岗位

**版本：** v1.0.4  
**状态：** ✅ 可用（Alpha）  
**适用：** OpenClaw 用户

---

## 🎯 功能特点

- ✅ **自动识别岗位信息** - 公司、薪资、学历、技术要求等
- ✅ **智能匹配筛选** - 薪资、城市、公司类型、学历等
- ✅ **个性化招呼语生成** - 基于岗位职责和用户简历匹配
- ✅ **支持测试/正式模式** - 测试模式只生成不投递
- ✅ **自动记录投递结果** - CSV 格式，方便统计
- ✅ **HR 消息检查与回复** - 自动检查并回复 HR 消息
- ✅ **API 限流保护** - 避免频繁调用被封禁

---

## 🚀 快速开始

### 📦 OpenClaw 用户安装

**详细的 OpenClaw 安装指南：** [docs/INSTALL.md](docs/INSTALL.md)

**快速安装：**
```bash
# 1. 下载 Skill
cd C:\Users\chen\.openclaw\workspace\skills
git clone https://github.com/chenlibulei/boss-auto-apply.git

# 2. 安装依赖
cd boss-auto-apply
pip install -r requirements.txt

# 3. 运行配置向导（推荐）
python setup.py

# 4. 开始使用
python scripts/boss_auto_apply.py --mode test --count 5
```

---

### 🎯 配置向导（推荐）

**首次使用建议运行配置向导：**

```bash
python setup.py
```

**向导会帮助你配置：**

1. ✅ **选择图像识别模型提供商**
   - 阿里云百炼 (qwen-vl-plus) - 推荐
   - OpenAI (gpt-4o)
   - Anthropic (Claude 3.5)
   - 本地模型 (Ollama)

2. ✅ **选择文本生成模型提供商**
   - 阿里云百炼 (qwen3.5-plus)
   - OpenAI (gpt-4o-mini)
   - Anthropic (Claude 3.5)
   - 本地模型

3. ✅ **配置 API Key**
   - 根据选择的提供商配置对应的 API Key

4. ✅ **配置个人信息**
   - 你的称呼
   - 当前职位
   - 工作年限
   - 期望城市
   - 核心技能
   - AI 助手名称

**配置完成后会自动保存：**
- `config/.env` - AI 模型配置
- `config/user_config.json` - 个人信息配置
- `.gitignore` - 保护敏感信息

---

### 📝 手动配置

如果不想使用配置向导，可以手动配置：

**1. 复制配置模板**
```bash
cp config/ai_models.env config/.env
cp config/user_config.example.json config/user_config.json
```

**2. 编辑配置文件**

**config/.env:**
```bash
# 选择模型提供商
IMAGE_MODEL_PROVIDER=dashscope
TEXT_MODEL_PROVIDER=dashscope

# 配置 API Key
DASHSCOPE_API_KEY=sk-your-api-key-here
```

**config/user_config.json:**
```json
{
  "user": {
    "name": "你的名字",
    "title": "前端开发工程师"
  }
}
```

---

### 1. 安装依赖

```bash
cd skills/boss-auto-apply
pip install -r requirements.txt
```

**依赖说明：**
- `pyautogui` - 鼠标键盘自动化
- `pyperclip` - 剪贴板操作
- `pillow` - 图像处理
- `dashscope` - 百炼 API 客户端（可选，用于图像识别和招呼语生成）
- `python-dotenv` - 环境变量管理

### 2. 配置 API Key（推荐）

如果需要使用**图像识别岗位信息**和**个性化招呼语生成**：

```bash
# 复制配置模板
cp config/.env.example config/.env

# 编辑 .env 文件，填入你的 API Key
# 获取地址：https://dashscope.console.aliyun.com/apiKey
DASHSCOPE_API_KEY=sk-your-api-key-here
```

**API 用途：**
- 📸 **图像识别** - 识别 BOSS 直聘岗位详情页（公司、薪资、职责等）
- 💬 **招呼语生成** - 基于岗位要求生成个性化招呼语

**注意：** 不配置 API Key 也可以使用，但会：
- 使用模拟数据进行岗位识别（需要手动输入）
- 使用模板生成招呼语（不够个性化）

### 3. 个性化配置

**复制用户配置模板：**
```bash
cp config/user_config.example.json config/user_config.json
```

**编辑 `config/user_config.json`：**

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
      "preferred": ["杭州", "宁波"]  // 优先城市
    }
  },
  "skills": {
    "proficient": ["React", "Vue"],  // 熟练掌握的技能
    "familiar": ["Node.js"]          // 熟悉的技能
  },
  "greeting_style": {
    "assistant_name": "小虾"         // AI 助手名称
  }
}
```

**配置说明：**
- `user.name` - 你的称呼（如"黎哥"）
- `job_preferences.salary.min_upper_limit` - 最低薪资要求
- `job_preferences.cities.preferred` - 期望工作城市
- `skills.proficient` - 你的核心技能栈
- `greeting_style.assistant_name` - AI 助手名称

### 4. 校准坐标

**重要：** 首次使用前必须校准坐标！

```bash
# 打开 BOSS 直聘网页
# 鼠标移动到各个按钮位置，记录坐标

# 编辑 config/coordinates.json
{
  "jobCard": { "x": 432, "y": 340 },      // 职位卡片
  "immediateChat": { "x": 1336, "y": 333 }, // 立即沟通
  "chatInput": { "x": 845, "y": 1299 }    // 聊天输入框
}
```

**坐标校准工具：**
```python
import pyautogui
print(pyautogui.position())  # 移动鼠标查看坐标
```

### 5. 运行测试

**测试模式（只识别不投递）：**
```bash
python scripts/boss_auto_apply.py --mode test --count 5
```

**正式投递：**
```bash
python scripts/boss_auto_apply.py --mode apply --count 6
```

---

## 📋 筛选条件

所有筛选条件可在 `config/user_config.json` 中配置：

| 条件 | 默认值 | 配置项 |
|------|--------|--------|
| 💰 薪资 | 上限≥14k | `job_preferences.salary.min_upper_limit` |
| 📍 城市 | 杭州及周边 | `job_preferences.cities.preferred` |
| ❌ 公司类型 | 排除大厂/外包 | `blacklist.big_tech` / `blacklist.outsourcing` |
| ❌ 岗位类型 | 正式岗 | `job_preferences.job_types` |
| 📚 学历 | 不要求硕士以上 | `job_preferences.education` |

### 公司黑名单（可配置）

**大厂黑名单：**
阿里、腾讯、字节、华为、美团、京东、拼多多、网易、快手、哔哩哔哩

**外包黑名单：**
中软国际、软通动力、文思海辉、法本信息、外服、人瑞、中科软、海隆软件

---

## 🤖 招呼语生成

### 生成方式

**方式一：大模型生成（推荐）**
- 需要配置 API Key
- 基于岗位职责和用户简历个性化生成
- 自动匹配技能点

**方式二：模板生成（回退方案）**
- 无需 API Key
- 使用通用模板
- 根据岗位名称突出对应技能

### 招呼语风格（可配置）

在 `config/user_config.json` 中配置：

```json
{
  "greeting_style": {
    "assistant_name": "小虾",
    "tone": "专业、真诚",
    "avoid_words": ["精通", "专家", "大师", "顶尖"],
    "preferred_words": ["熟练掌握", "熟悉", "有经验"]
  }
}
```

---

## 📁 项目结构

```
boss-auto-apply/
├── SKILL.md                          # OpenClaw 技能说明
├── README.md                         # 本文件
├── requirements.txt                  # Python 依赖
├── config/
│   ├── .env.example                  # API 配置模板
│   ├── coordinates.json              # 坐标配置
│   ├── filter-rules.json             # 筛选规则
│   └── user_config.example.json      # 用户配置模板 ⭐
├── scripts/
│   ├── boss_auto_apply.py            # 主脚本
│   ├── salary_parser.py              # 薪资解析
│   ├── logger.py                     # 日志系统
│   ├── greeting_generator.py         # 招呼语生成
│   ├── api_client.py                 # API 客户端
│   └── check_message.py              # 消息检查
├── templates/
│   └── greeting-template.md          # 招呼语模板
└── references/
    └── resume.md                     # 简历信息（可替换）
```

---

## 🔧 高级配置

### 日志系统

日志文件保存在 `logs/` 目录：

```bash
logs/boss-auto-apply-2026-03-01.log
```

**日志级别：**
- DEBUG - 调试信息
- INFO - 普通信息
- WARNING - 警告
- ERROR - 错误
- CRITICAL - 严重错误

### 投递记录

投递记录保存在 workspace 根目录：

```bash
boss-apply-2026-03-01.csv
```

**CSV 格式：**
```csv
日期，公司，岗位，薪资，学历，状态，招呼语
2026-03-01，某某科技，前端开发工程师，15-25K，本科，已投递，[已保存]
```

### 坐标配置

所有坐标在 `config/coordinates.json` 中配置：

```json
{
  "coordinates": {
    "returnButton": { "x": 23, "y": 57 },
    "jobCard": { "x": 432, "y": 340 },
    "immediateChat": { "x": 1336, "y": 333 },
    "continueChat": { "x": 1014, "y": 797 },
    "chatInput": { "x": 845, "y": 1299 },
    "messageButton": { "x": 1275, "y": 113 }
  },
  "scroll": {
    "distance": 180
  }
}
```

---

## ⚠️ 注意事项

### 安全提示

1. **不要分享 API Key** - 将 `.env` 文件添加到 `.gitignore`
2. **不要分享个人信息** - 将 `user_config.json` 添加到 `.gitignore`
3. **每日投递限制** - 建议不超过 20 个，避免被平台限制
4. **屏幕分辨率** - 坐标基于特定分辨率，变化后需重新校准

### 常见问题

**Q: 点击位置不准确？**
A: 重新校准坐标，编辑 `config/coordinates.json`

**Q: 薪资解析失败？**
A: 检查薪资格式，支持 "15-25K"、"15-25K·13 薪" 等

**Q: 招呼语生成失败？**
A: 检查 API Key 配置，或切换到模板模式

**Q: 网络超时？**
A: 检查网络连接，或增加超时时间

---

## 🛠️ 待开发功能

以下功能已规划但尚未实现：

- [ ] 图像识别气泡检测（检测未读消息）
- [ ] 公司去重逻辑（避免重复投递）
- [ ] 错误处理与重试机制
- [ ] 智能回复（根据 HR 消息内容）
- [ ] 统计报告（投递成功率等）
- [ ] 坐标校准工具（GUI）

---

## 📝 更新日志

### v1.0.4 (2026-03-01)
- ✅ 新增：薪资解析功能
- ✅ 新增：日志系统
- ✅ 新增：大模型招呼语生成
- ✅ 新增：用户配置文件
- ✅ 新增：API 客户端
- ⏳ 待开发：错误处理

### v1.0.3 (2026-03-01)
- ✅ 新增：消息检查与回复

### v1.0.2 (2026-03-01)
- ✅ 修复：滚动前先移动到卡片位置

### v1.0.1 (2026-03-01)
- ✅ 修复：添加滚动和点击下一个

### v1.0.0 (2026-03-01)
- ✅ 初始版本

---

## 🤝 贡献指南

欢迎提交 Issue 和 Pull Request！

**开发环境设置：**
```bash
git clone https://github.com/chenlibulei/boss-auto-apply.git
cd boss-auto-apply
pip install -r requirements.txt
pip install pytest  # 可选，用于测试
```

---

## 📄 许可证

MIT License - 详见 [LICENSE](LICENSE) 文件

---

## 📞 支持

**问题反馈：** https://github.com/chenlibulei/boss-auto-apply/issues

**GitHub 仓库：** https://github.com/chenlibulei/boss-auto-apply

**OpenClaw 文档：** https://docs.openclaw.ai

---

## 🌟 致谢

- OpenClaw 框架
- 百炼 DashScope API
- 所有贡献者

---

**最后更新：** 2026-03-01  
**维护者：** @chenlibulei
