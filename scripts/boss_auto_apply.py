#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
BOSS 直聘自动投递脚本 - v1.0.4

更新内容：
- ✅ 集成薪资解析
- ✅ 添加日志系统
- ✅ 大模型生成招呼语
- ⏳ 错误处理（待开发）
"""

import pyautogui
import pyperclip
import time
import json
import os
from datetime import datetime
from pathlib import Path

# 导入日志系统
from scripts.logger import logger, info, warning, error, debug

# 禁用故障保护
pyautogui.FAILSAFE = False

# 工作区根目录
WORKSPACE_ROOT = Path('C:/Users/chen/.openclaw/workspace')

# 加载配置
CONFIG_PATH = Path(__file__).parent.parent / 'config' / 'coordinates.json'
with open(CONFIG_PATH, 'r', encoding='utf-8') as f:
    config = json.load(f)

COORDS = config['coordinates']
SCROLL = config['scroll']['distance']
TIMING = config['timing']

# 加载筛选规则
FILTER_PATH = Path(__file__).parent.parent / 'config' / 'filter-rules.json'
with open(FILTER_PATH, 'r', encoding='utf-8') as f:
    filter_rules = json.load(f)

# 导入薪资解析
from scripts.salary_parser import parse_salary, check_salary_match, format_salary

# 导入招呼语生成
from scripts.greeting_generator import generate_greeting


class BossAutoApply:
    def __init__(self, mode='test', count=5):
        self.mode = mode
        self.count = count
        self.results = []
        self.applied_count = 0
        
    def click_job_card(self):
        pyautogui.click(COORDS['jobCard']['x'], COORDS['jobCard']['y'])
        time.sleep(TIMING['pageLoadWait'] / 1000)
        
    def screenshot_job(self, index):
        """截图保存岗位信息"""
        screenshot = pyautogui.screenshot()
        path = WORKSPACE_ROOT / f'boss-apply-{index}.png'
        screenshot.save(str(path))
        info(f'截图已保存：{path.name}')
        return path
    
    def delete_screenshot(self, screenshot_path):
        """删除截图文件"""
        try:
            if screenshot_path.exists():
                screenshot_path.unlink()
                info(f'截图已删除：{screenshot_path.name}')
            else:
                warning(f'截图文件不存在：{screenshot_path}')
        except Exception as e:
            error(f'删除截图失败：{e}')
        
    def identify_job_with_browser(self):
        """使用 browser 工具识别岗位信息（通过 OpenClaw）"""
        info('正在调用 browser snapshot 识别岗位信息...')
        
        # 调用 browser snapshot
        try:
            from browser import snapshot
            result = snapshot(refs='aria')
            # 解析返回的页面信息
            job_info = self.parse_browser_snapshot(result)
            return job_info
        except Exception as e:
            warning(f'browser snapshot 失败：{e}')
            return None
    
    def identify_job_with_api(self, screenshot_path):
        """使用大模型 API 识别岗位信息"""
        info('正在调用大模型 API 识别岗位信息...')
        
        try:
            from scripts.api_client import call_image_api
            
            # 识别提示词
            prompt = """请详细识别这个 BOSS 直聘岗位详情页的所有信息，并以 JSON 格式返回：

需要识别的信息：
1. 公司名称（company）
2. 岗位名称（position）
3. 薪资范围（salary，如 "15-25K·13 薪"）
4. 学历要求（education，如 "本科"）
5. 城市（city，如 "杭州"）
6. 经验要求（experience，如 "3-5 年"）
7. 岗位职责（responsibilities，数组格式）
8. 任职要求（requirements，数组格式）

