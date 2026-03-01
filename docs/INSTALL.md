# OpenClaw 用户安装指南

本指南帮助 OpenClaw 用户快速安装和使用 BOSS 直聘自动投递 Agent。

---

## 📦 方式一：通过 OpenClaw Skill Hub 安装（推荐）

**如果此 Skill 已发布到 Skill Hub：**

```
用户：帮我安装 boss-auto-apply

OpenClaw: 正在安装 boss-auto-apply Skill...
✅ 安装完成！
```

然后在对话中直接使用：
```
用户：测试 BOSS 直聘自动投递，测试 5 个岗位
```

---

## 📦 方式二：手动安装（当前可用）

### 步骤 1：下载 Skill

**方式 A - Git 克隆：**
```bash
# 进入 OpenClaw workspace
cd C:\Users\chen\.openclaw\workspace\skills

# 克隆仓库
git clone https://github.com/chenlibulei/boss-auto-apply.git
```

**方式 B - 下载 ZIP：**
1. 访问：https://github.com/chenlibulei/boss-auto-apply
2. 点击 "Code" → "Download ZIP"
3. 解压到 `C:\Users\chen\.openclaw\workspace\skills\boss-auto-apply`

### 步骤 2：安装依赖

```bash
cd C:\Users\chen\.openclaw\workspace\skills\boss-auto-apply
pip install -r requirements.txt
```

**依赖说明：**
- `pyautogui` - 鼠标键盘自动化（必需）
- `pyperclip` - 剪贴板操作（必需）
- `pillow` - 图像处理（必需）
- `dashscope` - 百炼 API 客户端（可选）
- `python-dotenv` - 环境变量管理（可选）

### 步骤 3：配置个人信息

```bash
# 复制配置模板
cp config/user_config.example.json config/user_config.json
```

**编辑 `config/user_config.json`：**

```json
{
  "user": {
    "name": "你的名字",          // 你的称呼
    "title": "前端开发工程师",     // 当前职位
    "years_of_experience": 5,    // 工作年限
    "dev_years": 3               // 开发年限
  },
  "job_preferences": {
    "salary": {
      "min_upper_limit": 14000   // 最低薪资要求
    },
    "cities": {
      "preferred": ["杭州", "上海"]  // 期望城市
    }
  },
  "skills": {
    "proficient": ["React", "Vue"],  // 你的核心技能
    "familiar": ["Node.js"]
  },
  "greeting_style": {
    "assistant_name": "小助手"  // AI 助手名称
  }
}
```

### 步骤 4：配置 API Key（可选）

如果需要使用图像识别和个性化招呼语生成：

```bash
# 复制配置模板
cp config/.env.example config/.env
```

**编辑 `config/.env`：**
```bash
DASHSCOPE_API_KEY=sk-your-api-key-here
```

**获取 API Key：**
1. 访问：https://dashscope.console.aliyun.com/apiKey
2. 登录/注册阿里云账号
3. 创建 API Key
4. 复制到 `.env` 文件

**注意：** 不配置 API Key 也可以使用，但会使用模板生成招呼语。

### 步骤 5：校准坐标

**重要：** 首次使用前必须校准坐标！

```bash
# 编辑 config/coordinates.json
```

**校准方法：**

1. **打开 BOSS 直聘网页**
   ```
   在浏览器中打开：https://www.zhipin.com
   ```

2. **获取坐标**
   ```python
   import pyautogui
   print(pyautogui.position())  # 移动鼠标查看实时坐标
   ```

3. **更新配置**
   ```json
   {
     "coordinates": {
       "jobCard": { "x": 你的 X, "y": 你的 Y },
       "immediateChat": { "x": 你的 X, "y": 你的 Y },
       "chatInput": { "x": 你的 X, "y": 你的 Y }
     },
     "scroll": {
       "distance": 180
     }
   }
   ```

### 步骤 6：开始使用

**在 OpenClaw 对话中：**

**测试模式：**
```
用户：测试 BOSS 直聘自动投递，测试 5 个岗位

Agent: 好的！开始测试 BOSS 直聘自动投递...

[岗位 1/5] 开始处理...
✅ 符合条件
招呼语预览：您好，我是小助手...

[岗位 2/5] ...
```

