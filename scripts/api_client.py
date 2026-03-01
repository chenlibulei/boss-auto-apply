#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
API 客户端 - 调用百炼 DashScope API

使用前请配置 API Key：
1. 复制 config/.env.example 为 config/.env
2. 填入你的 DASHSCOPE_API_KEY
3. 获取地址：https://dashscope.console.aliyun.com/apiKey
"""

import os
from pathlib import Path

# 尝试加载 dotenv
try:
    from dotenv import load_dotenv
    env_path = Path(__file__).parent.parent / 'config' / '.env'
    load_dotenv(env_path)
except ImportError:
    pass

# 获取 API Key
DASHSCOPE_API_KEY = os.getenv('DASHSCOPE_API_KEY', '')
IMAGE_MODEL = os.getenv('IMAGE_MODEL', 'qwen-vl-plus')
TEXT_MODEL = os.getenv('TEXT_MODEL', 'qwen3.5-plus')


def check_api_key():
    """检查 API Key 是否配置"""
    if not DASHSCOPE_API_KEY or DASHSCOPE_API_KEY == 'sk-your-api-key-here':
        raise ValueError(
            '未配置 API Key！\n'
            '请按以下步骤配置：\n'
            '1. 复制 config/.env.example 为 config/.env\n'
            '2. 填入你的 DASHSCOPE_API_KEY\n'
            '3. 获取地址：https://dashscope.console.aliyun.com/apiKey'
        )
    return True


def call_image_api(image_path, prompt):
    """
    调用图像识别 API
    
    参数：
    image_path: 图片路径
    prompt: 识别提示词
    
    返回：
    dict - 识别结果
    """
    check_api_key()
    
    try:
        import dashscope
        from dashscope import MultiModalConversation
        
        # 调用 API
        response = MultiModalConversation.call(
            model=IMAGE_MODEL,
            messages=[{
                'role': 'user',
                'content': [
                    {'image': f'file://{image_path}'},
                    {'text': prompt}
                ]
            }],
            api_key=DASHSCOPE_API_KEY
        )
        
        if response.status_code == 200:
            return response.output.choices[0].message.content[0]['text']
        else:
            raise Exception(f'API 调用失败：{response.code} - {response.message}')
    
    except ImportError:
        raise ImportError('请安装 dashscope: pip install dashscope')


def call_llm_api(prompt, model=None):
    """
    调用文本生成 API
    
    参数：
    prompt: 提示词
    model: 模型名称（默认使用 TEXT_MODEL）
    
    返回：
    str - 生成结果
    """
    check_api_key()
    
    if model is None:
        model = TEXT_MODEL
    
    try:
        import dashscope
        from dashscope import Generation
        
        # 调用 API
        response = Generation.call(
            model=model,
            prompt=prompt,
            api_key=DASHSCOPE_API_KEY
        )
        
        if response.status_code == 200:
            return response.output.text
        else:
            raise Exception(f'API 调用失败：{response.code} - {response.message}')
    
    except ImportError:
        raise ImportError('请安装 dashscope: pip install dashscope')


# 测试
if __name__ == '__main__':
    print('API 客户端测试：\n')
    
    try:
        check_api_key()
        print('✅ API Key 已配置')
        
        # 测试文本生成
        print('\n测试文本生成...')
        response = call_llm_api('你好，请简单介绍一下自己')
        print(f'响应：{response[:100]}...')
        
    except ValueError as e:
        print(f'❌ {e}')
    except Exception as e:
        print(f'❌ 测试失败：{e}')
