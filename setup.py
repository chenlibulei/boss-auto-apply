#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
BOSS 直聘自动投递 - 安装配置脚本

安装时会主动询问用户配置：
1. 选择图像识别大模型提供商
2. 配置 API Key
3. 配置个人信息
"""

import os
import json
from pathlib import Path
from datetime import datetime

# 颜色输出
class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def print_header(text):
    print(f"\n{Colors.HEADER}{Colors.BOLD}{'='*60}{Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}{text.center(60)}{Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}{'='*60}{Colors.ENDC}\n")

def print_success(text):
    print(f"{Colors.OKGREEN}✅ {text}{Colors.ENDC}")

def print_warning(text):
    print(f"{Colors.WARNING}⚠️  {text}{Colors.ENDC}")

def print_error(text):
    print(f"{Colors.FAIL}❌ {text}{Colors.ENDC}")

def print_info(text):
    print(f"{Colors.OKCYAN}ℹ️  {text}{Colors.ENDC}")


def choose_image_model_provider():
    """选择图像识别模型提供商"""
    print_header("选择图像识别模型提供商")
    
    providers = [
        ("1", "dashscope", "阿里云百炼 (qwen-vl-plus)", "推荐，国内访问快"),
        ("2", "openai", "OpenAI (gpt-4o)", "需要国际网络"),
        ("3", "anthropic", "Anthropic (Claude 3.5)", "需要国际网络"),
        ("4", "local", "本地模型 (Ollama)", "免费，需要本地部署"),
        ("5", "skip", "跳过配置", "稍后手动配置 .env 文件")
    ]
    
    print("请选择图像识别模型提供商：\n")
    for num, key, name, desc in providers:
        print(f"  {Colors.OKBLUE}{num}{Colors.ENDC}. {name:30} - {desc}")
    
    while True:
        choice = input(f"\n{Colors.BOLD}请输入选项 (1-5): {Colors.ENDC}").strip()
        
        if choice == "1":
            print_success("已选择：阿里云百炼 (DashScope)")
            return "dashscope"
        elif choice == "2":
            print_success("已选择：OpenAI")
            return "openai"
        elif choice == "3":
            print_success("已选择：Anthropic (Claude)")
            return "anthropic"
        elif choice == "4":
            print_success("已选择：本地模型 (Ollama)")
            return "local"
        elif choice == "5":
            print_warning("已跳过配置")
            return None
        else:
            print_error("无效选项，请重新输入")


def choose_text_model_provider():
    """选择文本生成模型提供商"""
    print_header("选择文本生成模型提供商")
    
    print_info("文本生成用于生成个性化招呼语")
    print_info("建议和图像识别使用同一家提供商，方便管理\n")
    
    providers = [
        ("1", "dashscope", "阿里云百炼 (qwen3.5-plus)", "推荐"),
        ("2", "openai", "OpenAI (gpt-4o-mini)", ""),
        ("3", "anthropic", "Anthropic (Claude 3.5)", ""),
        ("4", "local", "本地模型", ""),
        ("5", "skip", "跳过配置", "使用模板生成招呼语")
    ]
    
    print("请选择文本生成模型提供商：\n")
    for num, key, name, desc in providers:
        print(f"  {Colors.OKBLUE}{num}{Colors.ENDC}. {name:35} - {desc}")
    
    while True:
        choice = input(f"\n{Colors.BOLD}请输入选项 (1-5): {Colors.ENDC}").strip()
        
        if choice == "1":
            print_success("已选择：阿里云百炼 (DashScope)")
            return "dashscope"
        elif choice == "2":
            print_success("已选择：OpenAI")
            return "openai"
        elif choice == "3":
            print_success("已选择：Anthropic (Claude)")
            return "anthropic"
        elif choice == "4":
            print_success("已选择：本地模型")
            return "local"
        elif choice == "5":
            print_warning("已跳过配置，将使用模板生成招呼语")
            return None
        else:
            print_error("无效选项，请重新输入")


def input_api_key(provider_name, api_key_url):
    """输入 API Key"""
    print(f"\n{Colors.BOLD}请输入 {provider_name} API Key:{Colors.ENDC}")
    print(f"获取地址：{api_key_url}")
    print(f"{Colors.WARNING}注意：API Key 只会保存在本地配置文件中{Colors.ENDC}\n")
    
    api_key = input("API Key: ").strip()
    
    if api_key and api_key != "sk-your-api-key-here":
        print_success("API Key 已保存")
        return api_key
    else:
        print_warning("未配置 API Key")
        return None


def configure_personal_info():
    """配置个人信息"""
    print_header("配置个人信息")
    
    print_info("这些信息用于生成个性化招呼语\n")
    
    config = {
        "user": {
            "name": "",
            "title": "",
            "years_of_experience": 0,
            "dev_years": 0
        },
        "job_preferences": {
            "salary": {
                "min_upper_limit": 14000
            },
            "cities": {
                "preferred": []
            }
        },
        "skills": {
            "proficient": [],
            "familiar": []
        },
        "greeting_style": {
            "assistant_name": "小助手"
        }
    }
    
    # 用户称呼
    name = input(f"{Colors.BOLD}你的称呼 (如 黎哥): {Colors.ENDC}").strip()
    if name:
        config["user"]["name"] = name
    
    # 当前职位
    title = input(f"{Colors.BOLD}当前职位 (如 前端开发组长): {Colors.ENDC}").strip()
    if title:
        config["user"]["title"] = title
    
    # 工作年限
    years = input(f"{Colors.BOLD}工作年限 (如 11): {Colors.ENDC}").strip()
    if years.isdigit():
        config["user"]["years_of_experience"] = int(years)
    
    # 开发年限
    dev_years = input(f"{Colors.BOLD}开发年限 (如 6): {Colors.ENDC}").strip()
    if dev_years.isdigit():
        config["user"]["dev_years"] = int(dev_years)
    
    # 期望城市
    cities_input = input(f"{Colors.BOLD}期望城市 (多个用逗号分隔，如 杭州，上海): {Colors.ENDC}").strip()
    if cities_input:
        config["job_preferences"]["cities"]["preferred"] = [c.strip() for c in cities_input.split(",")]
    
    # 核心技能
    skills_input = input(f"{Colors.BOLD}核心技能 (多个用逗号分隔，如 React,Vue,TypeScript): {Colors.ENDC}").strip()
    if skills_input:
        config["skills"]["proficient"] = [s.strip() for s in skills_input.split(",")]
    
    # AI 助手名称
    assistant_name = input(f"{Colors.BOLD}AI 助手名称 (如 小虾): {Colors.ENDC}").strip()
    if assistant_name:
        config["greeting_style"]["assistant_name"] = assistant_name
    
    return config


def save_config(image_provider, text_provider, api_keys, personal_info):
    """保存配置"""
    print_header("保存配置")
    
    config_dir = Path(__file__).parent / "config"
    config_dir.mkdir(exist_ok=True)
    
    # 保存 AI 模型配置
    env_content = f"""# AI 模型配置
