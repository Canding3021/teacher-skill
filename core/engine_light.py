#!/usr/bin/env python3
"""
Lightweight teacher-skill engine.

This module keeps the original public API of the light engine while
providing a compact, syntax-safe implementation for local testing and
offline development.
"""

import json
import logging
import re
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, Dict, List


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


@dataclass
class TeacherStyleContract:
    layer_0: Dict[str, Any] = field(
        default_factory=lambda: {
            "core_beliefs": [],
            "non_negotiables": [],
            "value_hierarchy": {"primary": "", "secondary": "", "tertiary": ""},
        }
    )
    layer_1: Dict[str, Any] = field(
        default_factory=lambda: {
            "primary_role": "",
            "secondary_roles": [],
            "professional_identity": {"strength": "", "mission": "", "challenge": ""},
            "self_efficacy": {"confidence": 0.0, "growth_mindset": False, "adaptability": 0.0},
        }
    )
    layer_2: Dict[str, Any] = field(
        default_factory=lambda: {
            "verbal_habits": {"catchphrases": [], "high_frequency": [], "sentence_patterns": []},
            "communication_style": {"formality": 0.0, "directness": 0.0, "humor_level": 0.0, "warmth": 0.0},
            "feedback_patterns": {"praise": [], "correction": [], "encouragement": []},
        }
    )
    layer_3: Dict[str, Any] = field(
        default_factory=lambda: {
            "decision_making": {"primary_mode": "", "secondary_mode": "", "process": [], "criteria": [], "speed": ""},
            "problem_solving": {"approach": "", "steps": [], "resources": []},
            "time_management": {"planning": "", "prioritization": "", "delegation": ""},
        }
    )
    layer_4: Dict[str, Any] = field(
        default_factory=lambda: {
            "relationship_style": {"primary": "", "secondary": "", "distance": "", "boundaries": "", "trust_building": []},
            "emotional_support": {"availability": "", "approach": "", "methods": []},
            "conflict_management": {"prevention": [], "resolution": [], "learning": []},
        }
    )
    metadata: Dict[str, Any] = field(
        default_factory=lambda: {
            "consistency_score": 0.0,
            "authenticity_score": 0.0,
            "distinctiveness": 0.0,
            "evidence_count": 0,
            "confidence_level": "low",
        }
    )

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    def validate(self) -> List[str]:
        errors: List[str] = []
        if not self.layer_0["core_beliefs"]:
            errors.append("layer_0.core_beliefs cannot be empty")
        if not self.layer_1["primary_role"]:
            errors.append("layer_1.primary_role cannot be empty")
        for key in ["formality", "directness", "humor_level", "warmth"]:
            value = self.layer_2["communication_style"].get(key, 0.0)
            if not 0.0 <= value <= 1.0:
                errors.append(f"layer_2.communication_style.{key} must be between 0 and 1")
        return errors

    def to_json(self, indent: int = 2) -> str:
        return json.dumps(self.to_dict(), ensure_ascii=False, indent=indent)


class ConflictResolutionProtocol:
    @staticmethod
    def resolve_direct_contradiction(old: str, new: str) -> Dict[str, Any]:
        return {
            "strategy": "mark_as_evolution",
            "resolution": f"Earlier: {old}\nCurrent: {new}",
            "notes": "Treat the difference as a development over time.",
        }

    @staticmethod
    def resolve_contextual_difference(old: str, new: str, context_old: str, context_new: str) -> Dict[str, Any]:
        return {
            "strategy": "supplement_with_context",
            "resolution": f"{context_old}: {old}\n{context_new}: {new}",
            "notes": "The statements can coexist across different contexts.",
        }

    @staticmethod
    def resolve_developmental_change(old: str, new: str, timeline: Dict[str, str]) -> Dict[str, Any]:
        lines = [f"{time}: {description}" for time, description in timeline.items()]
        lines.extend([f"Earlier: {old}", f"Current: {new}"])
        return {
            "strategy": "create_timeline",
            "resolution": "\n".join(lines),
            "notes": "Track the change as a timeline rather than a contradiction.",
        }


