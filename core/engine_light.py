#!/usr/bin/env python3
"""
Teacher Skill Engine - 轻量级重构版

专注于解决核心问题：
1. 结构化契约输出
2. 冲突解决协议
3. 影响权重系统
4. 分而治之策略
"""

import json
import logging
import re
from pathlib import Path
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field, asdict

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


# ============================================================================
# 结构化契约：数据类版本（轻量级）
# ============================================================================

@dataclass
class TeacherStyleContract:
    """教师风格结构化契约 - 轻量级版本"""
    
    # Layer 0: 教育理念
    layer_0: Dict[str, Any] = field(default_factory=lambda: {
        "core_beliefs": [],
        "non_negotiables": [],
        "value_hierarchy": {"primary": "", "secondary": "", "tertiary": ""}
    })
    
    # Layer 1: 教师身份
    layer_1: Dict[str, Any] = field(default_factory=lambda: {
        "primary_role": "",
        "secondary_roles": [],
        "professional_identity": {"strength": "", "mission": "", "challenge": ""},
        "self_efficacy": {"confidence": 0.0, "growth_mindset": False, "adaptability": 0.0}
    })
    
    # Layer 2: 沟通风格
    layer_2: Dict[str, Any] = field(default_factory=lambda: {
        "verbal_habits": {"catchphrases": [], "high_frequency": [], "sentence_patterns": []},
        "communication_style": {"formality": 0.0, "directness": 0.0, "humor_level": 0.0, "warmth": 0.0},
        "feedback_patterns": {"praise": [], "correction": [], "encouragement": []}
    })
    
    # Layer 3: 课堂决策
    layer_3: Dict[str, Any] = field(default_factory=lambda: {
        "decision_making": {"primary_mode": "", "secondary_mode": "", "process": [], "criteria": [], "speed": ""},
        "problem_solving": {"approach": "", "steps": [], "resources": []},
        "time_management": {"planning": "", "prioritization": "", "delegation": ""}
    })
    
    # Layer 4: 师生关系
    layer_4: Dict[str, Any] = field(default_factory=lambda: {
        "relationship_style": {"primary": "", "secondary": "", "distance": "", "boundaries": "", "trust_building": []},
        "emotional_support": {"availability": "", "approach": "", "methods": []},
        "conflict_management": {"prevention": [], "resolution": [], "learning": []}
    })
    
    # 元数据
    metadata: Dict[str, Any] = field(default_factory=lambda: {
        "consistency_score": 0.0,
        "authenticity_score": 0.0,
        "distinctiveness": 0.0,
        "evidence_count": 0,
        "confidence_level": "low"
    })
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return asdict(self)
    
    def validate(self) -> List[str]:
        """简单验证"""
        errors = []
        
        # 检查必填字段
        if not self.layer_0["core_beliefs"]:
            errors.append("layer_0.core_beliefs不能为空")
        
        if not self.layer_1["primary_role"]:
            errors.append("layer_1.primary_role不能为空")
        
        # 检查数值范围
        for key in ["formality", "directness", "humor_level", "warmth"]:
            value = self.layer_2["communication_style"].get(key, 0.0)
            if not 0.0 <= value <= 1.0:
                errors.append(f"layer_2.communication_style.{key}必须在0-1之间")
        
        return errors
    
    def to_json(self, indent: int = 2) -> str:
        """转换为JSON字符串"""
        return json.dumps(self.to_dict(), ensure_ascii=False, indent=indent)


# ============================================================================
# 冲突解决协议
# ============================================================================

class ConflictResolutionProtocol:
    """冲突解决协议 - 轻量级实现"""
    
    @staticmethod
    def resolve_direct_contradiction(old: str, new: str) -> Dict[str, Any]:
        """解决直接矛盾"""
        return {
            "strategy": "mark_as_evolution",
            "resolution": f"早期：{old}\n当前：{new}",
            "notes": "识别为发展阶段变化"
        }
    
    @staticmethod
    def resolve_contextual_difference(old: str, new: str, context_old: str, context_new: str) -> Dict[str, Any]:
        """解决情境差异"""
        return {
            "strategy": "supplement_with_context",
            "resolution": f"{context_old}情境：{old}\n{context_new}情境：{new}",
            "notes": "识别为情境差异"
        }
    
    @staticmethod
    def resolve_developmental_change(old: str, new: str, timeline: Dict[str, str]) -> Dict[str, Any]:
        """解决发展阶段变化"""
        return {
            "strategy": "create_timeline",
            "resolution": "\n".join([f"{time}: {desc}" for time, desc in timeline.items()]),
            "notes": "识别为发展阶段演进"
        }


# ============================================================================
# 影响权重系统
# ============================================================================

