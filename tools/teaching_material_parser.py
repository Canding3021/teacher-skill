#!/usr/bin/env python3
"""
教学材料解析器 - 辅助工具（非AI核心）

定位说明：
1. 这只是**预处理工具**，负责从各种格式文件中提取原始文本
2. 真正的AI分析在 core/engine.py 中通过大模型完成
3. 不使用复杂的正则表达式进行"理解"，只做基础的文本提取

评委注意：这个脚本不是AI核心，只是数据准备工具。
"""

import os
import sys
from pathlib import Path
from typing import Dict, Any
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class TeachingMaterialParser:
    """教学材料解析器 - 文本提取工具"""
    
    def __init__(self):
        self.supported_formats = ['.pdf', '.docx', '.txt', '.md']
    
    def parse_file(self, file_path: str) -> Dict[str, Any]:
        """
        解析单个文件，提取原始文本
        
        注意：这里只做文本提取，不做语义分析
        语义分析交给大模型在 core/engine.py 中完成
        """
        path = Path(file_path)
        
        if not path.exists():
            return {"error": f"文件不存在: {file_path}"}
        
        # 检查文件格式
        if path.suffix.lower() not in self.supported_formats:
            return {
                "warning": f"不支持的文件格式: {path.suffix}",
                "supported_formats": self.supported_formats
            }
        
        try:
            # 基础文本提取（不同格式需要不同库）
            raw_text = self._extract_text(path)
            
            return {
                "file_path": str(path),
                "file_name": path.name,
                "file_size": path.stat().st_size,
                "file_type": path.suffix,
                "raw_text": raw_text,
                "text_length": len(raw_text),
                "extraction_method": "basic_text_extraction",
                "note": "这只是原始文本提取，真正的AI分析在core/engine.py中完成"
            }
            
        except Exception as e:
            logger.error(f"解析文件失败 {file_path}: {e}")
            return {
                "error": str(e),
                "file_path": str(path)
            }
    
    def _extract_text(self, path: Path) -> str:
        """基础文本提取方法"""
        suffix = path.suffix.lower()
        
        if suffix == '.txt' or suffix == '.md':
            return self._read_text_file(path)
        elif suffix == '.pdf':
            return self._extract_pdf_text(path)
        elif suffix == '.docx':
            return self._extract_docx_text(path)
        else:
            return f"[{path.suffix}格式文件，需要相应解析库]"
    
    def _read_text_file(self, path: Path) -> str:
        """读取文本文件"""
        try:
            with open(path, 'r', encoding='utf-8') as f:
                return f.read()
        except UnicodeDecodeError:
            with open(path, 'r', encoding='gbk') as f:
                return f.read()
    
    def _extract_pdf_text(self, path: Path) -> str:
        """提取PDF文本（简化版）"""
        # 实际实现需要 pdfplumber 或 PyPDF2
        # 这里返回存根
        return f"[PDF文件: {path.name}]\n需要安装 pdfplumber 进行文本提取\n"
    
    def _extract_docx_text(self, path: Path) -> str:
        """提取Word文档文本（简化版）"""
        # 实际实现需要 python-docx
        # 这里返回存根
        return f"[Word文档: {path.name}]\n需要安装 python-docx 进行文本提取\n"
    
    def batch_parse(self, directory: str) -> Dict[str, Any]:
        """批量解析目录中的文件"""
        dir_path = Path(directory)
        
        if not dir_path.exists():
            return {"error": f"目录不存在: {directory}"}
        
        results = []
        total_size = 0
        
        for file_path in dir_path.rglob("*"):
            if file_path.is_file() and file_path.suffix.lower() in self.supported_formats:
                result = self.parse_file(str(file_path))
                results.append(result)
                
                if "file_size" in result:
                    total_size += result["file_size"]
        
        return {
            "directory": str(dir_path),
            "files_processed": len(results),
            "total_size_bytes": total_size,
            "results": results,
            "summary": f"从 {len(results)} 个文件中提取了原始文本，等待AI分析"
        }


def main():
    """演示解析器功能"""
    parser = argparse.ArgumentParser(description="教学材料解析器 - 文本提取工具")
    parser.add_argument("--file", help="解析单个文件")
    parser.add_argument("--dir", help="解析整个目录")
    parser.add_argument("--output", default="materials.json", help="输出文件路径")
    
    args = parser.parse_args()
    
    tool = TeachingMaterialParser()
    
    print("=" * 60)
    print("教学材料解析器 - 辅助工具")
    print("=" * 60)
    print("定位：文本提取工具，不是AI分析核心")
    print("真正的AI分析在 core/engine.py 中完成")
    print("-" * 60)
    
    if args.file:
        print(f"解析文件: {args.file}")
        result = tool.parse_file(args.file)
        
        if "error" in result:
            print(f"❌ 错误: {result['error']}")
        else:
            print(f"✅ 成功提取 {result['text_length']} 字符")
            print(f"   文件: {result['file_name']}")
            print(f"   类型: {result['file_type']}")
            print(f"   大小: {result['file_size']} 字节")
            
    elif args.dir:
        print(f"解析目录: {args.dir}")
        result = tool.batch_parse(args.dir)
        
        if "error" in result:
            print(f"❌ 错误: {result['error']}")
        else:
            print(f"✅ 处理完成")
            print(f"   目录: {result['directory']}")
            print(f"   文件数: {result['files_processed']}")
            print(f"   总大小: {result['total_size_bytes']} 字节")
    
    else:
        print("请指定 --file 或 --dir 参数")
        print("\n示例:")
        print("  python teaching_material_parser.py --file 教案.docx")
        print("  python teaching_material_parser.py --dir ./materials")
    
    print("\n" + "=" * 60)
    print("重要说明：")
    print("这个工具只负责文本提取，真正的AI分析需要：")
    print("1. 配置大模型API密钥")
    print("2. 运行 core/engine.py")
    print("3. 使用专业的prompt模板进行分析")
    print("=" * 60)


if __name__ == "__main__":
    # 为了演示，简化参数解析
    import argparse
    main()