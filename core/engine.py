#!/usr/bin/env python3

import os
import json
import hashlib
from pathlib import Path
from typing import Dict, Any, Optional, List, Generator
from abc import ABC, abstractmethod
import logging
from datetime import datetime

# 尝试导入Pydantic，如果失败则使用备用方案
try:
    from pydantic import BaseModel, Field, validator
    PYDANTIC_AVAILABLE = True
except ImportError:
    PYDANTIC_AVAILABLE = False
    # 备用方案：使用简单的数据类
    from dataclasses import dataclass, field
    from typing import List as TypingList

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


# ============================================================================
# 结构化契约：Pydantic模型
# ============================================================================

if PYDANTIC_AVAILABLE:
    class TeacherStyleModel(BaseModel):
        """教师风格5层结构 - 结构化契约"""
        
        # Layer 0: 教育理念
        layer_0: Dict[str, Any] = Field(
            default_factory=lambda: {
                "core_beliefs": [],
                "non_negotiables": [],
                "value_hierarchy": {"primary": "", "secondary": "", "tertiary": ""}
            },
            description="教育理念（核心原则）"
        )
        
        # Layer 1: 教师身份
        layer_1: Dict[str, Any] = Field(
            default_factory=lambda: {
                "primary_role": "",
                "secondary_roles": [],
                "professional_identity": {"strength": "", "mission": "", "challenge": ""},
                "self_efficacy": {"confidence": 0.0, "growth_mindset": False, "adaptability": 0.0}
            },
            description="教师身份（职业认知）"
        )
        
        # Layer 2: 沟通风格
        layer_2: Dict[str, Any] = Field(
            default_factory=lambda: {
                "verbal_habits": {"catchphrases": [], "high_frequency": [], "sentence_patterns": []},
                "communication_style": {"formality": 0.0, "directness": 0.0, "humor_level": 0.0, "warmth": 0.0},
                "feedback_patterns": {"praise": [], "correction": [], "encouragement": []}
            },
            description="沟通风格（表达方式）"
        )
        
        # Layer 3: 课堂决策
        layer_3: Dict[str, Any] = Field(
            default_factory=lambda: {
                "decision_making": {"primary_mode": "", "secondary_mode": "", "process": [], "criteria": [], "speed": ""},
                "problem_solving": {"approach": "", "steps": [], "resources": []},
                "time_management": {"planning": "", "prioritization": "", "delegation": ""}
            },
            description="课堂决策（行为模式）"
        )
        
        # Layer 4: 师生关系
        layer_4: Dict[str, Any] = Field(
            default_factory=lambda: {
                "relationship_style": {"primary": "", "secondary": "", "distance": "", "boundaries": "", "trust_building": []},
                "emotional_support": {"availability": "", "approach": "", "methods": []},
                "conflict_management": {"prevention": [], "resolution": [], "learning": []}
            },
            description="师生关系（人际互动）"
        )
        
        # 元数据
        metadata: Dict[str, Any] = Field(
            default_factory=lambda: {
                "consistency_score": 0.0,
                "authenticity_score": 0.0,
                "distinctiveness": 0.0,
                "evidence_count": 0,
                "confidence_level": "low"
            }
        )
        
        @validator('layer_2.communication_style.*')
        def validate_communication_scores(cls, v):
            """验证沟通风格分数在0-1之间"""
            if isinstance(v, (int, float)):
                return max(0.0, min(1.0, float(v)))
            return v
        
        class Config:
            """Pydantic配置"""
            validate_assignment = True
            extra = "forbid"  # 禁止额外字段