class InfluenceWeightSystem:
    @staticmethod
    def analyze_correction(correction: str, current_skill: Dict[str, Any]) -> Dict[str, Any]:
        weight = 0.3
        if any(keyword in correction for keyword in ["不是", "不对", "错误"]):
            weight = 0.6
        if any(keyword in correction for keyword in ["根本不是", "完全错误"]):
            weight = 0.85
        if any(keyword in correction for keyword in ["还会", "另外", "补充"]):
            weight = min(weight, 0.25)

        confidence = 0.7
        if any(keyword in correction for keyword in ["例如", "比如", "原话"]):
            confidence = 0.9

        return {
            "influence_weight": weight,
            "confidence": confidence,
            "correction_type": "principle_refinement" if weight >= 0.6 else "style_adjustment",
        }


class DivideAndConquerStrategy:
    def __init__(self, chunk_size: int = 5000, overlap: int = 500):
        self.chunk_size = chunk_size
        self.overlap = overlap

    def split_text(self, text: str) -> List[str]:
        if len(text) <= self.chunk_size:
            return [text]

        chunks: List[str] = []
        start = 0
        while start < len(text):
            end = min(len(text), start + self.chunk_size)
            if end < len(text):
                sentence_break = max(text.rfind("。", start, end), text.rfind("\n", start, end))
                if sentence_break > start:
                    end = sentence_break + 1
            chunks.append(text[start:end])
            next_start = end - self.overlap
            start = next_start if next_start > start else end
        return chunks


