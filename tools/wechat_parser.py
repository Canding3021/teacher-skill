#!/usr/bin/env python3
"""
微信聊天记录解析器 - 教师版

专门用于解析教师相关的微信聊天记录：
1. 家长群消息（班级群、学科群等）
2. 同事群消息（教研组、备课组等）
3. 与学生/家长的私聊记录
4. 教学相关的文件分享

支持格式：
- WeChatMsg 导出（txt/html/csv）
- 留痕导出（json）
- 手动复制粘贴（纯文本）
- 微信备份文件（需要额外工具）

用法：
  python3 wechat_parser.py --file 聊天记录.txt --teacher "张老师" --subject "数学"
  python3 wechat_parser.py --file 家长群.json --teacher "李老师" --output ./materials/li_teacher
"""

import argparse
import json
import re
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional, List, Dict, Any
import logging

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class WeChatParser:
    """微信聊天记录解析器 - 教师专用版"""
    
    def __init__(self, teacher_name: str, subject: Optional[str] = None):
        self.teacher_name = teacher_name
        self.subject = subject
        self.teacher_messages = []
        self.parent_messages = []
        self.student_messages = []
        self.teaching_content = []
        
    def detect_format(self, file_path: str) -> str:
        """自动检测文件格式"""
        ext = Path(file_path).suffix.lower()
        
        if ext == '.json':
            return 'liuhen'  # 留痕导出
        elif ext == '.csv':
            return 'wechatmsg_csv'
        elif ext == '.html' or ext == '.htm':
            return 'wechatmsg_html'
        elif ext == '.txt':
            # 尝试区分 WeChatMsg txt 和纯文本
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                first_lines = f.read(2000)
            # WeChatMsg 格式通常有时间戳模式
            if re.search(r'\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}:\d{2}', first_lines):
                return 'wechatmsg_txt'
            return 'plaintext'
        else:
            return 'plaintext'
    
    def parse_wechatmsg_txt(self, file_path: str) -> List[Dict[str, Any]]:
        """解析 WeChatMsg 导出的 txt 格式
        
        典型格式：
        2024-01-15 20:30:45 张老师
        今天作业是练习册第25页
        
        2024-01-15 20:31:02 学生家长
        收到，谢谢老师
        """
        messages = []
        current_msg = None
        
        # WeChatMsg 时间戳 + 发送者模式
        msg_pattern = re.compile(r'^(\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}:\d{2})\s+(.+)$')
        
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            for line in f:
                line = line.rstrip('\n')
                match = msg_pattern.match(line)
                if match:
                    if current_msg:
                        messages.append(current_msg)
                    timestamp, sender = match.groups()
                    current_msg = {
                        'timestamp': timestamp,
                        'sender': sender.strip(),
                        'content': '',
                        'source': 'wechatmsg_txt'
                    }
                elif current_msg and line.strip():
                    if current_msg['content']:
                        current_msg['content'] += '\n'
                    current_msg['content'] += line
        
        if current_msg:
            messages.append(current_msg)
        
        logger.info(f"从 WeChatMsg txt 格式解析出 {len(messages)} 条消息")
        return messages
    
    def parse_plaintext(self, file_path: str) -> List[Dict[str, Any]]:
        """解析纯文本格式"""
        messages = []
        
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            lines = f.readlines()
        
        # 简单的行解析
        for i, line in enumerate(lines):
            line = line.strip()
            if line:
                # 尝试提取发送者（简单模式：以"："或":"分隔）
                if '：' in line:
                    parts = line.split('：', 1)
                    sender = parts[0].strip()
                    content = parts[1].strip() if len(parts) > 1 else ""
                elif ':' in line and not line.startswith('http'):
                    parts = line.split(':', 1)
                    sender = parts[0].strip()
                    content = parts[1].strip() if len(parts) > 1 else ""
                else:
                    sender = "未知"
                    content = line
                
                messages.append({
                    'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    'sender': sender,
                    'content': content,
                    'source': 'plaintext',
                    'line_number': i + 1
                })
        
        logger.info(f"从纯文本格式解析出 {len(messages)} 条消息")
        return messages
    
    def parse_json(self, file_path: str) -> List[Dict[str, Any]]:
        """解析 JSON 格式（留痕导出）"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            messages = []
            
            # 留痕导出格式
            if isinstance(data, list):
                for item in data:
                    msg = {
                        'timestamp': item.get('time', ''),
                        'sender': item.get('sender', ''),
                        'content': item.get('content', ''),
                        'source': 'liuhen_json'
                    }
                    messages.append(msg)
            elif isinstance(data, dict) and 'messages' in data:
                for item in data['messages']:
                    msg = {
                        'timestamp': item.get('time', ''),
                        'sender': item.get('sender', ''),
                        'content': item.get('content', ''),
                        'source': 'liuhen_json'
                    }
                    messages.append(msg)
            
            logger.info(f"从 JSON 格式解析出 {len(messages)} 条消息")
            return messages
            
        except Exception as e:
            logger.error(f"解析 JSON 文件失败: {e}")
            return []
    
    def categorize_messages(self, messages: List[Dict[str, Any]]) -> Dict[str, Any]:
        """分类消息"""
        teacher_keywords = ["老师", "教师", "班主任", "教授"]
        parent_keywords = ["家长", "爸爸", "妈妈", "父亲", "母亲"]
        student_keywords = ["同学", "学生", "孩子", "小朋友"]
        teaching_keywords = ["作业", "考试", "成绩", "教案", "课件", "练习", "上课", "教学"]
        
        if self.subject:
            teaching_keywords.append(self.subject)
        
        for msg in messages:
            sender = msg.get('sender', '').lower()
            content = msg.get('content', '').lower()
            
            # 检查是否是教师消息
            is_teacher = False
            for keyword in teacher_keywords:
                if keyword in sender or (self.teacher_name and self.teacher_name in sender):
                    is_teacher = True
                    break
            
            if is_teacher:
                self.teacher_messages.append(msg)
                
                # 检查是否包含教学相关内容
                is_teaching = False
                for keyword in teaching_keywords:
                    if keyword in content:
                        is_teaching = True
                        break
                
                if is_teaching:
                    self.teaching_content.append(msg)
            
            # 检查是否是家长消息
            is_parent = False
            for keyword in parent_keywords:
                if keyword in sender:
                    is_parent = True
                    break
            
            if is_parent:
                self.parent_messages.append(msg)
            
            # 检查是否是学生消息
            is_student = False
            for keyword in student_keywords:
                if keyword in sender:
                    is_student = True
                    break
            
            if is_student:
                self.student_messages.append(msg)
        
        return {
            'teacher_messages': len(self.teacher_messages),
            'parent_messages': len(self.parent_messages),
            'student_messages': len(self.student_messages),
            'teaching_content': len(self.teaching_content)
        }
    
    def analyze_teaching_patterns(self) -> Dict[str, Any]:
        """分析教学模式"""
        patterns = {
            'homework_patterns': [],
            'exam_patterns': [],
            'feedback_patterns': [],
            'communication_style': []
        }
        
        # 分析作业布置模式
        homework_keywords = ["作业", "练习", "任务", "完成", "提交"]
        for msg in self.teacher_messages:
            content = msg.get('content', '').lower()
            if any(keyword in content for keyword in homework_keywords):
                patterns['homework_patterns'].append({
                    'content': msg['content'][:100] + "..." if len(msg['content']) > 100 else msg['content'],
                    'time': msg.get('timestamp', '')
                })
        
        # 分析考试相关模式
        exam_keywords = ["考试", "测验", "成绩", "分数", "排名"]
        for msg in self.teacher_messages:
            content = msg.get('content', '').lower()
            if any(keyword in content for keyword in exam_keywords):
                patterns['exam_patterns'].append({
                    'content': msg['content'][:100] + "..." if len(msg['content']) > 100 else msg['content'],
                    'time': msg.get('timestamp', '')
                })
        
        # 分析沟通风格
        style_indicators = {
            'formal': ["请", "谢谢", "您好", "麻烦", "辛苦"],
            'encouraging': ["加油", "很棒", "优秀", "进步", "表扬"],
            'strict': ["必须", "一定", "严格", "要求", "检查"],
            'caring': ["注意", "小心", "保重", "关心", "照顾"]
        }
        
        for style, keywords in style_indicators.items():
            count = 0
            for msg in self.teacher_messages:
                content = msg.get('content', '').lower()
                if any(keyword in content for keyword in keywords):
                    count += 1
            if count > 0:
                patterns['communication_style'].append({
                    'style': style,
                    'count': count,
                    'percentage': round(count / max(len(self.teacher_messages), 1) * 100, 1)
                })
        
        return patterns
    
    def parse_file(self, file_path: str) -> Dict[str, Any]:
        """解析文件主函数"""
        if not Path(file_path).exists():
            return {"status": "error", "message": f"文件不存在: {file_path}"}
        
        # 检测并解析格式
        file_format = self.detect_format(file_path)
        logger.info(f"检测到文件格式: {file_format}")
        
        if file_format == 'wechatmsg_txt':
            messages = self.parse_wechatmsg_txt(file_path)
        elif file_format == 'liuhen':
            messages = self.parse_json(file_path)
        else:
            messages = self.parse_plaintext(file_path)
        
        if not messages:
            return {"status": "error", "message": "未能解析出任何消息"}
        
        # 分类消息
        categories = self.categorize_messages(messages)
        
        # 分析教学模式
        patterns = self.analyze_teaching_patterns()
        
        # 生成报告
        report = {
            "status": "success",
            "teacher": self.teacher_name,
            "subject": self.subject,
            "file_format": file_format,
            "total_messages": len(messages),
            "categories": categories,
            "patterns": patterns,
            "sample_messages": {
                "teacher": self.teacher_messages[:5] if self.teacher_messages else [],
                "teaching": self.teaching_content[:3] if self.teaching_content else []
            }
        }
        
        return report
    
    def save_results(self, report: Dict[str, Any], output_dir: Optional[str] = None) -> str:
        """保存解析结果"""
        if output_dir:
            output_path = Path(output_dir)
        else:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_path = Path(f"./wechat_analysis/{self.teacher_name}_{timestamp}")
        
        output_path.mkdir(parents=True, exist_ok=True)
        
        # 保存报告
        report_path = output_path / "analysis_report.json"
        report_path.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
        
        # 保存教师消息
        if self.teacher_messages:
            teacher_msg_path = output_path / "teacher_messages.json"
            teacher_msg_path.write_text(json.dumps(self.teacher_messages, indent=2, ensure_ascii=False), encoding="utf-8")
        
        # 保存教学相关内容
        if self.teaching_content:
            teaching_path = output_path / "teaching_content.json"
            teaching_path.write_text(json.dumps(self.teaching_content, indent=2, ensure_ascii=False), encoding="utf-8")
        
        # 保存原始分类数据
        categories_data = {
            "teacher_messages": self.teacher_messages,
            "parent_messages": self.parent_messages,
            "student_messages": self.student_messages,
            "teaching_content": self.teaching_content
        }
        
        categories_path = output_path / "categorized_messages.json"
        categories_path.write_text(json.dumps(categories_data, indent=2, ensure_ascii=False), encoding="utf-8")
        
        logger.info(f"解析结果已保存到: {output_path}")
        return str(output_path.absolute())


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description="微信聊天记录解析器 - 教师版")
    parser.add_argument("--file", type=str, required=True, help="聊天记录文件路径")
    parser.add_argument("--teacher", type=str, required=True, help="教师姓名")
    parser.add_argument("--subject", type=str, help="教师学科")
    parser.add_argument("--output", type=str, help="输出目录")
    
    args = parser.parse_args()
    
    # 创建解析器
    parser_obj = WeChatParser(args.teacher, args.subject)
    
    # 解析文件
    print(f"开始解析微信聊天记录: {args.file}")
    report = parser_obj.parse_file(args.file)
    
    if report["status"] == "error":
        print(f"错误: {report['message']}")
        sys.exit(1)
    
    # 保存结果
    output_dir = parser_obj.save_results(report, args.output)
    
    # 打印摘要
    print("\n" + "="*60)
    print("微信聊天记录解析完成!")
    print("="*60)
    print(f"教师: {report['teacher']}")
    print(f"学科: {report['subject'] or '未指定'}")
    print(f"文件格式: {report['file_format']}")
    print(f"总消息数: {report['total_messages']}")
    print(f"教师消息: {report['categories']['teacher_messages']}")
    print(f"家长消息: {report['categories']['parent_messages']}")
    print(f"学生消息: {report['categories']['student_messages']}")
    print(f"教学相关内容: {report['categories']['teaching_content']}")
    print(f"输出目录: {output_dir}")
    print("="*60)
    
    # 打印沟通风格分析
    if report['patterns']['communication_style']:
        print("\n沟通风格分析:")
        for style in report['patterns']['communication_style']:
            print(f"  {style['style']}: {style['count']}次 ({style['percentage']}%)")


if __name__ == "__main__":
    main()