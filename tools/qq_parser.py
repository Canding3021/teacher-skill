#!/usr/bin/env python3
"""
QQ chat parser for teacher-related materials.

The original file in this repository was truncated near the CLI section.
This rewrite keeps the same public class/method names while providing a
stable, syntax-safe parser for the supported export shapes.
"""

import argparse
import html
import json
import logging
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


class QQParser:
    """Parser focused on teacher-related QQ chat exports."""

    def __init__(self, teacher_name: str, group_name: Optional[str] = None):
        self.teacher_name = teacher_name
        self.group_name = group_name
        self.teacher_messages: List[Dict[str, Any]] = []
        self.group_messages: List[Dict[str, Any]] = []
        self.file_shares: List[Dict[str, Any]] = []
        self.teaching_content: List[Dict[str, Any]] = []

    def detect_format(self, file_path: str) -> str:
        ext = Path(file_path).suffix.lower()
        if ext in {".mht", ".mhtml"}:
            return "qq_mht"
        if ext == ".txt":
            preview = Path(file_path).read_text(encoding="utf-8", errors="ignore")[:2000]
            if "消息记录" in preview or "聊天记录" in preview:
                return "qq_export"
            if re.search(r"\d{4}-\d{2}-\d{2}\s+\d{1,2}:\d{2}:\d{2}", preview):
                return "timestamp_txt"
        return "plaintext"

    def parse_qq_export(self, file_path: str) -> List[Dict[str, Any]]:
        content = Path(file_path).read_text(encoding="utf-8", errors="ignore")
        pattern = re.compile(r"(\d{4}-\d{2}-\d{2}\s+\d{1,2}:\d{2}:\d{2})\s+([^(]+)\(([^)]+)\)")

        messages: List[Dict[str, Any]] = []
        current: Optional[Dict[str, Any]] = None

        for raw_line in content.splitlines():
            line = raw_line.strip()
            if not line:
                continue
            matched = pattern.match(line)
            if matched:
                if current:
                    messages.append(current)
                timestamp, sender, qq_number = matched.groups()
                current = {
                    "timestamp": timestamp,
                    "sender": sender.strip(),
                    "qq_number": qq_number.strip(),
                    "content": "",
                    "source": "qq_export",
                }
                continue
            if current is None:
                continue
            current["content"] = f"{current['content']}\n{line}".strip()

        if current:
            messages.append(current)

        logger.info("Parsed %s messages from QQ export", len(messages))
        return messages

    def parse_qq_mht(self, file_path: str) -> List[Dict[str, Any]]:
        content = Path(file_path).read_text(encoding="utf-8", errors="ignore")
        content = html.unescape(content)

        block_pattern = re.compile(r"<div[^>]*class=[\"']?message[\"']?[^>]*>(.*?)</div>", re.IGNORECASE | re.DOTALL)
        sender_pattern = re.compile(r"<span[^>]*class=[\"']?sender[\"']?[^>]*>(.*?)</span>", re.IGNORECASE | re.DOTALL)
        time_pattern = re.compile(r"<span[^>]*class=[\"']?(?:time|timestamp)[\"']?[^>]*>(.*?)</span>", re.IGNORECASE | re.DOTALL)
        content_pattern = re.compile(r"<span[^>]*class=[\"']?(?:content|text)[\"']?[^>]*>(.*?)</span>", re.IGNORECASE | re.DOTALL)
        tag_pattern = re.compile(r"<[^>]+>")

        messages: List[Dict[str, Any]] = []
        for block in block_pattern.findall(content):
            sender = sender_pattern.search(block)
            timestamp = time_pattern.search(block)
            text_match = content_pattern.search(block)
            cleaned = tag_pattern.sub("", text_match.group(1) if text_match else block).strip()
            if not cleaned:
                continue
            messages.append(
                {
                    "timestamp": tag_pattern.sub("", timestamp.group(1)).strip() if timestamp else "",
                    "sender": tag_pattern.sub("", sender.group(1)).strip() if sender else "unknown",
                    "content": cleaned,
                    "source": "qq_mht",
                }
            )

        logger.info("Parsed %s messages from QQ MHT", len(messages))
        return messages

    def parse_timestamp_txt(self, file_path: str) -> List[Dict[str, Any]]:
        content = Path(file_path).read_text(encoding="utf-8", errors="ignore")
        pattern = re.compile(r"(\d{4}-\d{2}-\d{2}\s+\d{1,2}:\d{2}:\d{2})\s+([^:：]+)[:：]\s*(.*)")

        messages: List[Dict[str, Any]] = []
        for raw_line in content.splitlines():
            line = raw_line.strip()
            if not line:
                continue
            matched = pattern.match(line)
            if not matched:
                continue
            timestamp, sender, message = matched.groups()
            messages.append(
                {
                    "timestamp": timestamp,
                    "sender": sender.strip(),
                    "content": message.strip(),
                    "source": "timestamp_txt",
                }
            )

        logger.info("Parsed %s timestamped text messages", len(messages))
        return messages

    def parse_plaintext(self, file_path: str) -> List[Dict[str, Any]]:
        content = Path(file_path).read_text(encoding="utf-8", errors="ignore").strip()
        if not content:
            return []
        return [
            {
                "timestamp": "",
                "sender": "unknown",
                "content": content,
                "source": "plaintext",
            }
        ]

    def categorize_messages(self, messages: List[Dict[str, Any]]) -> Dict[str, Any]:
        self.teacher_messages = []
        self.group_messages = []
        self.file_shares = []
        self.teaching_content = []

        teaching_keywords = ["作业", "课堂", "上课", "学生", "家长", "考试", "讲题", "教学", "备课", "教案"]
        file_keywords = ["文件", "课件", "资料", "作业包", "pdf", "ppt", "doc", "zip"]

        for message in messages:
            sender = message.get("sender", "")
            content = message.get("content", "")

            if self.teacher_name and self.teacher_name in sender:
                self.teacher_messages.append(message)
            if self.group_name:
                self.group_messages.append(message)
            if any(keyword.lower() in content.lower() for keyword in file_keywords):
                self.file_shares.append(message)
            if any(keyword in content for keyword in teaching_keywords):
                self.teaching_content.append(message)

        return {
            "teacher_messages": self.teacher_messages,
            "group_messages": self.group_messages,
            "file_shares": self.file_shares,
            "teaching_content": self.teaching_content,
        }

    def analyze_teaching_characteristics(self) -> Dict[str, Any]:
        combined_text = "\n".join(message.get("content", "") for message in self.teacher_messages)
        keywords = ["作业", "课堂", "反馈", "方法", "学生", "家长", "考试", "目标"]
        keyword_counts = {keyword: combined_text.count(keyword) for keyword in keywords if keyword in combined_text}

        return {
            "teacher_message_count": len(self.teacher_messages),
            "teaching_message_count": len(self.teaching_content),
            "file_share_count": len(self.file_shares),
            "top_keywords": keyword_counts,
            "has_group_context": bool(self.group_name),
        }

    def parse_file(self, file_path: str) -> Dict[str, Any]:
        format_name = self.detect_format(file_path)
        parser_map = {
            "qq_export": self.parse_qq_export,
            "qq_mht": self.parse_qq_mht,
            "timestamp_txt": self.parse_timestamp_txt,
            "plaintext": self.parse_plaintext,
        }
        messages = parser_map[format_name](file_path)
        categorized = self.categorize_messages(messages)

        return {
            "metadata": {
                "source_file": str(Path(file_path).resolve()),
                "format": format_name,
                "teacher_name": self.teacher_name,
                "group_name": self.group_name,
                "parsed_at": datetime.now().isoformat(),
                "total_messages": len(messages),
            },
            "analysis": self.analyze_teaching_characteristics(),
            "messages": categorized,
        }

    def save_results(self, report: Dict[str, Any], output_dir: Optional[str] = None) -> str:
        if output_dir:
            output_path = Path(output_dir)
        else:
            source_file = Path(report["metadata"]["source_file"])
            output_path = source_file.parent / f"{source_file.stem}_parsed"

        output_path.mkdir(parents=True, exist_ok=True)

        report_path = output_path / "qq_parser_report.json"
        report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")

        if self.teacher_messages:
            teacher_path = output_path / "teacher_messages.json"
            teacher_path.write_text(json.dumps(self.teacher_messages, ensure_ascii=False, indent=2), encoding="utf-8")

        if self.teaching_content:
            teaching_path = output_path / "teaching_content.json"
            teaching_path.write_text(json.dumps(self.teaching_content, ensure_ascii=False, indent=2), encoding="utf-8")

        logger.info("Saved QQ parser results to %s", output_path)
        return str(output_path.resolve())


def main() -> int:
    parser = argparse.ArgumentParser(description="QQ chat parser for teacher materials")
    parser.add_argument("--file", type=str, required=True, help="Path to the chat export file")
    parser.add_argument("--teacher", type=str, required=True, help="Teacher name")
    parser.add_argument("--group", type=str, help="Optional QQ group name")
    parser.add_argument("--output", type=str, help="Output directory")

    args = parser.parse_args()

    qq_parser = QQParser(teacher_name=args.teacher, group_name=args.group)
    report = qq_parser.parse_file(args.file)
    saved_path = qq_parser.save_results(report, args.output)

    print(json.dumps(report["analysis"], ensure_ascii=False, indent=2))
    print(f"\nSaved to: {saved_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