class InfluenceWeightSystem:
    """影响权重系统 - 避免过度修正"""
    
    @staticmethod
    def analyze_correction(correction: str, current_skill: Dict[str, Any]) -> Dict[str, Any]:
        """分析纠正意图和权重"""
        
        # 简单关键词分析
        weight = 0.3  # 默认低权重
        
        if "不会" in correction or "不对" in correction:
            weight = 0.5  # 中等权重：行为修正
        
        if "根本不是" in correction or "完全错误" in correction:
            weight = 0.8  # 高权重：原则修正
        
        if "还会" in correction or "另外" in correction:
            weight = 0.2  # 低权重：补充说明
        
        # 置信度评估
        confidence = 0.7  # 默认中等置信度
        if "例如" in correction or "比如" in correction:
            confidence = 0.9  # 高置信度：有具体例子
        
        return {
            "influence_weight": weight,
            "confidence": confidence,
            "correction_type": "style_adjustment" if weight < 0.6 else "principle_refinement"
        }


# ============================================================================
# 分而治之策略
# ============================================================================

class DivideAndConquerStrategy:
    """分而治之策略 - 处理大文本"""
    
    def __init__(self, chunk_size: int = 5000, overlap: int = 500):
        self.chunk_size = chunk_size
        self.overlap = overlap
    
    def split_text(self, text: str) -> List[str]:
        """分割文本为块"""
        chunks = []
        start = 0
        
        while start < len(text):
            end = start + self.chunk_size
            
            # 尝试在句子边界分割
            if end < len(text):
                # 找最近的句号
                sentence_end = text.rfind('。', start, end)
                if sentence_end != -1:
                    end = sentence_end + 1  # 包括句号
            
            chunk = text[start:end]
            chunks.append(chunk)
            
            # 移动起始位置，考虑重叠
            start = end - self.overlap if end - self.overlap > start else end
        
        return chunks


# ============================================================================
# 核心引擎：轻量级重构
# ============================================================================

