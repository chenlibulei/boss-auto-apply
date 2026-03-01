# 更新日志

## v1.0.2 (2026-03-01 15:28)

### 🐛 Bug 修复

**问题：** 投递完成后返回，直接滚动但没有先移动到卡片位置，导致滚动无效

**原流程（v1.0.1）：**
```
返回 → 直接滚动 → 点击
       ❌ 鼠标可能不在卡片位置，滚动无效
```

**修正后流程（v1.0.2）：**
```
返回 → 移动到卡片位置 → 滚动 → 等待 → 点击
       ✅ 确保鼠标在卡片位置，滚动后下一个卡片到位
```

**修改内容：**
```python
# 点击返回按钮后
print('  移动到职位卡片位置...')
pyautogui.moveTo(COORDS['jobCard']['x'], COORDS['jobCard']['y'])
time.sleep(0.5)

print('  滚动到下一个岗位...')
pyautogui.scroll(-SCROLL)
time.sleep(TIMING['afterScrollWait'] / 1000)

print('  点击下一个职位卡片...')
pyautogui.click(COORDS['jobCard']['x'], COORDS['jobCard']['y'])
time.sleep(TIMING['pageLoadWait'] / 1000)
```

---

## v1.0.1 (2026-03-01 15:20)

### 🐛 Bug 修复

**问题：** 投递完成后返回，缺少点击下一个职位卡片的操作，导致岗位信息对不上

**原流程：**
```
步骤 4：发送 → 点击返回 → (结束)
步骤 5：滚动 → 点击 (下一个循环)
```

**问题：** 步骤 4 返回后没有立即滚动和点击，导致步骤 5 的点击可能对准了错误的位置

**修正后流程：**
```
步骤 4（正式投递）：
  1. 发送消息
  2. 点击返回按钮
  3. 等待 1.5 秒
  4. 滚动 180px
  5. 点击下一个职位卡片 ← 新增！
  6. 等待 2 秒（页面加载）
```

**修改文件：**
- `scripts/boss_auto_apply.py` - apply_job() 方法

**修改内容：**
```python
def apply_job(self, greeting):
    # ... 发送消息 ...
    
    # 点击返回按钮
    pyautogui.click(COORDS['returnButton']['x'], COORDS['returnButton']['y'])
    time.sleep(TIMING['afterReturnWait'] / 1000)
    
    # 新增：滚动到下一个岗位并点击
    print('  滚动到下一个岗位...')
    pyautogui.scroll(-SCROLL)
    time.sleep(TIMING['afterScrollWait'] / 1000)
    
    print('  点击下一个职位卡片...')
    pyautogui.click(COORDS['jobCard']['x'], COORDS['jobCard']['y'])
    time.sleep(TIMING['pageLoadWait'] / 1000)
```

---

### 📊 流程对比

#### 修正前（有问题）
```
岗位 1 投递完成 → 返回 → [缺少滚动点击]
     ↓
岗位 2 点击 (432, 340) → ❌ 可能点错了位置
```

#### 修正后（正确）
```
岗位 1 投递完成 → 返回 → 滚动 180px → 点击下一个职位卡片
     ↓
岗位 2 已在详情页 → ✅ 正确识别
```

---

## v1.0.0 (2026-03-01 15:00)

### ✅ 初始版本

- 基础框架完成
- 坐标配置化
- 筛选规则配置化
- 招呼语生成
- 测试模式和正式投递模式
- CSV 记录保存

---

## 待优化

- [ ] 集成真实图像识别 API
- [ ] 去重逻辑（避免同一家公司重复投递）
- [ ] 错误重试机制
- [ ] 详细日志输出
