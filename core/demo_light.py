#!/usr/bin/env python3
"""
Teacher Skill Engine 轻量级重构演示

展示核心改进：
1. 结构化契约输出（解决散文式问题）
2. 冲突解决协议（解决精神分裂问题）
3. 影响权重系统（避免过度修正）
4. 幻觉审计（保证质量）
"""

import json
from engine_light import TeacherSkillEngineLight, TeacherStyleContract

def demo_structured_contract():
    """演示结构化契约输出"""
    print("=" * 60)
    print("演示1: 结构化契约输出")
    print("=" * 60)
    
    # 创建引擎
    engine = TeacherSkillEngineLight()
    
    # 模拟教学材料
    materials = """
    张老师的教学反思：
    我始终相信教育是唤醒，不是灌输。每个学生都有闪光点，只是需要时间发现。
    在课堂上，我经常说"我们来思考一下"，鼓励学生自己探索答案。
    我从不公开批评学生，错误是学习的最好机会。
    作业我会当天批改，及时反馈很重要。
    学生说我的课很有趣，因为我经常用生活中的例子讲解数学。
    """
    
    print("📚 输入材料:")
    print(materials[:200] + "...")
    print()
    
    # 分析并生成结构化契约
    contract = engine.analyze_with_contract(materials)
    
    print("✅ 结构化契约输出:")
    print(json.dumps(contract.to_dict(), ensure_ascii=False, indent=2)[:500] + "...")
    print()
    
    # 验证契约
    errors = contract.validate()
    if errors:
        print("⚠️  验证警告:", errors)
    else:
        print("✅ 契约验证通过")
    
    return contract

def demo_conflict_resolution(original_contract):
    """演示冲突解决协议"""
    print("\n" + "=" * 60)
    print("演示2: 冲突解决协议")
    print("=" * 60)
    
    engine = TeacherSkillEngineLight()
    
    # 模拟更新数据（包含冲突）
    updates = [
        {
            "layer_0": {
                "core_beliefs": ["教育是合作，不是单向传授"],  # 与原始"教育是唤醒"有差异
                "non_negotiables": ["作业必须隔天批改"]  # 与原始"当天批改"冲突
            },
            "layer_2": {
                "verbal_habits": {
                    "catchphrases": ["大家动动脑子"]  # 新口头禅
                }
            }
        }
    ]
    
    print("🔄 更新数据（包含冲突）:")
    print(json.dumps(updates, ensure_ascii=False, indent=2))
    print()
    
    # 使用冲突解决协议合并
    merged = engine.merge_with_protocol(original_contract, updates)
    
    print("✅ 合并结果（应用冲突解决协议）:")
    print(f"冲突解决记录: {len(merged.metadata.get('conflict_resolutions', []))}个")
    print(f"合并策略: {merged.metadata.get('merge_strategy', 'unknown')}")
    print()
    
    # 显示解决的具体冲突
    if "conflict_resolutions" in merged.metadata:
        print("🔧 解决的冲突:")
        for i, resolution in enumerate(merged.metadata["conflict_resolutions"][:2], 1):
            print(f"  {i}. {resolution.get('field', 'unknown')}")
            print(f"     策略: {resolution.get('resolution', {}).get('strategy', 'unknown')}")
    
    return merged

def demo_influence_weight_system(current_contract):
    """演示影响权重系统"""
    print("\n" + "=" * 60)
    print("演示3: 影响权重系统")
    print("=" * 60)
    
    engine = TeacherSkillEngineLight()
    
    # 不同权重的纠正示例
    corrections = [
        ("他不会说'我们来思考一下'，他通常说'大家动动脑子'", "低权重纠正"),
        ("他不会公开批评学生，但会在私下严肃指出问题", "中权重纠正"),
        ("他根本不是'以学生为中心'，他是典型的'知识本位'", "高权重纠正")
    ]
    
    for correction, description in corrections:
        print(f"\n📝 {description}:")
        print(f"   用户反馈: {correction}")
        
        # 分析纠正权重
        report = engine.correct_with_weight(current_contract, correction)
        
        print(f"   分析结果:")
        print(f"     - 影响权重: {report['correction_analysis']['influence_weight']:.2f}")
        print(f"     - 纠正类型: {report['correction_analysis']['correction_type']}")
        print(f"     - 应用策略: {report['applied_strategy']}")
        print(f"     - 置信度: {report['confidence']:.2f}")
        print(f"     - 推荐: {report.get('recommendation', 'N/A')}")

