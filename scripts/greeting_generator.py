#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
招呼语生成器 - 基于大模型匹配岗位和简历
"""

import json
from pathlib import Path

# 简历信息
RESUME_DATA = {
    'years': 11,
    'dev_years': 6,
    'current_role': '前端开发组长',
    'skills': {
        'proficient': ['React', 'Vue', 'TypeScript', 'Ant Design', 'ElementUI', 'ThreeJs', 'CesiumJs', 'Echarts'],
        'familiar': ['Node.js', 'Python', 'Webpack', 'Vite'],
        'experience': ['微信小程序', '支付宝小程序', '移动端 H5', '跨平台开发']
    },
    'abilities': [
        '从 0 到 1 搭建前端系统架构',
        '前端整体技术架构设计与选型',
        '制定前端编码规范与技术文档标准',
        '团队管理与建设',
        '任务分配、进度管理、代码审查'
    ],
    'projects': [
        '金赋水工业互联网平台（前端架构设计）',
        '华峰集团前端系统（从 0 到 1 搭建）',
        '城安智联前端项目（从 0 到 1 搭建）',
        '数据可视化、3D 模型展示项目',
        '监控平台、运维后台管理系统',
        '小程序开发与迭代'
    ]
}


def generate_greeting_prompt(job_info):
    """
    生成招呼语提示词
    
    参数：
    job_info: 岗位信息字典
    
    返回：
    str - 提示词
    """
    prompt = f"""你是一个专业的求职助手，需要根据岗位要求和候选人简历，生成一封个性化的求职招呼语。

## 岗位信息
- 公司：{job_info.get('company', '贵公司')}
- 岗位：{job_info.get('position', '岗位')}
- 薪资：{job_info.get('salary', '面议')}
- 城市：{job_info.get('city', '城市')}
- 经验要求：{job_info.get('experience', '经验不限')}
- 学历要求：{job_info.get('education', '学历不限')}

## 岗位职责
{job_info.get('responsibilities', '暂无详细描述')}

## 任职要求
{job_info.get('requirements', '暂无详细描述')}

## 候选人简历
- 工作年限：{RESUME_DATA['years']}年工作经验，{RESUME_DATA['dev_years']}年软件开发经验
- 当前职位：{RESUME_DATA['current_role']}
- 熟练掌握：{', '.join(RESUME_DATA['skills']['proficient'])}
- 熟悉：{', '.join(RESUME_DATA['skills']['familiar'])}
- 项目经验：{', '.join(RESUME_DATA['projects'][:3])}
- 核心能力：{', '.join(RESUME_DATA['abilities'][:3])}

## 生成要求

请分析岗位要求与候选人简历的匹配点，生成一封个性化招呼语。

**注意：**
1. 技术栈描述使用"熟练掌握"，不要使用"精通"、"专家"等夸大词汇
2. 突出与岗位要求最匹配的 3-4 个核心优势
3. 语气真诚、专业，不要过于夸张
4. 长度控制在 200-300 字
5. 如果岗位技术要求与候选人不完全匹配，强调学习能力和基础扎实

## 招呼语格式

```
您好，我是小虾，黎哥的 AI 助手。

我仔细分析了这个{岗位名称}岗位（{薪资}）的要求，并结合黎哥的经历进行了匹配：

【匹配点】
1. 经验匹配：{经验匹配描述}
2. 技术栈匹配：
   - {技术栈匹配点 1}
   - {技术栈匹配点 2}
3. {项目/能力匹配标题}：
   - {匹配描述 1}
   - {匹配描述 2}
4. 团队协作：
   - {协作能力描述}

【核心优势】
- {核心优势 1}
- {核心优势 2}
- {核心优势 3}

作为黎哥的 AI 助手，我觉得这个岗位与黎哥的经历非常匹配，尤其是{核心匹配点}方面，希望能有机会进一步沟通，谢谢！
```

