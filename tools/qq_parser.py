#!/usr/bin/env python3
"""
QQ聊天记录解析器 - 教师版

专门用于解析教师相关的QQ聊天记录：
1. QQ群消息（班级群、学科群、教研群等）
2. QQ私聊记录（与学生、家长、同事）
3. QQ空间动态（教学分享、教育感悟）
4. QQ文件传输（教案、课件、资料）

支持格式：
- QQ消息导出（txt/mht）
- QQ备份文件（需要解密）
- 手动复制粘贴
- 第三方工具导出

用法：
  python3 qq_parser.py --file qq_chat.txt --teacher "张老师" --group "高一数学群"
  python3 qq_parser.py --file 班级群.mht --teacher "李老师" --output ./materials/li_teacher
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
import html

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class QQParser:
    """QQ聊天记录解析器 - 教师专用版"""
    
    def __init__(self, teacher_name: str, group_name: Optional[str] = None):
        self.teacher_name = teacher_name
        self.group_name = group_name
        self.teacher_messages = []
        self.group_messages = []
        self.file_shares = []
        self.teaching_content = []
        
    def detect_format(self, file_path: str) -> str:
        """自动检测文件格式"""
        ext = Path(file_path).suffix.lower()
        
        if ext == '.mht' or ext == '.mhtml':
            return 'qq_mht'
        elif ext == '.txt':
            # 检查是否是QQ导出格式
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                first_lines = f.read(1000)
            
            # QQ导出常见模式
            if '消息记录' in first_lines or '聊天记录' in first_lines:
                return 'qq_export'
            elif re.search(r'\d{4}-\d{2}-\d{2}\s+\d{1,2}:\d{2}:\d{2}', first_lines):
                return 'timestamp_txt'
            return 'plaintext'
        else:
            return 'plaintext'
    
    def parse_qq_export(self, file_path: str) -> List[Dict[str, Any]]:
        """解析QQ导出格式（txt）"""
        messages = []
        
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        
        # QQ导出常见模式：时间 + 昵称(QQ号)
        # 2024-01-15 20:30:45 张老师(123456)
        pattern = re.compile(r'(\d{4}-\d{2}-\d{2}\s+\d{1,2}:\d{2}:\d{2})\s+([^(]+)\((\d+)\)')
        
        lines = content.split('\n')
        current_msg = None
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            match = pattern.match(line)
            if match:
                if current_msg:
                    messages.append(current_msg)
                
                timestamp, nickname, qq_number = match.groups()
                current_msg = {
                    'timestamp': timestamp,
                    'sender': nickname.strip(),
                    'qq_number': qq_number,
                    'content': '',
                    'source': 'qq_export'
                }
            elif current_msg:
                if current_msg['content']:
                    current_msg['content'] += '\n'
                current_msg['content'] += line
        
        if current_msg:
            messages.append(current_msg)
        
        logger.info(f"从QQ导出格式解析出 {len(messages)} 条消息")
        return messages
    
    def parse_qq_mht(self, file_path: str) -> List[Dict[str, Any]]:
        """解析QQ MHT格式"""
        messages = []
        
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            # MHT格式包含HTML，需要提取消息
            # 简单提取：查找消息内容
            message_pattern = re.compile(r'<div[^>]*class="message"[^>]*>.*?</div>', re.DOTALL)
            matches = message_pattern.findall(content)
            
            for match in matches:
                # 提取发送者和内容
                sender_match = re.search(r'<span[^>]*class="sender"[^>]*>(.*?)</span>', match)
                content_match = re.search(r'<div[^>]*class="content"[^>]*>(.*?)</div>', match, re.DOTALL)
                time_match = re.search(r'<span[^>]*class="time"[^>]*>(.*?)</span>', match)
                
                if sender_match and content_match:
                    sender = html.unescape(sender_match.group(1)).strip()
                    content = html.unescape(content_match.group(1)).strip()
                    timestamp = time_match.group(1).strip() if time_match else ""
                    
                    messages.append({
                        'timestamp': timestamp,
                        'sender': sender,
                        'content': content,
                        'source': 'qq_mht'
                    })
            
            logger.info(f"从QQ MHT格式解析出 {len(messages)} 条消息")
            return messages
            
        except Exception as e:
            logger.error(f"解析MHT文件失败: {e}")
            return []
    
    def parse_timestamp_txt(self, file_path: str) -> List[Dict[str, Any]]:
        """解析带时间戳的文本格式"""
        messages = []
        current_msg = None
        
        # 时间戳模式：YYYY-MM-DD HH:MM:SS
        timestamp_pattern = re.compile(r'^(\d{4}-\d{2}-\d{2}\s+\d{1,2}:\d{2}:\d{2})\s+(.+)$')
        
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            for line in f:
                line = line.rstrip('\n')
                match = timestamp_pattern.match(line)
                if match:
                    if current_msg:
                        messages.append(current_msg)
                    
                    timestamp, rest = match.groups()
                    
                    # 尝试提取发送者（可能包含在剩余部分中）
                    sender = rest
                    content = ""
                    
                    # 常见格式：发送者: 内容
                    if ':' in rest:
                        parts = rest.split(':', 1)
                        sender = parts[0].strip()
                        content = parts[1].strip() if len(parts) > 1 else ""
                    elif '：' in rest:
                        parts = rest.split('：', 1)
                        sender = parts[0].strip()
                        content = parts[1].strip() if len(parts) > 1 else ""
                    
                    current_msg = {
                        'timestamp': timestamp,
                        'sender': sender,
                        'content': content,
                        'source': 'timestamp_txt'
                    }
                elif current_msg:
                    if current_msg['content']:
                        current_msg['content'] += '\n'
                    current_msg['content'] += line
        
        if current_msg:
            messages.append(current_msg)
        
        logger.info(f"从时间戳文本格式解析出 {len(messages)} 条消息")
        return messages
    
    def parse_plaintext(self, file_path: str) -> List[Dict[str, Any]]:
        """解析纯文本格式"""
        messages = []
        
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            lines = f.readlines()
        
        for i, line in enumerate(lines):
            line = line.strip()
            if line:
                # 尝试提取发送者和内容
                if ':' in line and not line.startswith('http'):
                    parts = line.split(':', 1)
                    sender = parts[0].strip()
                    content = parts[1].strip() if len(parts) > 1 else ""
                elif '：' in line:
                    parts = line.split('：', 1)
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
    
    def categorize_messages(self, messages: List[Dict[str, Any]]) -> Dict[str, Any]:
        """分类消息"""
        teacher_keywords = ["老师", "教师", "班主任", "教授", "导师"]
        group_keywords = ["群", "组", "班", "集体"]
        file_keywords = ["文件", "图片", "文档", "课件", "教案", "资料", "http", "https", ".", "发送了一个"]
        teaching_keywords = ["作业", "考试", "成绩", "上课", "教学", "练习", "讲解", "知识点"]
        
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
            
            # 检查是否是群消息（如果指定了群名）
            if self.group_name and self.group_name.lower() in content.lower():
                self.group_messages.append(msg)
            
            # 检查是否包含文件分享
            is_file = False
            for keyword in file_keywords:
                if keyword in content:
                    is_file = True
                    break
            
            if is_file:
                self.file_shares.append(msg)
        
        return {
            'teacher_messages': len(self.teacher_messages),
            'group_messages': len(self.group_messages),
            'file_shares': len(self.file_shares),
            'teaching_content': len(self.teaching_content)
        }
    
    def analyze_teaching_characteristics(self) -> Dict[str, Any]:
        """分析教学特点"""
        characteristics = {
            'communication_frequency': {
                'total': len(self.teacher_messages),
                'per_day': 0,
                'time_distribution': {}
            },
            'content_types': {
                'announcements': 0,
                'qna': 0,
                'feedback': 0,
                'encouragement': 0
            },
            'file_types': {
                'documents': 0,
                'images': 0,
                'links': 0,
                'other': 0
            }
        }
        
        # 分析沟通频率（按时间分布）
        time_patterns = {
            'morning': 0,    # 6:00-12:00
            'afternoon': 0,  # 12:00-18:00
            'evening': 0,    # 18:00-22:00
            'night': 0       # 22:00-6:00
        }
        
        for msg in self.teacher_messages:
            timestamp = msg.get('timestamp', '')
            if timestamp:
                try:
                    # 提取时间部分
                    time_match = re.search(r'(\d{1,2}):\d{2}:\d{2}', timestamp)
                    if time_match:
                        hour = int(time_match.group(1))
                        if 6 <= hour < 12:
                            time_patterns['morning'] += 1
                        elif 12 <= hour < 18:
                            time_patterns['afternoon'] += 1
                        elif 18 <= hour < 22:
                            time_patterns['evening'] += 1
                        else:
                            time_patterns['night'] += 1
                except:
                    pass
        
        characteristics['communication_frequency']['time_distribution'] = time_patterns
        
        # 分析内容类型
        announcement_keywords = ["通知", "公告", "提醒", "注意", "重要"]
        qna_keywords = ["问题", "解答", "回答", "疑问", "不懂"]
        feedback_keywords = ["批改", "评价", "反馈", "建议", "修改"]
        encouragement_keywords = ["加油", "很棒", "优秀", "进步", "表扬"]
        
        for msg in self.teacher_messages:
            content = msg.get('content', '').lower()
            
            if any(keyword in content for keyword in announcement_keywords):
                characteristics['content_types']['announcements'] += 1
            
            if any(keyword in content for keyword in qna_keywords):
                characteristics['content_types']['qna'] += 1
            
            if any(keyword in content for keyword in feedback_keywords):
                characteristics['content_types']['feedback'] += 1
            
            if any(keyword in content for keyword in encouragement_keywords):
                characteristics['content_types']['encouragement'] += 1
        
        # 分析文件类型
        for msg in self.file_shares:
            content = msg.get('content', '').lower()
            
            if any(ext in content for ext in ['.doc', '.docx', '.pdf', '.ppt', '.pptx', '.xls', '.xlsx']):
                characteristics['file_types']['documents'] += 1
            elif any(ext in content for ext in ['.jpg', '.jpeg', '.png', '.gif', '.bmp']):
                characteristics['file_types']['images'] += 1
            elif 'http' in content or 'https' in content:
                characteristics['file_types']['links'] += 1
            else:
                characteristics['file_types']['other'] += 1
        
        return characteristics
    
    def parse_file(self, file_path: str) -> Dict[str, Any]:
        """解析文件主函数"""
        if not Path(file_path).exists():
            return {"status": "error", "message": f"文件不存在: {file_path}"}
        
        # 检测并解析格式
        file_format = self.detect_format(file_path)
        logger.info(f"检测到文件格式: {file_format}")
        
        if file_format == 'qq_export':
            messages = self.parse_qq_export(file_path)
        elif file_format == 'qq_mht':
            messages = self.parse_qq_mht(file_path)
        elif file_format == 'timestamp_txt':
            messages = self.parse_timestamp_txt(file_path)
        else:
            messages = self.parse_plaintext(file_path)
        
        if not messages:
            return {"status": "error", "message": "未能解析出任何消息"}
        
        # 分类消息
        categories = self.categorize_messages(messages)
        
        # 分析教学特点
        characteristics = self.analyze_teaching_characteristics()
        
        # 生成报告
        report = {
            "status": "success",
            "teacher": self.teacher_name,
            "group": self.group_name,
            "file_format": file_format,
            "total_messages": len(messages),
            "categories": categories,
            "characteristics": characteristics,
            "sample_data": {
                "teacher_messages": self.teacher_messages[:5] if self.teacher_messages else [],
                "file_shares": self.file_shares[:3] if self.file_shares else [],
                "teaching_content": self.teaching_content[:3] if self.teaching_content else []
            }
        }
        
        return report
    
    def save_results(self, report: Dict[str, Any], output_dir: Optional[str] = None) -> str:
        """保存解析结果"""
        if output_dir:
            output_path = Path(output_dir)
        else:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_path = Path(f"./qq_analysis/{self.teacher_name}_{timestamp}")
        
        output_path.mkdir(parents=True, exist_ok=True)
        
        # 保存报告
        report_path = output_path / "analysis_report.json"
        report_path.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
        
        # 保存教师消息
        if self.teacher_messages:
            teacher_msg_path = output_path / "teacher_messages.json"
            teacher_msg_path.write_text(json.dumps(self.teacher_messages, indent=2, ensure_ascii=False), encoding="utf-8")
        
        # 保存文件分享记录
        if self.file_shares:
            files_path = output_path / "file_shares.json"
            files_path.write_text(json.dumps(self.file_shares, indent=2, ensure_ascii=False), encoding="utf-8")
        
        # 保存教学相关内容
        if self.teaching_content:
            teaching_path = output_path / "teaching_content.json"
            teaching_path.write_text(json.dumps(self.teaching_content, indent=2, ensure_ascii=False), encoding="utf-8")
        
        logger.info(f"解析结果已保存到: {output_path}")
        return str(output_path.absolute())


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description="QQ聊天记录解析器 - 教师版")
    parser.add_argument("--file", type=str, required=True, help="聊天记录文件路径")
    parser.add_argument("--teacher", type=str, required=True, help="教师姓名")
    parser.add_argument("--group", type=str, help="QQ群名称")
    parser.add_argument("