请只返回 JSON 数据，不要其他说明。格式如下：
{
  "company": "公司名称",
  "position": "岗位名称",
  "salary": "薪资范围",
  "education": "学历要求",
  "city": "城市",
  "experience": "经验要求",
  "responsibilities": ["职责 1", "职责 2"],
  "requirements": ["要求 1", "要求 2"]
}"""
            
            # 调用 API
            result_text = call_image_api(str(screenshot_path), prompt)
            
            # 解析 JSON 结果
            import json
            # 尝试提取 JSON 部分（去除可能的 markdown 标记）
            json_start = result_text.find('{')
            json_end = result_text.rfind('}') + 1
            if json_start >= 0 and json_end > json_start:
                json_str = result_text[json_start:json_end]
                job_info = json.loads(json_str)
                info(f'API 识别成功：{job_info.get("company")} - {job_info.get("position")}')
                return job_info
            else:
                warning('API 返回格式不正确')
                return None
                
        except Exception as e:
            error(f'大模型 API 识别失败：{e}')
            return None
    
    def parse_browser_snapshot(self, snapshot_data):
        """解析 browser snapshot 数据"""
        # 从 snapshot 中提取岗位信息
        # 这是一个简化版本，实际需要更复杂的解析
        job_info = {
            'company': '待识别',
            'position': '待识别',
            'salary': '待识别',
            'salary_min': 0,
            'salary_max': 0,
            'education': '待识别',
            'city': '待识别',
            'experience': '待识别',
            'responsibilities': '',
            'requirements': ''
        }
        
        # TODO: 解析 snapshot 数据
        return job_info
        
    def check_job_match(self, job_info):
        """判断岗位是否符合条件"""
        # 解析薪资
        salary_info = parse_salary(job_info.get('salary', ''))
        job_info['salary_parsed'] = salary_info  # 保存解析结果
        
        # 检查薪资
        is_match, reason = check_salary_match(salary_info, filter_rules['salary']['minUpperLimit'])
        if not is_match:
            return False, reason
        
        # 检查城市
        city = job_info.get('city', '')
        preferred_cities = filter_rules['cities']['preferred']
        if city and city not in preferred_cities and '杭州' not in city:
            return False, f'城市{city}不在优先列表'
        
        # 检查公司黑名单
        company = job_info.get('company', '')
        for big_tech in filter_rules['blacklist']['bigTech']:
            if big_tech in company:
                return False, f'大厂{big_tech}'
        
        for outsourcing in filter_rules['blacklist']['outsourcing']:
            if outsourcing in company:
                return False, f'外包{outsourcing}'
        
        # 检查学历
        education = job_info.get('education', '')
        if '硕士' in education and '以上' in education:
            return False, '学历要求硕士以上'
        
        return True, ''
        
    def generate_greeting(self, job_info):
        """生成个性化招呼语（使用大模型）"""
        try:
            info(f'正在调用大模型生成招呼语...')
            greeting = generate_greeting(job_info, use_llm=True)
            info('招呼语生成成功')
            return greeting
        except Exception as e:
            warning(f'大模型生成失败，使用模板：{e}')
            # 回退到模板生成
            from scripts.greeting_generator import generate_greeting_template
            return generate_greeting_template(job_info)
        
    def next_job(self):
        pyautogui.moveTo(COORDS['jobCard']['x'], COORDS['jobCard']['y'])
        time.sleep(0.5)
        pyautogui.scroll(-SCROLL)
        time.sleep(TIMING['afterScrollWait'] / 1000)
        
    def apply_job(self, greeting):
        pyperclip.copy(greeting)
        print('  招呼语已复制到剪贴板')
        
        print('  点击立即沟通...')
        pyautogui.click(COORDS['immediateChat']['x'], COORDS['immediateChat']['y'])
        time.sleep(TIMING['afterClickWait'] / 1000)
        
        print('  点击继续沟通...')
        pyautogui.click(COORDS['continueChat']['x'], COORDS['continueChat']['y'])
        time.sleep(TIMING['afterContinueWait'] / 1000)
        
        print('  点击聊天输入框...')
        pyautogui.click(COORDS['chatInput']['x'], COORDS['chatInput']['y'])
        time.sleep(TIMING['beforePasteWait'] / 1000)
        
        print('  粘贴招呼语...')
        pyautogui.hotkey('ctrl', 'v')
        time.sleep(TIMING['afterPasteWait'] / 1000)
        
        print('  发送消息...')
        pyautogui.press('enter')
        time.sleep(TIMING['afterSendWait'] / 1000)
        
        print('  点击返回按钮...')
        pyautogui.click(COORDS['returnButton']['x'], COORDS['returnButton']['y'])
        time.sleep(TIMING['afterReturnWait'] / 1000)
        
        # 新增：先移动到卡片位置，再滚动，再点击
        print('  移动到职位卡片位置...')
        pyautogui.moveTo(COORDS['jobCard']['x'], COORDS['jobCard']['y'])
        time.sleep(0.5)
        
        print('  滚动到下一个岗位...')
        pyautogui.scroll(-SCROLL)
        time.sleep(TIMING['afterScrollWait'] / 1000)
        
        print('  点击下一个职位卡片...')
        pyautogui.click(COORDS['jobCard']['x'], COORDS['jobCard']['y'])
        time.sleep(TIMING['pageLoadWait'] / 1000)
        
    def save_result(self, job_info, status, greeting=None):
        result = {
            'date': datetime.now().strftime('%Y-%m-%d'),
            'company': job_info.get('company', ''),
            'position': job_info.get('position', ''),
            'salary': job_info.get('salary', ''),
            'education': job_info.get('education', ''),
            'status': status,
            'greeting': greeting or ''
        }
        self.results.append(result)
        
    def save_to_csv(self):
        date_str = datetime.now().strftime('%Y-%m-%d')
        path = WORKSPACE_ROOT / f'boss-apply-{date_str}.csv'
        
        with open(path, 'w', encoding='utf-8-sig') as f:
            f.write('日期，公司，岗位，薪资，学历，状态，招呼语\n')
            for r in self.results:
                greeting_clean = r['greeting'].replace('\n', ' ').replace(',', ',')
                f.write(f"{r['date']},{r['company']},{r['position']},{r['salary']},{r['education']},{r['status']},{greeting_clean}\n")
                
    def run(self):
        info(f'\n{"="*50}')
        info(f'BOSS 直聘自动投递 - 开始执行')
        info(f'模式：{self.mode}, 数量：{self.count}')
        info(f'{"="*50}\n')
        
        for i in range(1, self.count + 1):
            info(f'\n[岗位{i}/{self.count}] 开始处理...')
            info('-' * 40)
            
            # 步骤 1：点击职位卡片
            info('步骤 1：点击职位卡片...')
            self.click_job_card()
            
            # 截图
            screenshot_path = self.screenshot_job(i)
            info(f'截图已保存：{screenshot_path.name}')
            
            # 步骤 2：识别岗位信息
            info('步骤 2：识别岗位信息...')
            time.sleep(TIMING['apiLimitWait'] / 1000)
            
            # 使用大模型识别岗位信息
            job_info = self.identify_job_with_api(screenshot_path)
            
            if job_info:
                info(f'识别结果：{job_info["company"]} - {job_info["position"]} - {job_info["salary"]}')
            else:
                # 如果 API 识别失败，使用模拟数据
                warning('API 识别失败，使用模拟数据')
                job_info = {
                    'company': f'测试公司{i}',
                    'position': '前端开发工程师',
                    'salary': '15-25K',
                    'salary_min': 15000,
                    'salary_max': 25000,
                    'education': '本科',
                    'city': '杭州',
                    'experience': '3-5 年',
                    'responsibilities': '负责前端开发',
                    'requirements': '熟练掌握 React/Vue'
                }
            
            # 判断是否符合条件
            print(f'步骤 2：判断是否符合条件...')
            is_match, reason = self.check_job_match(job_info)
            
            if is_match:
                print(f'[OK] 符合条件')
                
                # 步骤 3：生成招呼语
                print(f'步骤 3：生成招呼语...')
                greeting = self.generate_greeting(job_info)
                
                # 删除截图（识别完成后）
                self.delete_screenshot(screenshot_path)
                
                if self.mode == 'test':
                    print(f'\n【招呼语预览】')
                    print(f'{greeting[:150]}...')
                    print()
                    self.save_result(job_info, '测试 - 符合', greeting)
                    # 测试模式也需要滚动到下一个
                    if i < self.count:
                        print(f'步骤 5：滚动到下一个岗位...')
                        self.next_job()
                else:
                    print(f'步骤 4：执行投递...')
                    self.apply_job(greeting)  # 已包含滚动和点击下一个
                    print(f'[OK] 投递完成！')
                    self.save_result(job_info, '已投递', greeting)
                    self.applied_count += 1
                    # 正式模式 apply_job 已处理滚动和点击，不需要再调用 next_job()
            else:
                print(f'[SKIP] 不符合条件：{reason}')
                # 删除截图（识别完成后）
                self.delete_screenshot(screenshot_path)
                self.save_result(job_info, f'不符合-{reason}')
                # 不符合也需要滚动到下一个
                if i < self.count:
                    print(f'步骤 5：滚动到下一个岗位...')
                    self.next_job()
                
            if i % 5 == 0 and i < self.count:
                print(f'\n已处理 5 个岗位，休息 15 秒...')
                time.sleep(15)
        
        self.save_to_csv()
        
        print(f'\n{"="*50}')
        print(f'执行完成！')
        print(f'共投递 {self.applied_count} 个岗位')
        print(f'结果已保存到：boss-apply-{datetime.now().strftime("%Y-%m-%d")}.csv')
        print(f'{"="*50}\n')
        
        # 投递完成后，检查是否有 HR 回复
        print('\n检查 HR 消息回复...')
        self.check_and_reply()
        
    def check_and_reply(self):
        """检查消息并回复"""
        from scripts.check_message import check_and_reply as check_reply
        try:
            check_reply()
        except Exception as e:
            print(f'检查消息失败：{e}')


if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(description='BOSS 直聘自动投递')
    parser.add_argument('--mode', choices=['test', 'apply'], default='test', help='运行模式')
    parser.add_argument('--count', type=int, default=5, help='处理岗位数量')
    
    args = parser.parse_args()
    
    agent = BossAutoApply(mode=args.mode, count=args.count)
    agent.run()