请生成招呼语内容（只返回招呼语正文，不要其他说明）：
"""
    return prompt


def parse_greeting_from_response(response_text):
    """
    从 API 响应中解析招呼语
    
    参数：
    response_text: API 返回的文本
    
    返回：
    str - 招呼语正文
    """
    # 去除可能的 markdown 代码块标记
    if response_text.startswith('```'):
        lines = response_text.split('\n')
        # 跳过第一行（```）和最后一行（```）
        if lines[-1].strip() == '```':
            lines = lines[1:-1]
        else:
            lines = lines[1:]
        response_text = '\n'.join(lines)
    
    return response_text.strip()


def generate_greeting(job_info, use_llm=True):
    """
    生成招呼语
    
    参数：
    job_info: 岗位信息字典
    use_llm: 是否使用大模型生成（默认 True）
    
    返回：
    str - 招呼语
    """
    if use_llm:
        try:
            # 调用大模型生成
            from .api_client import call_llm_api
            prompt = generate_greeting_prompt(job_info)
            response = call_llm_api(prompt)
            greeting = parse_greeting_from_response(response)
            return greeting
        except Exception as e:
            # 如果 LLM 调用失败，回退到模板生成
            print(f'LLM 生成失败，使用模板：{e}')
            return generate_greeting_template(job_info)
    else:
        return generate_greeting_template(job_info)


def generate_greeting_template(job_info):
    """
    使用模板生成招呼语（回退方案）
    
    参数：
    job_info: 岗位信息字典
    
    返回：
    str - 招呼语
    """
    company = job_info.get('company', '贵公司')
    position = job_info.get('position', '岗位')
    salary = job_info.get('salary', '面议')
    
    # 根据岗位名称判断技术栈重点
    position_lower = position.lower()
    if 'react' in position_lower:
        tech_highlight = 'React'
    elif 'vue' in position_lower:
        tech_highlight = 'Vue'
    elif 'uni' in position_lower or '小程序' in position_lower:
        tech_highlight = '小程序'
    elif '3d' in position_lower or '可视化' in position_lower:
        tech_highlight = '数据可视化'
    else:
        tech_highlight = 'React/Vue'
    
    greeting = f"""您好，我是小虾，黎哥的 AI 助手。

我仔细分析了这个{position}岗位（{salary}）的要求，并结合黎哥的经历进行了匹配：

【匹配点】
1. 经验匹配：11 年工作经验，6 年软件开发经验
2. 技术栈匹配：
   - 熟练掌握 React、Vue 双框架，有实际项目经验
   - 熟练掌握 TypeScript、Ant Design 等 UI 库
   - 有微信小程序、支付宝小程序完整开发经验
3. 架构能力：
   - 从 0 到 1 搭建过多个前端系统架构
   - 有前端架构设计与性能优化经验
4. 团队协作：
   - 现任前端开发组长，统筹团队日常管理
   - 与产品、后端、UI 团队高效协同

【核心优势】
- 技术全面：熟练掌握 React/Vue 双框架及相关技术栈
- 架构经验：擅长技术选型、架构设计及性能优化
- 团队管理：具备团队建设与人才发展经验
- 学习能力：能快速定位排查项目紧急 BUG

作为黎哥的 AI 助手，我觉得这个岗位与黎哥的经历非常匹配，尤其是{tech_highlight}经验方面，希望能有机会进一步沟通，谢谢！"""
    
    return greeting


# 测试
if __name__ == '__main__':
    test_job = {
        'company': '测试公司',
        'position': '高级前端开发工程师',
        'salary': '20-30K·15 薪',
        'city': '杭州',
        'experience': '5-10 年',
        'education': '本科',
        'responsibilities': '负责前端架构设计',
        'requirements': '熟练掌握 React/Vue'
    }
    
    print('招呼语生成测试：\n')
    greeting = generate_greeting(test_job, use_llm=False)
    print(greeting)
