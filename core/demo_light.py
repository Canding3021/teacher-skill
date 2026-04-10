#!/usr/bin/env python3
"""
Runnable demo for the lightweight teacher-skill engine.
"""

import json
import sys

from engine_light import TeacherSkillEngineLight


def _ensure_utf8_stdout() -> None:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")


def demo_structured_contract(engine: TeacherSkillEngineLight):
    print("=" * 60)
    print("Demo 1: Structured Contract Output")
    print("=" * 60)

    materials = """
    张老师的教学反思：
    我始终相信教育是唤醒，不是灌输。每个学生都有闪光点，只是需要时间发现。
    在课堂上，我经常说“我们来思考一下”，鼓励学生自己探索答案。
    我从不公开批评学生，错误是学习的最好机会。
    作业我会当天批改，及时反馈很重要。
    学生说我的课很有趣，因为我经常用生活中的例子讲解数学。
    """

    contract = engine.analyze_with_contract(materials)
    print(json.dumps(contract.to_dict(), ensure_ascii=False, indent=2)[:800] + "...")

    errors = contract.validate()
    if errors:
        print("Validation warnings:", errors)
    else:
        print("Validation passed")
    return contract


def demo_conflict_resolution(engine: TeacherSkillEngineLight, contract):
    print("\n" + "=" * 60)
    print("Demo 2: Conflict Resolution")
    print("=" * 60)

    updates = [
        {
            "layer_0": {
                "core_beliefs": ["教育是合作，不是单向传授"],
                "non_negotiables": ["作业必须隔天批改"],
            },
            "layer_2": {
                "verbal_habits": {"catchphrases": ["大家动动脑子"]},
            },
        }
    ]

    merged = engine.merge_with_protocol(contract, updates)
    print("merge_strategy:", merged.metadata.get("merge_strategy"))
    print("conflict_resolutions:", len(merged.metadata.get("conflict_resolutions", [])))
    return merged


def demo_influence_weight_system(engine: TeacherSkillEngineLight, contract):
    print("\n" + "=" * 60)
    print("Demo 3: Influence Weight System")
    print("=" * 60)

    corrections = [
        "他不会说‘我们来思考一下’，他通常说‘大家动动脑子’",
        "他不会公开批评学生，但会在私下严谨指出问题",
        "他根本不是‘以学生为中心’，他更偏知识本位",
    ]

    for correction in corrections:
        report = engine.correct_with_weight(contract, correction)
        analysis = report["correction_analysis"]
        print(
            json.dumps(
                {
                    "correction": correction,
                    "influence_weight": analysis["influence_weight"],
                    "correction_type": analysis["correction_type"],
                    "applied_strategy": report["applied_strategy"],
                    "confidence": report["confidence"],
                    "recommendation": report["recommendation"],
                },
                ensure_ascii=False,
                indent=2,
            )
        )


def demo_hallucination_audit(engine: TeacherSkillEngineLight):
    print("\n" + "=" * 60)
    print("Demo 4: Hallucination Audit")
    print("=" * 60)

    generated_document = """
    张老师是一位非常优秀的数学老师，学生都很喜欢他。
    他经常用生活中的例子讲解数学，作业当天批改。
    他每天都工作到很晚，总是第一个到校。
    """

    source_materials = [
        "张老师教数学，学生说他的课很有趣。",
        "张老师用生活中的例子讲解数学。",
        "张老师当天批改作业。",
    ]

    audit_report = engine.audit_for_hallucinations(generated_document, source_materials)
    print(json.dumps(audit_report, ensure_ascii=False, indent=2))


def main() -> int:
    _ensure_utf8_stdout()
    print("Teacher Skill Engine Lightweight Demo")
    print("Focused on structure, merge safety, correction weighting, and auditing")

    engine = TeacherSkillEngineLight()
    contract = demo_structured_contract(engine)
    merged = demo_conflict_resolution(engine, contract)
    demo_influence_weight_system(engine, merged)
    demo_hallucination_audit(engine)

    print("\nDemo completed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
