# 消息检查与回复功能

## 功能说明

投递完成后自动检查 HR 消息并回复。

---

## 坐标配置

消息按钮坐标已配置在 `config/coordinates.json`：

```json
{
  "messageButton": {
    "x": 1275,
    "y": 113,
    "description": "消息按钮 - 检查 HR 回复"
  }
}
```

---

## 工作流程

### 1. 检查消息按钮

截图消息按钮区域，检测是否有红色未读气泡。

```python
# 截取消息按钮周围 100x100 区域
screenshot = pyautogui.screenshot(region=(x-50, y-50, 100, 100))
```

### 2. 打开消息列表

如果有未读气泡，点击消息按钮。

```python
pyautogui.click(COORDS['messageButton']['x'], COORDS['messageButton']['y'])
```

### 3. 检查新消息

截图消息列表，识别新消息。

### 4. 回复 HR

如果有新消息，自动回复。

```python
# 默认回复内容
message = '您好，感谢您的关注！我会尽快查看并回复。'
```

---

## 使用方法

### 方式一：投递完成后自动检查

```bash
python scripts/boss_auto_apply.py --mode apply --count 6
# 投递完成后自动调用 check_and_reply()
```

### 方式二：手动检查

```bash
python scripts/check_message.py
```

---

## 自定义回复内容

编辑 `scripts/check_message.py`：

```python
def reply_to_hr(message='自定义回复内容'):
    """回复 HR 消息"""
    # ...
```

---

## 图像识别（待实现）

当前版本使用简化逻辑（假设总有消息），需要实现：

### 1. 检测红色气泡

```python
# 分析截图中的红色区域
# 如果有红色圆形区域，说明有未读消息
```

### 2. 识别新消息

```python
# 分析消息列表页面
# 识别带有"新"标签的消息
```

---

## 坐标校准

如果消息按钮位置不准确：

1. 打开 BOSS 直聘网页
2. 鼠标移动到消息按钮
3. 运行命令获取坐标：
   ```python
   import pyautogui
   print(pyautogui.position())
   ```
4. 更新 `config/coordinates.json`：
   ```json
   {
     "messageButton": { "x": 新 X, "y": 新 Y }
   }
   ```

---

## 注意事项

1. **首次使用前**必须校准消息按钮坐标
2. **图像识别**功能待实现，当前为简化版本
3. **回复内容**可根据需要自定义
4. **检查频率**建议不要过于频繁

---

## 输出文件

| 文件 | 说明 |
|------|------|
| `workspace/message-button-check.png` | 消息按钮截图 |
| `workspace/message-list.png` | 消息列表截图 |

---

## 示例流程

```
投递完成！
共投递 6 个岗位

检查 HR 消息回复...
==================================================
开始检查消息并回复
==================================================

正在检查消息按钮...
消息按钮截图已保存：message-button-check.png
点击消息按钮...
已打开消息列表
检查新消息...
消息列表截图已保存：message-list.png
回复 HR 消息...
消息已发送

消息回复完成！
==================================================
```

---

## 待实现功能

- [ ] 图像识别红色气泡
- [ ] 识别新消息标签
- [ ] 智能回复（根据 HR 消息内容）
- [ ] 多消息处理
- [ ] 消息分类（面试邀请、咨询等）
