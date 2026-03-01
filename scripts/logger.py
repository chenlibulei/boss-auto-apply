#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
日志系统配置
"""

import logging
import sys
from pathlib import Path
from datetime import datetime


def setup_logger(log_dir=None, level=logging.INFO):
    """
    设置日志系统
    
    参数：
    log_dir: 日志文件目录，默认在当前目录
    level: 日志级别
    
    返回：
    logger: 日志对象
    """
    if log_dir is None:
        log_dir = Path(__file__).parent.parent / 'logs'
    else:
        log_dir = Path(log_dir)
    
    # 创建日志目录
    log_dir.mkdir(parents=True, exist_ok=True)
    
    # 日志文件名（按日期）
    date_str = datetime.now().strftime('%Y-%m-%d')
    log_file = log_dir / f'boss-auto-apply-{date_str}.log'
    
    # 创建 logger
    logger = logging.getLogger('boss_auto_apply')
    logger.setLevel(level)
    
    # 避免重复添加 handler
    if logger.handlers:
        return logger
    
    # 创建 formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # 文件 handler
    file_handler = logging.FileHandler(log_file, encoding='utf-8')
    file_handler.setLevel(level)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    
    # 控制台 handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(level)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    return logger


# 创建全局 logger 实例
logger = setup_logger()


def get_logger():
    """获取 logger 实例"""
    return logger


# 快捷函数
def debug(msg):
    logger.debug(msg)


def info(msg):
    logger.info(msg)


def warning(msg):
    logger.warning(msg)


def error(msg):
    logger.error(msg)


def critical(msg):
    logger.critical(msg)


# 测试
if __name__ == '__main__':
    print('日志系统测试：\n')
    debug('这是一条调试信息')
    info('这是一条普通信息')
    warning('这是一条警告信息')
    error('这是一条错误信息')
    critical('这是一条严重错误信息')
    print(f'\n日志文件已保存到：logs/boss-auto-apply-{datetime.now().strftime("%Y-%m-%d")}.log')
