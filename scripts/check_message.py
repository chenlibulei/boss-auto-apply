#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
检查 BOSS 直聘消息并回复
"""

import pyautogui
import time
from pathlib import Path

pyautogui.FAILSAFE = False

WORKSPACE_ROOT = Path('C:/Users/chen/.openclaw/workspace')

# 加载配置
import json
CONFIG_PATH = Path(__file__).parent / 'config' / 'coordinates.json'
with open(CONFIG_PATH, 'r', encoding='utf-8') as f:
    config = json.load(f)

COORDS = config['coordinates']


def check_message_button():
    """检查消息按钮是否有未读气泡"""
    print('正在检查消息按钮...')
    
    # 截图消息按钮区域
    x, y = COORDS['messageButton']['x'], COORDS['messageButton']['y']
    # 截取按钮周围 100x100 区域
    screenshot = pyautogui.screenshot(region=(x-50, y-50, 100, 100))
    path = WORKSPACE_ROOT / 'message-button-check.png'
    screenshot.save(str(path))
    print(f'消息按钮截图已保存：{path}')
    
    # TODO: 使用图像识别检测是否有红色气泡
    # 简化版本：让用户确认
    return True  # 假设有消息


def open_message():
    """点击消息按钮"""
    print('点击消息按钮...')
    pyautogui.click(COORDS['messageButton']['x'], COORDS['messageButton']['y'])
    time.sleep(2)
    print('已打开消息列表')


def check_new_messages():
    """检查是否有新消息"""
    print('检查新消息...')
    # 截图消息列表页面
    screenshot = pyautogui.screenshot()
    path = WORKSPACE_ROOT / 'message-list.png'
    screenshot.save(str(path))
    print(f'消息列表截图已保存：{path}')
    
    # TODO: 使用图像识别检测新消息
    return True  # 假设有新消息


def reply_to_hr(message='您好，感谢您的关注！我会尽快查看并回复。'):
    """回复 HR 消息"""
    import pyperclip
    
    print('回复 HR 消息...')
    
    # 复制回复内容
    pyperclip.copy(message)
    
    # 点击聊天输入框
    pyautogui.click(COORDS['chatInput']['x'], COORDS['chatInput']['y'])
    time.sleep(0.5)
    
    # 粘贴
    pyautogui.hotkey('ctrl', 'v')
    time.sleep(0.5)
    
    # 发送
    pyautogui.press('enter')
    time.sleep(1)
    
    print('消息已发送')


def check_and_reply():
    """完整流程：检查消息并回复"""
    print('\n' + '='*50)
    print('开始检查消息并回复')
    print('='*50 + '\n')
    
    # 步骤 1：检查消息按钮
    has_unread = check_message_button()
    
    if has_unread:
        # 步骤 2：打开消息
        open_message()
        
        # 步骤 3：检查新消息
        has_new = check_new_messages()
        
        if has_new:
            # 步骤 4：回复
            reply_to_hr()
            print('\n消息回复完成！')
        else:
            print('\n没有新消息')
    else:
        print('\n没有未读消息')
    
    print('\n' + '='*50)


if __name__ == '__main__':
    check_and_reply()