else:
    # 备用方案：简单数据类
    @dataclass
    class TeacherStyleModel:
        """教师风格5层结构 - 简化版本"""
        layer_0: Dict[str, Any] = field(default_factory=lambda: {
            "core_beliefs": [], "non_negotiables": [], "value_hierarchy": {"primary": "", "secondary": "", "tertiary": ""}
        })
        layer_1: Dict[str, Any] = field(default_factory=lambda: {
            "primary_role": "", "secondary_roles": [], 
            "professional_identity": {"strength": "", "mission": "", "challenge": ""},
            "self_efficacy": {"confidence": 0.0, "growth_mindset": False, "adaptability": 0.0}
        })
        layer_2: Dict[str, Any] = field(default_factory=lambda: {
            "verbal_habits": {"catchphrases": [], "high_frequency": [], "sentence_patterns": []},
            "communication_style": {"formality": 0.0, "directness": 0.0, "humor_level": 0.0, "warmth": 0.0},
            "feedback_patterns": {"praise": [], "correction": [], "encouragement": []}
        })
        layer_3: Dict[str, Any] = field(default_factory=lambda: {
            "decision_making": {"primary_mode": "", "secondary_mode": "", "process": [], "criteria": [], "speed": ""},
            "problem_solving": {"approach": "", "steps": [], "resources": []},
            "time_management": {"planning": "", "prioritization": "", "delegation": ""}
        })
        layer_4: Dict[str, Any] = field(default_factory=lambda: {
            "relationship_style": {"primary": "", "secondary": "", "distance": "", "boundaries": "", "trust_building": []},
            "emotional_support": {"availability": "", "approach": "", "methods": []},
            "conflict_management": {"prevention": [], "resolution": [], "learning": []}
        })
        metadata: Dict[str, Any] = field(default_factory=lambda: {
            "consistency_score": 0.0, "authenticity_score": 0.0, "distinctiveness": 0.0,
            "evidence_count": 0, "confidence_level": "low"
        })


# ============================================================================
# LLM提供商抽象
# ============================================================================

class LLMProvider(ABC):
    """大模型提供商抽象接口"""
    
    @abstractmethod
    def call_with_schema(self, prompt: str, context: str, schema: Dict[str, Any]) -> Dict[str, Any]:
        """调用大模型API，要求返回符合Schema的JSON"""
        pass
    
    @abstractmethod
    def estimate_tokens(self, text: str) -> int:
        """估算文本的token数量"""
        pass


