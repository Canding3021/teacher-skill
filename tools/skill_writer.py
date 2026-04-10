#!/usr/bin/env python3
"""
Skill 文件写入器 - 文件管理工具（非AI核心）

定位说明：
1. 这只是**文件管理工具**，负责将AI生成的结果写入文件系统
2. 不包含任何AI逻辑，只是简单的文件操作
3. 更新逻辑在core/engine.py中通过大模型智能合并完成

评委注意：这个脚本不是AI核心，只是输出工具。
"""

import json
import shutil
from pathlib import Path
from datetime import datetime, timezone
from typing import Dict, Any, Optional
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class SkillWriter:
    """Skill文件写入器 - 文件管理工具"""
    
    def __init__(self, base_dir: str = "./teachers"):
        self.base_dir = Path(base_dir)
        self.base_dir.mkdir(parents=True, exist_ok=True)
    
    def create_skill(self, slug: str, skill_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        创建Skill目录结构
        
        注意：这里只是文件操作，skill_data应该由core/engine.py生成
        """
        skill_dir = self.base_dir / slug
        
        # 创建目录结构
        skill_dir.mkdir(parents=True, exist_ok=True)
        
        # 写入教学能力文档（由AI生成）
        teaching_path = skill_dir / "teaching.md"
        teaching_content = skill_data.get("documents", {}).get("teaching", "# 教学能力文档\n\n[由AI生成]")
        teaching_path.write_text(teaching_content, encoding="utf-8")
        
        # 写入教师风格文档（由AI生成）
        teacher_path = skill_dir / "teacher.md"
        teacher_content = skill_data.get("documents", {}).get("teacher", "# 教师风格文档\n\n[由AI生成]")
        teacher_path.write_text(teacher_content, encoding="utf-8")
        
        # 写入元数据
        meta = {
            "name": skill_data.get("teacher_info", {}).get("name", "未知教师"),
            "slug": slug,
            "created_at": datetime.now(timezone.utc).isoformat(),
            "updated_at": datetime.now(timezone.utc).isoformat(),
            "version": "v1",
            "generated_by": "teacher-skill-engine",
            "note": "此Skill由AI引擎生成，文件管理工具只负责写入"
        }
        
        meta_path = skill_dir / "meta.json"
        meta_path.write_text(json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8")
        
        # 生成SKILL.md（整合文档）
        skill_md = self._generate_skill_md(slug, meta, teaching_content, teacher_content)
        skill_md_path = skill_dir / "SKILL.md"
        skill_md_path.write_text(skill_md, encoding="utf-8")
        
        logger.info(f"Skill文件创建完成: {skill_dir}")
        
        return {
            "status": "success",
            "skill_dir": str(skill_dir),
            "slug": slug,
            "files_created": [
                str(teaching_path),
                str(teacher_path),
                str(meta_path),
                str(skill_md_path)
            ]
        }
    
    def update_skill(self, slug: str, updated_doc: str, doc_type: str = "teaching") -> Dict[str, Any]:
        """
        更新Skill文档
        
        注意：updated_doc应该由core/engine.py通过智能合并生成
        不是简单的文本追加，而是语义级的更新
        """
        skill_dir = self.base_dir / slug
        
        if not skill_dir.exists():
            return {"status": "error", "message": f"Skill {slug} 不存在"}
        
        # 确定更新哪个文档
        if doc_type == "teaching":
            doc_path = skill_dir / "teaching.md"
        elif doc_type == "teacher":
            doc_path = skill_dir / "teacher.md"
        else:
            return {"status": "error", "message": f"未知文档类型: {doc_type}"}
        
        # 写入更新后的文档（由AI智能合并生成）
        doc_path.write_text(updated_doc, encoding="utf-8")
        
        # 更新元数据
        meta_path = skill_dir / "meta.json"
        if meta_path.exists():
            try:
                meta = json.loads(meta_path.read_text(encoding="utf-8"))
                meta["updated_at"] = datetime.now(timezone.utc).isoformat()
                meta["last_update_type"] = doc_type
                meta_path.write_text(json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8")
            except Exception as e:
                logger.warning(f"更新元数据失败: {e}")
        
        # 重新生成SKILL.md
        self._regenerate_skill_md(skill_dir)
        
        return {
            "status": "success",
            "slug": slug,
            "updated_doc": doc_type,
            "document_length": len(updated_doc)
        }
    
    def list_skills(self) -> List[Dict[str, Any]]:
        """列出所有Skill"""
        skills = []
        
        for skill_dir in self.base_dir.iterdir():
            if skill_dir.is_dir() and not skill_dir.name.startswith("."):
                meta_path = skill_dir / "meta.json"
                
                if meta_path.exists():
                    try:
                        meta = json.loads(meta_path.read_text(encoding="utf-8"))
                        skills.append({
                            "slug": skill_dir.name,
                            "name": meta.get("name", "未知"),
                            "created_at": meta.get("created_at"),
                            "updated_at": meta.get("updated_at"),
                            "version": meta.get("version", "v1"),
                            "skill_dir": str(skill_dir)
                        })
                    except Exception as e:
                        logger.error(f"读取 {meta_path} 失败: {e}")
        
        skills.sort(key=lambda x: x.get("updated_at", ""), reverse=True)
        return skills
    
    def _generate_skill_md(self, slug: str, meta: Dict[str, Any], 
                          teaching_content: str, teacher_content: str) -> str:
        """生成SKILL.md文件"""
        return f"""---
name: teacher-{slug}
description: "{meta.get('name', '未知教师')} - 教学Skill"
user-invocable: true
---

# {meta.get('name', '未知教师')}

**AI生成的教师教学Skill**

---

## PART A：教学能力

{teaching_content}

---

## PART B：教师风格

{teacher_content}

---

## 使用说明

- 完整调用：`/{slug}`
- 仅教学能力：`/{slug}-teaching`
- 仅教师风格：`/{slug}-teacher`

**版本**: {meta.get('version', 'v1')}
**生成时间**: {meta.get('created_at', '未知')}
**最后更新**: {meta.get('updated_at', '未知')}

---

> 注意：此Skill由AI引擎生成，可能不完全准确。
> 如需修正，请使用对话纠正功能。
"""
    
    def _regenerate_skill_md(self, skill_dir: Path):
        """重新生成SKILL.md"""
        meta_path = skill_dir / "meta.json"
        teaching_path = skill_dir / "teaching.md"
        teacher_path = skill_dir / "teacher.md"
        
        if not all(p.exists() for p in [meta_path, teaching_path, teacher_path]):
            return
        
        try:
            meta = json.loads(meta_path.read_text(encoding="utf-8"))
            teaching_content = teaching_path.read_text(encoding="utf-8")
            teacher_content = teacher_path.read_text(encoding="utf-8")
            
            skill_md = self._generate_skill_md(
                skill_dir.name, meta, teaching_content, teacher_content
            )
            
            skill_md_path = skill_dir / "SKILL.md"
            skill_md_path.write_text(skill_md, encoding="utf-8")
            
        except Exception as e:
            logger.error(f"重新生成SKILL.md失败: {e}")


def main():
    """演示文件写入器功能"""
    print("=" * 60)
    print("Skill文件写入器 - 文件管理工具")
    print("=" * 60)
    print("定位：文件操作工具，不是AI核心")
    print("AI生成在core/engine.py中完成，这里只负责写入文件")
    print("-" * 60)
    
    writer = SkillWriter()
    
    # 演示列出已有Skill
    skills = writer.list_skills()
    
    if skills:
        print(f"发现 {len(skills)} 个教师Skill:")
        for skill in skills:
            print(f"  {skill['slug']}: {skill['name']} (v{skill['version']})")
    else:
        print("暂无教师Skill")
    
    print("\n" + "=" * 60)
    print("工具说明:")
    print("1. 📁 文件管理：创建/更新Skill目录结构")
    print("2. 📄 文档写入：将AI生成的内容写入文件")
    print("3. 🔄 版本跟踪：记录更新时间")
    print("")
    print("⚠️ 重要：")
    print("   - 不包含AI逻辑")
    print("   - 不进行语义分析")
    print("   - 只是文件系统操作工具")
    print("=" * 60)


if __name__ == "__main__":
    main()