def demo_hallucination_audit():
    """演示幻觉审计"""
    print("\n" + "=" * 60)
    print("演示4: 幻觉审计")
    print("=" * 60)
    
    engine = TeacherSkillEngineLight()
    
    # 模拟生成的文档（包含一些幻觉）
    generated_document = """
    张老师是一位非常优秀的数学教师，他总是很有耐心。
    他的教学方法非常先进，总是使用最新的教育技术。
    学生们都非常喜欢他，认为他是最好的老师。
    他每天工作到很晚，总是第一个到学校。
    他的课堂气氛总是很活跃，学生从不走神。
    """
    
    # 源材料（有限的证据）
    source_materials = [
        "张老师教数学，学生说他的课有趣。",
        "张老师用生活中的例子讲解数学。",
        "张老师当天批改作业。"
    ]
    
    print("📄 生成的文档:")
    print(generated_document)
    print()
    
    print("📚 源材料:")
    for i, material in enumerate(source_materials, 1):
        print(f"  {i}. {material}")
    print()
    
    # 执行审计
    audit_report = engine.audit_for_hallucinations(generated_document, source_materials)
    
    print("🔍 审计结果:")
    print(f"  总声称数: {audit_report['document_quality']['total_claims']}")
    print(f"  已验证声称: {audit_report['document_quality']['verified_claims']}")
    print(f"  幻觉数量: {audit_report['document_quality']['hallucinations']}")
    print(f"  幻觉率: {audit_report['document_quality']['hallucination_rate']:.1%}")
    print(f"  置信度: {audit_report['document_quality']['confidence_level']}")
    print(f"  验证状态: {audit_report['verification_status']}")
    
    if audit_report.get('sample_hallucinations'):
        print("\n⚠️  示例幻觉:")
        for i, hallucination in enumerate(audit_report['sample_hallucinations'], 1):
            print(f"  {i}. '{hallucination['claim']}'")
            print(f"     类型: {hallucination['type']}, 严重性: {hallucination['severity']}")

def demo_architecture_benefits():
    """演示架构优势"""
    print("\n" + "=" * 60)
    print("架构优势总结")
    print("=" * 60)
    
    benefits = [
        {
            "问题": "散文式Prompt输出",
            "旧方案": "自由文本描述，格式不一致",
            "新方案": "结构化契约（JSON Schema）",
            "优势": "强制一致格式，便于程序处理"
        },
        {
            "问题": "合并导致精神分裂",
            "旧方案": "简单文本拼接",
            "新方案": "冲突解决协议",
            "优势": "智能解决冲突，保持一致性"
        },
        {
            "问题": "过度修正",
            "旧方案": "用户说什么就改什么",
            "新方案": "影响权重系统",
            "优势": "适度调整，避免推倒重来"
        },
        {
            "问题": "幻觉内容",
            "旧方案": "无验证，可能编造",
            "新方案": "幻觉审计",
            "优势": "检测无证据支持的内容"
        },
        {
            "问题": "大文本处理",
            "旧方案": "一次性处理，可能超限",
            "新方案": "分而治之策略",
            "优势": "分批处理，支持大文本"
        }
    ]
    
    print("🏗️  重构后的架构优势:")
    for i, benefit in enumerate(benefits, 1):
        print(f"\n{i}. {benefit['问题']}")
        print(f"   ❌ 旧: {benefit['旧方案']}")
        print(f"   ✅ 新: {benefit['新方案']}")
        print(f"   🎯 优势: {benefit['优势']}")

def main():
    """主演示函数"""
    print("🎯 Teacher Skill Engine 轻量级重构演示")
    print("专注于解决核心工程问题")
    print()
    
    try:
        # 演示1: 结构化契约
        contract = demo_structured_contract()
        
        # 演示2: 冲突解决
        merged_contract = demo_conflict_resolution(contract)
        
        # 演示3: 影响权重
        demo_influence_weight_system(merged_contract)
        
        # 演示4: 幻觉审计
        demo_hallucination_audit()
        
        # 架构优势总结
        demo_architecture_benefits()
        
        print("\n" + "=" * 60)
        print("✅ 演示完成!")
        print("=" * 60)
        print("\n关键改进已实现:")
        print("1. 📝 结构化契约 → 解决散文式输出问题")
        print("2. 🔄 冲突解决协议 → 解决精神分裂问题")
        print("3. ⚖️  影响权重系统 → 避免过度修正")
        print("4. 🔍 幻觉审计 → 保证内容真实性")
        print("5. 🧩 分而治之 → 支持大文本处理")
        
    except Exception as e:
        print(f"\n❌ 演示出错: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()