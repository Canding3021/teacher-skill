#!/usr/bin/env python3
"""
飞书自动采集器 - 教师版

专门用于采集教师相关的飞书数据：
1. 教师参与的群聊消息（教研组、备课组、年级组等）
2. 教师创建的文档（教案、课件、教学反思等）
3. 教师参与的多维表格（成绩表、考勤表等）

用法：
  python3 feishu_auto_collector.py --name "张老师" --subject "数学"
  python3 feishu_auto_collector.py --name "李老师" --output-dir ./materials/li_teacher
"""

import json
import sys
import time
import argparse
from pathlib import Path
from datetime import datetime, timezone
from typing import Optional, List, Dict, Any
import logging

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

try:
    import requests
except ImportError:
    print("错误：请先安装 requests：pip3 install requests", file=sys.stderr)
    sys.exit(1)

CONFIG_PATH = Path.home() / ".teacher-skill" / "feishu_config.json"


class FeishuAutoCollector:
    """飞书自动采集器 - 教师专用版"""
    
    def __init__(self, app_id: str, app_secret: str):
        self.app_id = app_id
        self.app_secret = app_secret
        self.session = requests.Session()
        self.session.headers.update({
            "Content-Type": "application/json",
            "User-Agent": "TeacherSkill-FeishuCollector/1.0"
        })
        self.base_url = "https://open.feishu.cn/open-apis"
        
    def _get_tenant_access_token(self) -> str:
        """获取租户访问令牌"""
        url = f"{self.base_url}/auth/v3/tenant_access_token/internal"
        payload = {
            "app_id": self.app_id,
            "app_secret": self.app_secret
        }
        
        try:
            response = self.session.post(url, json=payload, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            if data.get("code") == 0:
                token = data["tenant_access_token"]
                logger.info("成功获取租户访问令牌")
                return token
            else:
                logger.error(f"获取令牌失败: {data.get('msg', '未知错误')}")
                sys.exit(1)
                
        except Exception as e:
            logger.error(f"获取租户访问令牌时出错: {e}")
            sys.exit(1)
    
    def collect_teacher_materials(self, teacher_name: str, subject: Optional[str] = None,
                                 output_dir: Optional[str] = None) -> Dict[str, Any]:
        """收集教师材料的主函数"""
        logger.info(f"开始收集教师材料: {teacher_name} ({subject or '未指定学科'})")
        
        # 创建输出目录
        if output_dir:
            output_path = Path(output_dir)
        else:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_path = Path(f"./materials/{teacher_name}_{timestamp}")
        
        output_path.mkdir(parents=True, exist_ok=True)
        
        # 模拟收集过程（实际实现需要飞书API权限）
        teacher_info = {
            "name": teacher_name,
            "subject": subject,
            "collection_time": datetime.now(timezone.utc).isoformat(),
            "note": "这是一个演示版本，实际使用需要配置飞书应用权限"
        }
        
        # 保存教师信息
        teacher_info_path = output_path / "teacher_info.json"
        teacher_info_path.write_text(json.dumps(teacher_info, indent=2, ensure_ascii=False), encoding="utf-8")
        
        # 创建示例数据
        example_messages = [
            {
                "sender": teacher_name,
                "content": f"同学们，今天的{subject or '数学'}作业是...",
                "time": "2026-04-10 14:30:00",
                "chat": "高一数学备课组"
            },
            {
                "sender": teacher_name,
                "content": "这个知识点很重要，大家要重点掌握",
                "time": "2026-04-09 10:15:00",
                "chat": "教研组群"
            }
        ]
        
        example_docs = [
            {
                "title": f"{subject or '数学'}教案 - 第1单元",
                "type": "doc",
                "content": f"这是{teacher_name}老师的{subject or '数学'}教案示例..."
            }
        ]
        
        # 保存示例数据
        messages_path = output_path / "messages.json"
        messages_path.write_text(json.dumps(example_messages, indent=2, ensure_ascii=False), encoding="utf-8")
        
        docs_path = output_path / "docs.json"
        docs_path.write_text(json.dumps(example_docs, indent=2, ensure_ascii=False), encoding="utf-8")
        
        # 生成汇总报告
        summary = {
            "teacher": teacher_info,
            "collection_time": datetime.now(timezone.utc).isoformat(),
            "statistics": {
                "messages_collected": len(example_messages),
                "docs_collected": len(example_docs),
                "output_directory": str(output_path.absolute())
            },
            "note": "这是演示版本。实际使用需要：\n1. 在飞书开放平台创建应用\n2. 申请相应权限\n3. 配置App ID和Secret"
        }
        
        summary_path = output_path / "summary.json"
        summary_path.write_text(json.dumps(summary, indent=2, ensure_ascii=False), encoding="utf-8")
        
        logger.info(f"材料收集完成! 输出目录: {output_path}")
        logger.info("注意：这是演示版本，实际使用需要配置飞书应用权限")
        
        return {
            "status": "success",
            "summary": summary,
            "output_dir": str(output_path.absolute())
        }


def setup_config() -> None:
    """配置飞书应用"""
    print("=== 飞书自动采集配置 - 教师版 ===\n")
    print("请前往 https://open.feishu.cn 创建企业自建应用，开通以下权限：\n")
    
    print("必需权限（应用权限）：")
    print("  1. 消息与群组")
    print("     • im:message:readonly          读取消息")
    print("     • im:chat:readonly             读取群聊信息")
    print("     • im:chat.members:readonly     读取群成员")
    print()
    print("  2. 通讯录")
    print("     • contact:user.base:readonly       读取用户基本信息")
    print("     • contact:department.base:readonly  遍历部门查找用户")
    print()
    print("  3. 云文档")
    print("     • docs:doc:readonly            读取文档")
    print("     • drive:drive:readonly         搜索云盘文件")
    print()
    
    config = {}
    config["app_id"] = input("请输入 App ID: ").strip()
    config["app_secret"] = input("请输入 App Secret: ").strip()
    
    # 保存配置
    CONFIG_PATH.parent.mkdir(parents=True, exist_ok=True)
    CONFIG_PATH.write_text(json.dumps(config, indent=2, ensure_ascii=False), encoding="utf-8")
    
    print(f"\n✅ 配置已保存到: {CONFIG_PATH}")
    print("\n下一步：")
    print("1. 在飞书开放平台发布应用版本")
    print("2. 申请开通上述权限")
    print("3. 等待管理员审核通过")
    print("4. 开始使用采集功能")


def load_config() -> Dict[str, str]:
    """加载配置"""
    if not CONFIG_PATH.exists():
        logger.error(f"未找到配置文件: {CONFIG_PATH}")
        logger.info("请先运行: python3 feishu_auto_collector.py --setup")
        sys.exit(1)
    
    try:
        return json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
    except Exception as e:
        logger.error(f"读取配置文件失败: {e}")
        sys.exit(1)


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description="飞书自动采集器 - 教师版")
    parser.add_argument("--setup", action="store_true", help="配置飞书应用")
    parser.add_argument("--name", type=str, required=False, help="教师姓名")
    parser.add_argument("--subject", type=str, help="教师学科")
    parser.add_argument("--output-dir", type=str, help="输出目录")
    
    args = parser.parse_args()
    
    if args.setup:
        setup_config()
        return
    
    if not args.name:
        print("错误：请指定教师姓名")
        parser.print_help()
        sys.exit(1)
    
    # 加载配置
    config = load_config()
    
    # 创建采集器并执行
    collector = FeishuAutoCollector(config["app_id"], config["app_secret"])
    result = collector.collect_teacher_materials(
        teacher_name=args.name,
        subject=args.subject,
        output_dir=args.output_dir
    )
    
    print("\n" + "="*60)
    print("采集结果:")
    print(json.dumps(result, indent=2, ensure_ascii=False))
    print("="*60)


if __name__ == "__main__":
    main()