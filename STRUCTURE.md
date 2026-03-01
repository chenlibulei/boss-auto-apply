# 目录结构

```
boss-auto-apply/
├── SKILL.md                      # 技能说明文档（必需）
├── README.md                     # 使用说明
├── config/
│   ├── coordinates.json          # 坐标配置
│   └── filter-rules.json         # 筛选规则配置
├── scripts/
│   └── boss_auto_apply.py        # 主脚本
├── templates/
│   └── greeting-template.md      # 招呼语模板
├── references/
│   └── resume.md                 # 黎哥简历信息
└── STRUCTURE.md                  # 本文件
```

---

## 文件说明

### 核心文件

| 文件 | 说明 | 是否必需 |
|------|------|----------|
| `SKILL.md` | 技能说明文档，OpenClaw 识别技能用 | ✅ 必需 |
| `scripts/boss_auto_apply.py` | 主脚本，执行自动投递 | ✅ 必需 |

### 配置文件

| 文件 | 说明 | 何时修改 |
|------|------|----------|
| `config/coordinates.json` | 屏幕坐标配置 | 点击位置不准确时 |
| `config/filter-rules.json` | 筛选条件配置 | 需要调整筛选条件时 |

### 模板文件

| 文件 | 说明 | 何时修改 |
|------|------|----------|
| `templates/greeting-template.md` | 招呼语生成模板 | 需要调整招呼语风格时 |
| `references/resume.md` | 黎哥简历信息 | 简历更新时 |

### 文档文件

| 文件 | 说明 |
|------|------|
| `README.md` | 完整使用说明 |
| `STRUCTURE.md` | 目录结构说明 |

---

## 使用流程

1. **首次使用**
   - 阅读 `README.md`
   - 安装依赖：`pip install pyautogui pyperclip pillow`
   - 校准坐标（如需要）

2. **测试模式**
   - 运行：`python scripts/boss_auto_apply.py --mode test --count 5`
   - 查看匹配结果和招呼语

3. **正式投递**
   - 运行：`python scripts/boss_auto_apply.py --mode apply --count 6`
   - 查看投递记录：`workspace/boss-apply-YYYY-MM-DD.csv`

---

## 配置说明

### 坐标配置 (`config/coordinates.json`)

```json
{
  "coordinates": {
    "returnButton": { "x": 23, "y": 57 },      // 返回按钮
    "jobCard": { "x": 432, "y": 340 },         // 职位卡片
    "immediateChat": { "x": 1336, "y": 333 },  // 立即沟通
    "continueChat": { "x": 1014, "y": 797 },   // 继续沟通
    "chatInput": { "x": 845, "y": 1299 }       // 聊天输入框
  },
  "scroll": {
    "distance": 180  // 滚动距离（像素）
  }
}
```

### 筛选规则 (`config/filter-rules.json`)

```json
{
  "salary": {
    "minUpperLimit": 14000  // 薪资上限最低要求
  },
  "cities": {
    "preferred": ["杭州", "宁波", "温州", ...]  // 优先城市
  },
  "blacklist": {
    "bigTech": [...],      // 大厂黑名单
    "outsourcing": [...]   // 外包黑名单
  }
}
```

---

## 输出文件

### 投递记录 (`workspace/boss-apply-YYYY-MM-DD.csv`)

```csv
日期，公司，岗位，薪资，学历，状态，招呼语
2026-03-01，高帆破浪科技，初级前端开发工程师，15-30K，本科，已投递，[已保存]
```

### 岗位截图 (`workspace/boss-apply-{1-6}.png`)

每个岗位投递前的截图，用于识别和记录。

---

## 更新技能

当需要更新技能时：

1. 修改对应文件
2. 测试验证
3. 更新 `README.md` 中的版本信息
4. 提交更改

---

## 故障排查

参考 `README.md` 中的"故障处理"章节。