class TeacherSkillEngineLight:
    """
    教师Skill引擎 - 轻量级重构版
    
    专注于解决核心工程问题，保持简单可维护
    """
    
    def __init__(self, prompts_dir: str = "./prompts"):
        self.prompts_dir = Path(prompts_dir)
        self.conflict_resolver = ConflictResolutionProtocol()
        self.weight_system = InfluenceWeightSystem()
        self.divide_conquer = DivideAndConquerStrategy()
        
    def analyze_with_contract(self, materials_text: str) -> TeacherStyleContract:
        """
        使用结构化契约分析
        
        关键改进：强制结构化输出，避免散文式描述
        """
        logger.info("开始结构化契约分析...")
        
        # 1. 分而治之：如果文本太大
        if len(materials_text) > 10000:  # 简单长度检查
            logger.info("文本过大，启用分而治之策略...")
            chunks = self.divide_conquer.split_text(materials_text)
            logger.info(f"分割为{len(chunks)}个块")
            # 这里实际应该对每个块进行分析然后合并
            # 为简化演示，只分析第一个块
        
        # 2. 提取关键信息（模拟LLM分析）
        analysis_result = self._extract_key_information(materials_text[:5000])
        
        # 3. 转换为结构化契约
        contract = TeacherStyleContract(**analysis_result)
        
        # 4. 验证结果
        errors = contract.validate()
        if errors:
            logger.warning(f"分析结果验证警告: {errors}")
        
        logger.info(f"分析完成: {contract.metadata['evidence_count']}个证据")
        return contract
    
    def merge_with_protocol(self, original: TeacherStyleContract, updates: List[Dict]) -> TeacherStyleContract:
        """
        使用冲突解决协议合并
        
        关键改进：智能解决冲突，避免精神分裂
        """
        logger.info("开始冲突解决协议合并...")
        
        # 1. 转换为字典以便操作
        merged_dict = original.to_dict()
        
        # 2. 记录冲突解决
        conflict_resolutions = []
        
        # 3. 应用更新，检测冲突
        for update in updates:
            for layer_key, layer_update in update.items():
                if layer_key in merged_dict:
                    # 检查每个字段的更新
                    for field_key, field_update in layer_update.items():
                        if isinstance(field_update, dict):
                            # 字典字段：深度合并
                            for sub_key, sub_update in field_update.items():
                                current_value = merged_dict[layer_key].get(field_key, {}).get(sub_key)
                                if current_value and current_value != sub_update:
                                    # 检测到冲突
                                    resolution = self.conflict_resolver.resolve_direct_contradiction(
                                        str(current_value),
                                        str(sub_update)
                                    )
                                    conflict_resolutions.append({
                                        "layer": layer_key,
                                        "field": f"{field_key}.{sub_key}",
                                        "resolution": resolution
                                    })
                                    logger.info(f"解决冲突: {layer_key}.{field_key}.{sub_key}")
                        
                        # 应用更新（简单策略：以新数据为主）
                        if isinstance(merged_dict[layer_key], dict):
                            if isinstance(field_update, dict):
                                # 深度合并字典
                                merged_dict[layer_key].setdefault(field_key, {}).update(field_update)
                            else:
                                # 直接替换
                                merged_dict[layer_key][field_key] = field_update
        
        # 4. 更新元数据
        merged_dict["metadata"]["conflict_resolutions"] = conflict_resolutions
        merged_dict["metadata"]["merge_strategy"] = "conflict_resolution_protocol"
        merged_dict["metadata"]["merge_timestamp"] = "2026-04-10T13:30:00Z"
        
        merged_contract = TeacherStyleContract(**merged_dict)
        logger.info(f"合并完成: {len(conflict_resolutions)}个冲突已解决")
        return merged_contract
    
    def correct_with_weight(self, current: TeacherStyleContract, correction: str) -> Dict[str, Any]:
        """
        使用影响权重系统处理纠正
        
        关键改进：避免过度修正
        """
        logger.info("开始权重化纠正处理...")
        
        # 1. 分析纠正权重
        weight_analysis = self.weight_system.analyze_correction(correction, current.to_dict())
        
        # 2. 根据权重选择策略
        weight = weight_analysis["influence_weight"]
        
        if weight < 0.3:
            strategy = "minimal_adjustment"
            changes = [{"type": "minor", "description": "语言微调", "impact": "low"}]
        elif weight < 0.6:
            strategy = "moderate_adjustment"
            changes = [{"type": "moderate", "description": "行为模式调整", "impact": "medium"}]
        else:
            strategy = "significant_restructuring"
            changes = [{"type": "major", "description": "核心理念修正", "impact": "high"}]
        
        # 3. 识别未修改的部分（保持原样）
        unchanged_sections = []
        contract_dict = current.to_dict()
        for layer in ["layer_0", "layer_1", "layer_2", "layer_3", "layer_4"]:
            if layer in contract_dict:
                unchanged_sections.append(layer)
        
        # 4. 生成纠正报告
        report = {
            "correction_analysis": weight_analysis,
            "applied_strategy": strategy,
            "changes": changes,
            "unchanged_sections": unchanged_sections,
            "confidence": weight_analysis["confidence"],
            "recommendation": self._get_correction_recommendation(weight)
        }
        
        logger.info(f"纠正完成: 权重={weight}, 策略={strategy}")
        return report
    
    def audit_for_hallucinations(self, document: str, source_materials: List[str]) -> Dict[str, Any]:
        """
        审计文档中的幻觉
        
        关键改进：检测无证据支持的内容
        """
        logger.info("开始幻觉审计...")
        
        # 1. 提取文档中的所有声称（简单实现）
        claims = self._extract_claims_simple(document)
        
        # 2. 验证每个声称的证据支持
        verified_claims = []
        hallucinations = []
        
        for claim in claims:
            # 简单验证：检查是否在源材料中提到
            evidence_found = False
            for material in source_materials[:3]:  # 只检查前3个材料
                if claim.lower() in material.lower():
                    evidence_found = True
                    break
            
            if evidence_found:
                verified_claims.append({
                    "claim": claim[:100],  # 截断
                    "evidence_count": 1,
                    "confidence": "medium"
                })
            else:
                # 分类幻觉类型
                hallucination_type = "unsupported_inference"
                if "总是" in claim or "从不" in claim:
                    hallucination_type = "overgeneralization"
                elif "优秀" in claim or "完美" in claim:
                    hallucination_type = "subjective_addition"
                
                hallucinations.append({
                    "claim": claim[:100],
                    "type": hallucination_type,
                    "severity": "minor" if len(claim) < 50 else "major"
                })
        
        # 3. 计算质量指标
        total_claims = len(claims)
        hallucination_rate = len(hallucinations) / total_claims if total_claims > 0 else 0
        
        audit_report = {
            "document_quality": {
                "total_claims": total_claims,
                "verified_claims": len(verified_claims),
                "hallucinations": len(hallucinations),
                "hallucination_rate": round(hallucination_rate, 3),
                "confidence_level": "high" if hallucination_rate < 0.1 else "medium" if hallucination_rate < 0.3 else "low"
            },
            "verification_status": "pass" if hallucination_rate < 0.1 else "conditional_pass" if hallucination_rate < 0.3 else "fail",
            "sample_hallucinations": hallucinations[:3] if hallucinations else []
        }
        
        logger.info(f"审计完成: {len(hallucinations)}个幻觉, 通过率={1-hallucination_rate:.1%}")
        return audit_report
    
    # ============================================================================
    # 辅助方法
    # ============================================================================
    
    def _extract_key_information(self, text: str) -> Dict[str, Any]:
        """从文本中提取关键信息（模拟LLM分析）"""
        # 这是一个简化的模拟实现
        # 实际应该调用真正的LLM
        
        # 提取核心信念
        core_beliefs = []
        if "教育" in text and "学生" in text:
            core_beliefs.append("以学生为中心的教育")
        if "错误" in text and "学习" in text:
            core_beliefs.append("错误是学习的机会")
        
        # 提取口头禅
        catchphrases = []
        if "思考" in text:
            catchphrases.append("我们来思考一下")
        if "理解" in text:
            catchphrases.append("理解了吗")
        
        return {
            "layer_0": {
                "core_beliefs": core_beliefs,
                "non_negotiables": ["绝不公开批评学生"],
                "value_hierarchy": {"primary": "学生成长", "secondary": "知识掌握", "tertiary": "考试成绩"}
            },
            "layer_1": {
                "primary_role": "学习引导者",
                "secondary_roles": ["知识传授者"],
                "professional_identity": {
                    "strength": "问题解决教学",
                    "mission": "激发学习兴趣", 
                    "challenge": "平衡个性与统一"