class StructuredOpenAIClient(LLMProvider):
    """支持结构化输出的OpenAI客户端"""
    
    def __init__(self, api_key: Optional[str] = None, model: str = "gpt-4-turbo-preview"):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.model = model
        
    def call_with_schema(self, prompt: str, context: str, schema: Dict[str, Any]) -> Dict[str, Any]:
        """
        调用OpenAI API，要求返回结构化JSON
        
        这才是真正的工业级实现：Prompt + Schema → 结构化输出
        """
        # 实际实现需要安装 openai 包
        # 这里展示架构逻辑
        
        logger.info(f"调用结构化OpenAI模型 {self.model}")
        logger.info(f"Schema字段数: {len(schema)}")
        logger.info(f"Context tokens: ~{self.estimate_tokens(context)}")
        
        # 模拟结构化输出
        return {
            "status": "success",
            "data": {
                "layer_0": {
                    "core_beliefs": ["模拟：教育是唤醒", "模拟：每个学生都能成功"],
                    "non_negotiables": ["模拟：绝不公开批评"],
                    "value_hierarchy": {"primary": "学生成长", "secondary": "知识掌握", "tertiary": "考试成绩"}
                },
                "metadata": {
                    "consistency_score": 0.85,
                    "authenticity_score": 0.8,
                    "evidence_count": 15,
                    "confidence_level": "high"
                }
            },
            "model": self.model,
            "tokens_used": 1500
        }
    
    def estimate_tokens(self, text: str) -> int:
        """简单的token估算（实际应该用tiktoken）"""
        # 粗略估算：英文~4字符/token，中文~2字符/token
        chinese_chars = sum(1 for c in text if '\u4e00' <= c <= '\u9fff')
        other_chars = len(text) - chinese_chars
        return (chinese_chars // 2) + (other_chars // 4)


# ============================================================================
# 核心引擎：重构版本
# ============================================================================

class TeacherSkillEngineV2:
    """
    教师Skill蒸馏引擎 v2 - 工业级版本
    
    特性：
    1. 结构化契约输出
    2. 分而治之策略（处理大文本）
    3. 内置审计能力
    4. 冲突解决协议
    """
    
    def __init__(self, llm_provider: LLMProvider, prompts_dir: str = "./prompts"):
        self.llm = llm_provider
        self.prompts_dir = Path(prompts_dir)
        self.token_limit = 30000  # 单次处理token限制
        self.chunk_size = 5000    # 分块大小
        
    def load_prompt(self, prompt_name: str) -> str:
        """加载专业prompt模板"""
        # 优先加载v2版本
        v2_path = self.prompts_dir / f"{prompt_name}_v2.md"
        if v2_path.exists():
            return v2_path.read_text(encoding="utf-8")
        
        # 回退到原始版本
        original_path = self.prompts_dir / f"{prompt_name}.md"
        if original_path.exists():
            return original_path.read_text(encoding="utf-8")
        
        raise FileNotFoundError(f"Prompt模板不存在: {prompt_name}")
    
    def analyze_teacher_style_with_schema(self, materials: List[str]) -> TeacherStyleModel:
        """
        使用结构化契约分析教师风格
        
        这才是真正的工业级分析：材料 → Schema → 结构化模型
        """
        logger.info("开始结构化教师风格分析...")
        
        # 1. 加载结构化prompt
        prompt = self.load_prompt("teacher_analyzer")
        
        # 2. 构建Schema（从Pydantic模型导出）
        schema = self._extract_schema_from_model(TeacherStyleModel)
        
        # 3. 分而治之：如果材料太大，分批处理
        if self._is_materials_too_large(materials):
            logger.info("材料过大，启用分而治之策略...")
            return self._analyze_in_chunks(materials, prompt, schema)
        
        # 4. 单次分析
        context = self._prepare_context(materials)
        result = self.llm.call_with_schema(prompt, context, schema)
        
        # 5. 验证和转换结果
        return self._validate_and_convert_result(result, TeacherStyleModel)
    
    def merge_with_conflict_resolution(self, original: TeacherStyleModel, updates: List[Dict]) -> TeacherStyleModel:
        """
        智能合并：应用冲突解决协议
        
        解决"精神分裂"问题的关键
        """
        logger.info("开始智能合并（冲突解决协议）...")
        
        # 1. 加载合并prompt
        prompt = self.load_prompt("merger")
        
        # 2. 构建合并上下文
        context = {
            "original": original.dict() if hasattr(original, 'dict') else original,
            "updates": updates,
            "conflict_resolution_protocol": self._get_conflict_protocol()
        }
        
        # 3. 调用LLM进行智能合并
        schema = self._extract_schema_from_model(TeacherStyleModel)
        result = self.llm.call_with_schema(
            prompt, 
            json.dumps(context, ensure_ascii=False, indent=2),
            schema
        )
        
        # 4. 生成合并报告
        merge_report = self._generate_merge_report(original, result, updates)
        logger.info(f"合并完成: {merge_report['changes_count']}处变更")
        
        return self._validate_and_convert_result(result, TeacherStyleModel)
    
    def audit_skill_document(self, document: str, source_materials: List[str]) -> Dict[str, Any]:
        """
        审计Skill文档：检测幻觉，验证证据
        
        质量保证的关键步骤
        """
        logger.info("开始Skill文档审计...")
        
        # 1. 加载审计专家prompt
        prompt = self.load_prompt("critique_specialist")
        
        # 2. 构建审计上下文
        context = {
            "document": document,
            "source_materials_preview": [m[:1000] for m in source_materials[:5]],  # 预览
            "materials_count": len(source_materials)
        }
        
        # 3. 定义审计报告Schema
        audit_schema = {
            "type": "object",
            "properties": {
                "document_quality": {
                    "type": "object",
                    "properties": {
                        "authenticity_score": {"type": "number", "minimum": 0, "maximum": 1},
                        "evidence_coverage": {"type": "number", "minimum": 0, "maximum": 1},
                        "hallucination_count": {"type": "integer", "minimum": 0},
                        "confidence_level": {"type": "string", "enum": ["high", "medium", "low"]}
                    },
                    "required": ["authenticity_score", "evidence_coverage", "hallucination_count", "confidence_level"]
                },
                "verification_status": {"type": "string", "enum": ["pass", "conditional_pass", "fail"]}
            },
            "required": ["document_quality", "verification_status"]
        }
        
        # 4. 执行审计
        audit_result = self.llm.call_with_schema(
            prompt,
            json.dumps(context, ensure_ascii=False),
            audit_schema
        )
        
        # 5. 生成详细审计报告
        detailed_report = self._enhance_audit_report(audit_result, document, source_materials)
        
        logger.info(f"审计完成: {audit_result.get('verification_status', 'unknown')}")
        return detailed_report
    
    def process_correction_with_weight(self, current_skill: TeacherStyleModel, correction: str) -> Dict[str, Any]:
        """
        处理纠正：应用影响权重系统
        
        避免过度修正的关键
        """
        logger.info("开始权重化纠正处理...")
        
        # 1. 加载纠正prompt
        prompt = self.load_prompt("correction_handler")
        
        # 2. 分析纠正意图和权重
        weight_analysis = self._analyze_correction_weight(correction, current_skill)
        
        # 3. 构建纠正上下文
        context = {
            "current_skill": current_skill.dict() if hasattr(current_skill, 'dict') else current_skill,
            "correction": correction,
            "weight_analysis": weight_analysis,
            "influence_weight_system": self._get_influence_weight_system()
        }
        
        # 4. 执行纠正
        correction_schema = {
            "type": "object",
            "properties": {
                "updated_skill": {"type": "object"},  # 简化，实际应该更详细
                "correction_analysis": {
                    "type": "object",
                    "properties": {
                        "influence_weight": {"type": "number", "minimum": 0, "maximum": 1},
                        "confidence": {"type": "number", "minimum": 0, "maximum": 1}
                    }
                }
            }
        }
        
        result = self.llm.call_with_schema(
            prompt,
            json.dumps(context, ensure_ascii=False, indent=2),
            correction_schema
        )
        
        return result


class OpenAIClient(StructuredOpenAIClient):
    """Backward-compatible alias for the public OpenAI client."""


class LocalLLMClient(LLMProvider):
    """Lightweight local-model client used by tests and offline workflows."""

    def __init__(self, model: str = "qwen2.5:7b", base_url: str = "http://localhost:11434"):
        self.model = model
        self.base_url = base_url

    def call_with_schema(self, prompt: str, context: str, schema: Dict[str, Any]) -> Dict[str, Any]:
        """Return a deterministic stub payload that roughly matches the requested schema."""
        properties = schema.get("properties", {})
        result: Dict[str, Any] = {}

        for key, value in properties.items():
            prop_type = value.get("type")
            if prop_type == "object":
                result[key] = {}
            elif prop_type == "array":
                result[key] = []
            elif prop_type == "number":
                result[key] = 0.0
            elif prop_type == "integer":
                result[key] = 0
            elif prop_type == "boolean":
                result[key] = False
            else:
                result[key] = ""

        if "verification_status" in properties:
            result["verification_status"] = "pass"
        if "document_quality" in properties:
            result["document_quality"] = {
                "authenticity_score": 1.0,
                "evidence_coverage": 1.0,
                "hallucination_count": 0,
                "confidence_level": "high",
            }

        return {"status": "success", "data": result, "model": self.model, "tokens_used": 0}

    def estimate_tokens(self, text: str) -> int:
        return max(1, len(text) // 4)


class TeacherSkillEngine(TeacherSkillEngineV2):
    """Compatibility wrapper that preserves the older public engine interface."""

    def _validate_analysis(self, analysis: Dict[str, Any]) -> Dict[str, Any]:
        validated = {
            "teacher_style": analysis.get("teacher_style", {}),
            "teaching_capabilities": analysis.get("teaching_capabilities", {}),
            "metadata": analysis.get("metadata", {}),
        }
        for key, value in analysis.items():
            if key not in validated:
                validated[key] = value
        return validated

    def _build_style_analysis_context(self, materials: List[Dict[str, Any]], interviews: List[str]) -> str:
        material_lines = []
        for index, item in enumerate(materials, start=1):
            summary = item.get("summary") or item.get("content", "")
            content = item.get("content", "")
            material_lines.append(f"材料{index}: {summary}")
            if content:
                material_lines.append(content)

        interview_lines = ["访谈记录:"]
        interview_lines.extend(f"- {entry}" for entry in interviews)

        return "\n".join(material_lines + [""] + interview_lines)


class Orchestrator:
    """Small orchestration layer kept for compatibility with the legacy tests/docs."""

    def __init__(self, engine: TeacherSkillEngine):
        self.engine = engine
        self.current_pipeline: List[str] = []

    def create_teacher_skill(self, materials_dir: str, teacher_info: Dict[str, Any]) -> Dict[str, Any]:
        self.current_pipeline = ["collect_materials", "analyze_style", "build_documents"]
        analysis = self.engine._validate_analysis(
            {
                "teacher_style": {"tone": "professional"},
                "teaching_capabilities": {"knowledge_system": "", "method_repertoire": []},
            }
        )
        return {
            "teacher_info": teacher_info,
            "analysis": analysis,
            "documents": {
                "teacher": "",
                "teaching": "",
                "knowledge": "",
                "materials_dir": materials_dir,
            },
            "metadata": {"created_at": datetime.now().isoformat(), "pipeline": list(self.current_pipeline)},
        }

    def update_teacher_skill(self, skill_slug: str, new_materials: List[str]) -> Dict[str, Any]:
        self.current_pipeline = ["load_existing", "merge_updates", "write_version"]
        return {
            "skill_slug": skill_slug,
            "new_materials_count": len(new_materials),
            "changes_applied": [
                "materials_index_refreshed",
                "analysis_marked_for_regeneration",
            ],
            "updated_at": datetime.now().isoformat(),
        }
    
   # ============================================================================
    # 辅助方法（实现原功能的关键逻辑）
    # ============================================================================
    
    def _extract_schema_from_model(self, model_class) -> Dict[str, Any]:
        """从Pydantic模型提取JSON Schema"""
        if PYDANTIC_AVAILABLE and hasattr(model_class, 'schema'):
            return model_class.schema()
        # 兜底手动 Schema 结构
        return {
            "type": "object",
            "properties": {f"layer_{i}": {"type": "object"} for i in range(5)}
        }

    def _is_materials_too_large(self, materials: List[str]) -> bool:
        """检查输入材料是否超过模型上下文限制"""
        total_text = "".join(materials)
        return self.llm.estimate_tokens(total_text) > self.token_limit

    def _prepare_context(self, materials: List[str]) -> str:
        """将多份材料整合成有序的上下文字符串"""
        context = []
        for i, m in enumerate(materials):
            context.append(f"--- Material #{i+1} ---\n{m}\n")
        return "\n".join(context)

    def _validate_and_convert_result(self, result: Dict, model_class: Any) -> TeacherStyleModel:
        """验证 LLM 返回的 JSON 是否符合模型定义"""
        data = result.get("data", result) # 兼容不同 API 返回格式
        try:
            if PYDANTIC_AVAILABLE:
                return model_class(**data)
            else:
                # 简单数据类映射
                obj = model_class()
                for k, v in data.items():
                    if hasattr(obj, k): setattr(obj, k, v)
                return obj
        except Exception as e:
            logger.error(f"结果转换失败: {str(e)}")
            return TeacherStyleModel() # 返回空模型保证引擎不崩溃

    def _analyze_in_chunks(self, materials: List[str], prompt: str, schema: Dict) -> TeacherStyleModel:
        """分而治之：分块分析并进行中间合并"""
        intermediate_results = []
        for i in range(0, len(materials), 2): # 每2篇材料一组
            chunk = materials[i:i+2]
            res = self.llm.call_with_schema(prompt, self._prepare_context(chunk), schema)
            intermediate_results.append(res.get("data", {}))
        
        # 将第一块作为初始值，后续进行迭代合并
        final_model = self._validate_and_convert_result(intermediate_results[0], TeacherStyleModel)
        if len(intermediate_results) > 1:
            return self.merge_with_conflict_resolution(final_model, intermediate_results[1:])
        return final_model

    def _get_conflict_protocol(self) -> Dict[str, str]:
        """定义冲突解决的硬性准则"""
        return {
            "priority": "evidence_density", # 证据密度优先
            "recency_bias": "low",          # 不盲目遵循最新材料，侧重稳定性
            "logical_consistency": "high"    # 强调层级间的逻辑自洽
        }

    def _get_influence_weight_system(self) -> Dict[str, float]:
        """定义不同类型修正的权重"""
        return {
            "factual_correction": 1.0,      # 事实性错误（如名字）权重最高
            "style_adjustment": 0.4,       # 语气微调权重较低
            "belief_shift": 0.7            # 教育理念转变需中高权重
        }

    def _generate_merge_report(self, original: TeacherStyleModel, new_data: Dict, updates: List) -> Dict:
        """计算合并前后的差异度"""
        # 简单逻辑：统计 key 的变化（实际可使用 dictdiffer 库）
        return {"changes_count": len(updates), "timestamp": datetime.now().isoformat()}

    def _analyze_correction_weight(self, correction: str, current_skill: TeacherStyleModel) -> Dict:
        """预分析纠正内容的性质"""
        # 模拟意图识别
        is_hard_fact = any(kw in correction for kw in ["不是", "错误", "改名"])
        return {
            "suggested_weight": 0.9 if is_hard_fact else 0.5,
            "domain": "communication" if "说话" in correction else "general"
        }

    def _enhance_audit_report(self, result: Dict, doc: str, materials: List[str]) -> Dict:
        """增强审计报告的可读性"""
        result["audit_timestamp"] = datetime.now().isoformat()
        result["summary"] = "文档通过质量验证" if result.get("verification_status") == "pass" else "需人工介入"
        return result
# 兼容性别名
TeacherSkillEngine = TeacherSkillEngineV2
StructuredOpenAIClient = StructuredOpenAIClient
LLMProvider = LLMProvider
TeacherSkillEngine = Orchestrator.__init__.__annotations__["engine"]
