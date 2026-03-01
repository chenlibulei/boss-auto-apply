#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
薪资解析工具
"""

import re


def parse_salary(salary_str):
    """
    解析薪资字符串
    
    支持格式：
    - "15-25K" → {min: 15000, max: 25000, unit: '月'}
    - "15-25K·13 薪" → {min: 15000, max: 25000, unit: '月', months: 13}
    - "13-20K·14 薪" → {min: 13000, max: 20000, unit: '月', months: 14}
    - "20-40K·13 薪" → {min: 20000, max: 40000, unit: '月', months: 13}
    - "12-18K" → {min: 12000, max: 18000, unit: '月'}
    
    返回：
    {
        'min': 15000,      # 最低月薪
        'max': 25000,      # 最高月薪
        'unit': '月',       # 薪资单位
        'months': 13,      # 年薪月数（可选）
        'original': '15-25K·13 薪'  # 原始字符串
    }
    """
    if not salary_str:
        return None
    
    result = {
        'min': 0,
        'max': 0,
        'unit': '月',
        'months': None,
        'original': salary_str
    }
    
    # 提取年薪月数（如 13 薪、14 薪、15 薪）
    months_match = re.search(r'·(\d+) 薪', salary_str)
    if months_match:
        result['months'] = int(months_match.group(1))
    
    # 提取 K 单位的薪资范围
    # 匹配 "15-25K" 或 "15-25k"
    k_pattern = r'(\d+(?:\.\d+)?)[-\s~]+(\d+(?:\.\d+)?)\s*[Kk]'
    k_match = re.search(k_pattern, salary_str)
    
    if k_match:
        min_k = float(k_match.group(1))
        max_k = float(k_match.group(2))
        result['min'] = int(min_k * 1000)
        result['max'] = int(max_k * 1000)
        result['unit'] = '月'
        return result
    
    # 匹配 "15k-25k" 格式
    k_pattern2 = r'(\d+(?:\.\d+)?)\s*[Kk][-\s~]+(\d+(?:\.\d+)?)\s*[Kk]'
    k_match2 = re.search(k_pattern2, salary_str)
    
    if k_match2:
        min_k = float(k_match2.group(1))
        max_k = float(k_match2.group(2))
        result['min'] = int(min_k * 1000)
        result['max'] = int(max_k * 1000)
        result['unit'] = '月'
        return result
    
    # 匹配 "15000-25000" 格式（直接数字）
    num_pattern = r'(\d+)[-\s~]+(\d+)'
    num_match = re.search(num_pattern, salary_str)
    
    if num_match:
        min_val = int(num_match.group(1))
        max_val = int(num_match.group(2))
        # 如果数字大于 1000，认为是月薪
        if min_val > 1000:
            result['min'] = min_val
            result['max'] = max_val
            result['unit'] = '月'
        else:
            # 否则认为是 K 单位
            result['min'] = min_val * 1000
            result['max'] = max_val * 1000
            result['unit'] = '月'
        return result
    
    # 如果以上都没匹配到，返回 None
    return None


def check_salary_match(salary_info, min_upper_limit=14000):
    """
    检查薪资是否符合要求
    
    参数：
    salary_info: parse_salary 返回的字典
    min_upper_limit: 最低薪资上限要求（默认 14k）
    
    返回：
    (bool, str) - (是否匹配，原因)
    """
    if not salary_info:
        return False, '薪资信息无法解析'
    
    if salary_info['max'] < min_upper_limit:
        return False, f'薪资上限{salary_info["max"]/1000}k < {min_upper_limit/1000}k'
    
    return True, ''


def format_salary(salary_info):
    """
    格式化薪资信息用于显示
    
    返回：
    str - 格式化的薪资字符串
    """
    if not salary_info:
        return '面议'
    
    min_k = salary_info['min'] / 1000
    max_k = salary_info['max'] / 1000
    
    # 如果是整数，去掉小数点
    if min_k == int(min_k):
        min_k = int(min_k)
    if max_k == int(max_k):
        max_k = int(max_k)
    
    result = f'{min_k}-{max_k}K'
    
    if salary_info.get('months'):
        result += f'·{salary_info["months"]}薪'
    
    return result


# 测试
if __name__ == '__main__':
    test_cases = [
        '15-25K',
        '15-25K·13 薪',
        '13-20K·14 薪',
        '20-40K·13 薪',
        '12-18K',
        '20-30K·15 薪',
        '14-18K·13 薪',
        '10-15K·15 薪',
    ]
    
    print('薪资解析测试：\n')
    for salary in test_cases:
        result = parse_salary(salary)
        print(f'输入：{salary}')
        print(f'输出：min={result["min"]}, max={result["max"]}, months={result.get("months")}')
        print(f'格式化：{format_salary(result)}')
        is_match, reason = check_salary_match(result)
        print(f'匹配检查：{"✅ 通过" if is_match else "❌ 不通过"} {reason}')
        print('-' * 50)