class TeacherSkillEngineLight:
    """Compact implementation used for smoke tests and low-cost analysis."""

    def __init__(self, prompts_dir: str = "./prompts"):
        self.prompts_dir = Path(prompts_dir)
        self.conflict_resolver = ConflictResolutionProtocol()
        self.weight_system = InfluenceWeightSystem()
        self.divide_conquer = DivideAndConquerStrategy()

    def analyze_with_contract(self, materials_text: str) -> TeacherStyleContract:
        logger.info("Analyzing materials with lightweight contract engine")
        extracted = self._extract_key_information(materials_text)
        contract = TeacherStyleContract()
        for key, value in extracted.items():
            if hasattr(contract, key):
                setattr(contract, key, value)

        contract.metadata.update(
            {
                "consistency_score": 0.75,
                "authenticity_score": 0.7,
                "distinctiveness": 0.65,
                "evidence_count": max(1, len(re.findall(r"[。！？!?]", materials_text))),
                "confidence_level": "medium",
            }
        )
        return contract

    def merge_with_protocol(self, original: TeacherStyleContract, updates: List[Dict[str, Any]]) -> TeacherStyleContract:
        merged = TeacherStyleContract(**original.to_dict())
        for update in updates:
            for layer_name in ["layer_0", "layer_1", "layer_2", "layer_3", "layer_4", "metadata"]:
                payload = update.get(layer_name)
                if isinstance(payload, dict):
                    getattr(merged, layer_name).update(payload)
        merged.metadata["evidence_count"] = merged.metadata.get("evidence_count", 0) + len(updates)
        return merged

    def correct_with_weight(self, current: TeacherStyleContract, correction: str) -> Dict[str, Any]:
        analysis = self.weight_system.analyze_correction(correction, current.to_dict())
        return {
            "current_skill": current.to_dict(),
            "correction": correction,
            "analysis": analysis,
        }

    def audit_for_hallucinations(self, document: str, source_materials: List[str]) -> Dict[str, Any]:
        claims = [segment.strip() for segment in re.split(r"[。！？!?]", document) if segment.strip()]
        verified_claims: List[Dict[str, Any]] = []
        hallucinations: List[Dict[str, Any]] = []

        for claim in claims:
            matched = any(claim[:20].lower() in source.lower() for source in source_materials[:5])
            if matched:
                verified_claims.append({"claim": claim[:100], "evidence_count": 1, "confidence": "medium"})
            else:
                hallucinations.append({"claim": claim[:100], "type": "unsupported_inference", "severity": "minor"})

        total_claims = len(claims)
        hallucination_rate = len(hallucinations) / total_claims if total_claims else 0.0
        verification_status = "pass" if hallucination_rate < 0.1 else "conditional_pass" if hallucination_rate < 0.3 else "fail"

        return {
            "document_quality": {
                "total_claims": total_claims,
                "verified_claims": len(verified_claims),
                "hallucinations": len(hallucinations),
                "hallucination_rate": round(hallucination_rate, 3),
                "confidence_level": "high" if verification_status == "pass" else "medium" if verification_status == "conditional_pass" else "low",
            },
            "verification_status": verification_status,
            "sample_hallucinations": hallucinations[:3],
        }

    def _extract_key_information(self, text: str) -> Dict[str, Any]:
        core_beliefs: List[str] = []
        if "教育" in text and "学生" in text:
            core_beliefs.append("以学生为中心的教育")
        if "错误" in text and "学习" in text:
            core_beliefs.append("错误是学习的一部分")
        if not core_beliefs:
            core_beliefs.append("重视真实材料中的教学证据")

        catchphrases: List[str] = []
        if "思考" in text:
            catchphrases.append("我们先想一想")
        if "理解" in text:
            catchphrases.append("你理解了吗")

        return {
            "layer_0": {
                "core_beliefs": core_beliefs,
                "non_negotiables": ["不公开羞辱学生"],
                "value_hierarchy": {"primary": "学生成长", "secondary": "知识掌握", "tertiary": "成绩表现"},
            },
            "layer_1": {
                "primary_role": "学习引导者",
                "secondary_roles": ["知识传授者"],
                "professional_identity": {
                    "strength": "问题解决式教学",
                    "mission": "激发学习兴趣",
                    "challenge": "兼顾个体差异与整体节奏",
                },
                "self_efficacy": {"confidence": 0.8, "growth_mindset": True, "adaptability": 0.75},
            },
            "layer_2": {
                "verbal_habits": {
                    "catchphrases": catchphrases,
                    "high_frequency": ["思考", "理解", "方法"],
                    "sentence_patterns": ["先分析问题，再给方法"],
                },
                "communication_style": {"formality": 0.55, "directness": 0.7, "humor_level": 0.3, "warmth": 0.65},
                "feedback_patterns": {
                    "praise": ["这个思路对了"],
                    "correction": ["这里再想一步"],
                    "encouragement": ["继续往下推就会更清楚"],
                },
            },
            "layer_3": {
                "decision_making": {
                    "primary_mode": "evidence_based",
                    "secondary_mode": "experience_based",
                    "process": ["收集材料", "识别模式", "归纳教学风格"],
                    "criteria": ["一致性", "证据密度", "可执行性"],
                    "speed": "medium",
                },
                "problem_solving": {
                    "approach": "break_down_problem",
                    "steps": ["拆分问题", "确认证据", "形成结论"],
                    "resources": ["materials", "interviews", "classroom records"],
                },
                "time_management": {"planning": "weekly", "prioritization": "student_impact_first", "delegation": "selective"},
            },
            "layer_4": {
                "relationship_style": {
                    "primary": "supportive",
                    "secondary": "structured",
                    "distance": "professional",
                    "boundaries": "clear",
                    "trust_building": ["稳定反馈", "尊重事实", "持续跟进"],
                },
                "emotional_support": {
                    "availability": "moderate",
                    "approach": "calm_and_practical",
                    "methods": ["解释问题", "提供方法", "确认进展"],
                },
                "conflict_management": {
                    "prevention": ["预期对齐", "规则透明"],
                    "resolution": ["先厘清事实", "再处理分歧"],
                    "learning": ["复盘沟通方式"],
                },
            },
        }