**正式投递：**
```
用户：开始正式投递，投递 6 个岗位

Agent: 好的！开始正式投递 6 个岗位...

[岗位 1/6] 已投递 ✅
[岗位 2/6] 已投递 ✅
...
```

**查看记录：**
```
用户：查看今天的投递记录

Agent: 这是今天的投递记录：
日期，公司，岗位，薪资，状态
2026-03-02，某某科技，前端工程师，15-25K，已投递
...
```

---

## 🔧 故障排查

### 问题 1：点击位置不准确

**症状：** 点击后没有反应或点错位置

**解决：**
1. 重新校准坐标
2. 确保 BOSS 直聘网页已打开
3. 确保浏览器窗口在最前面

### 问题 2：薪资解析失败

**症状：** 提示"薪资信息无法解析"

**解决：**
1. 检查薪资格式是否为 "15-25K" 或 "15-25K·13 薪"
2. 如果是其他格式，在 `salary_parser.py` 中添加解析规则

### 问题 3：API 调用失败

**症状：** "API 调用失败" 或 "未配置 API Key"

**解决：**
1. 检查 `config/.env` 是否存在
2. 检查 API Key 是否正确
3. 检查网络连接

### 问题 4：招呼语生成失败

**症状：** "大模型生成失败"

**解决：**
1. 检查 API Key 配置
2. 检查 API 余额是否充足
3. 系统会自动回退到模板生成

---

## 📝 配置说明

### 用户配置 (`config/user_config.json`)

| 配置项 | 说明 | 示例 |
|--------|------|------|
| `user.name` | 你的称呼 | "黎哥" |
| `user.title` | 当前职位 | "前端开发组长" |
| `job_preferences.salary.min_upper_limit` | 最低薪资要求 | 14000 |
| `job_preferences.cities.preferred` | 期望城市 | ["杭州", "上海"] |
| `skills.proficient` | 核心技能 | ["React", "Vue"] |
| `greeting_style.assistant_name` | AI 助手名称 | "小助手" |

### 坐标配置 (`config/coordinates.json`)

| 配置项 | 说明 | 默认值 |
|--------|------|--------|
| `jobCard` | 职位卡片坐标 | (432, 340) |
| `immediateChat` | 立即沟通按钮 | (1336, 333) |
| `chatInput` | 聊天输入框 | (845, 1299) |
| `scroll.distance` | 滚动距离 | 180 |

---

## 🎯 最佳实践

### 1. 首次使用

1. **完整测试流程**
   ```
   测试 BOSS 直聘自动投递，测试 3 个岗位
   ```

2. **检查招呼语**
   - 确认称呼正确
   - 确认技能匹配
   - 确认语气合适

3. **调整配置**
   - 修改 `user_config.json`
   - 重新测试

### 2. 日常使用

1. **早上 9 点开始投递**
   ```
   开始正式投递，投递 10 个岗位
   ```

2. **下午查看回复**
   ```
   检查 BOSS 直聘消息
   ```

3. **每周统计**
   ```
   查看本周投递记录
   ```

### 3. 安全提示

1. **每日投递限制** - 建议不超过 20 个
2. **API Key 保密** - 不要分享给他人
3. **个人信息保护** - `user_config.json` 不要上传
4. **定期清理日志** - `logs/` 目录定期清理

---

## 📞 获取帮助

### 文档

- **README.md** - 完整使用说明
- **SKILL.md** - OpenClaw Skill 说明
- **config/user_config.example.json** - 配置示例

### 在线支持

- **GitHub Issues:** https://github.com/chenlibulei/boss-auto-apply/issues
- **GitHub 仓库:** https://github.com/chenlibulei/boss-auto-apply
- **OpenClaw 文档:** https://docs.openclaw.ai

### 常见问题

查看 README.md 中的 "常见问题" 章节。

---

## 🔄 更新 Skill

```bash
cd C:\Users\chen\.openclaw\workspace\skills\boss-auto-apply
git pull origin main
```

**注意：** 更新前备份你的配置文件：
```bash
cp config/user_config.json config/user_config.json.bak
cp config/.env config/.env.bak
```

---

**最后更新：** 2026-03-02  
**维护者：** @chenlibulei