# 自动生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

# 图像识别模型提供商
IMAGE_MODEL_PROVIDER={image_provider or 'dashscope'}

# 文本生成模型提供商
TEXT_MODEL_PROVIDER={text_provider or 'dashscope'}

# ============================================
# API Keys
# ============================================

# 阿里云百炼
DASHSCOPE_API_KEY={api_keys.get('dashscope', 'sk-your-api-key-here')}
DASHSCOPE_IMAGE_MODEL=qwen-vl-plus
DASHSCOPE_TEXT_MODEL=qwen3.5-plus

# OpenAI
OPENAI_API_KEY={api_keys.get('openai', 'sk-your-openai-api-key-here')}
OPENAI_IMAGE_MODEL=gpt-4o
OPENAI_TEXT_MODEL=gpt-4o-mini

# Anthropic
ANTHROPIC_API_KEY={api_keys.get('anthropic', 'your-anthropic-api-key-here')}
ANTHROPIC_IMAGE_MODEL=claude-3-5-sonnet-20241022
ANTHROPIC_TEXT_MODEL=claude-3-5-haiku-20241022

# 本地模型
LOCAL_IMAGE_MODEL=llava
LOCAL_TEXT_MODEL=qwen2.5
LOCAL_IMAGE_ENDPOINT=http://localhost:11434/api/generate
"""
    
    env_path = config_dir / ".env"
    with open(env_path, 'w', encoding='utf-8') as f:
        f.write(env_content)
    print_success(f"AI 模型配置已保存：{env_path}")
    
    # 保存用户配置
    user_config_path = config_dir / "user_config.json"
    with open(user_config_path, 'w', encoding='utf-8') as f:
        json.dump(personal_info, f, indent=2, ensure_ascii=False)
    print_success(f"用户配置已保存：{user_config_path}")
    
    # 添加到 .gitignore
    gitignore_path = Path(__file__).parent / ".gitignore"
    with open(gitignore_path, 'a', encoding='utf-8') as f:
        f.write("\n# 配置文件\nconfig/.env\nconfig/user_config.json\n")
    print_success("配置文件已添加到 .gitignore")


def main():
    """主函数"""
    print_header("BOSS 直聘自动投递 - 安装配置向导")
    print_info("本向导会帮助你配置 AI 模型和个人信息")
    print_info("按 Ctrl+C 可以随时退出\n")
    
    try:
        # 选择模型提供商
        image_provider = choose_image_model_provider()
        text_provider = choose_text_model_provider()
        
        # 配置 API Keys
        api_keys = {}
        
        if image_provider == "dashscope" or text_provider == "dashscope":
            api_key = input_api_key(
                "阿里云百炼",
                "https://dashscope.console.aliyun.com/apiKey"
            )
            if api_key:
                api_keys["dashscope"] = api_key
        
        if image_provider == "openai" or text_provider == "openai":
            api_key = input_api_key(
                "OpenAI",
                "https://platform.openai.com/api-keys"
            )
            if api_key:
                api_keys["openai"] = api_key
        
        if image_provider == "anthropic" or text_provider == "anthropic":
            api_key = input_api_key(
                "Anthropic",
                "https://console.anthropic.com/settings/keys"
            )
            if api_key:
                api_keys["anthropic"] = api_key
        
        # 配置个人信息
        personal_info = configure_personal_info()
        
        # 保存配置
        save_config(image_provider, text_provider, api_keys, personal_info)
        
        # 完成
        print_header("配置完成")
        print_success("安装配置已完成！")
        print_info("\n下一步:")
        print("  1. 校准坐标：编辑 config/coordinates.json")
        print("  2. 测试运行：python scripts/boss_auto_apply.py --mode test --count 3")
        print("  3. 正式投递：python scripts/boss_auto_apply.py --mode apply --count 6")
        print()
        
    except KeyboardInterrupt:
        print("\n\n" + Colors.WARNING + "配置已取消" + Colors.ENDC)
        print_info("你可以稍后手动编辑 config/.env 和 config/user_config.json")


if __name__ == "__main__":
    main()
