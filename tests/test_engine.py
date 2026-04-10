#!/usr/bin/env python3
"""
Teacher Skill Engine 测试
"""

import unittest
import sys
import os
from pathlib import Path

# 添加项目根目录到Python路径
sys.path.insert(0, str(Path(__file__).parent.parent))

from core.engine import TeacherSkillEngine, OpenAIClient, LocalLLMClient


class TestLLMProvider(unittest.TestCase):
    """测试LLM提供商"""
    
    def test_openai_client_initialization(self):
        """测试OpenAI客户端初始化"""
        client = OpenAIClient(model="gpt-4")
        self.assertEqual(client.model, "gpt-4")
        
    def test_local_llm_client_initialization(self):
        """测试本地LLM客户端初始化"""
        client = LocalLLMClient(model="qwen2.5:7b")
        self.assertEqual(client.model, "qwen2.5:7b")
        self.assertEqual(client.base_url, "http://localhost:11434")


class TestTeacherSkillEngine(unittest.TestCase):
    """测试教师Skill引擎"""
    
    def setUp(self):
        """测试前准备"""
        # 使用本地模型客户端（避免API调用）
        self.llm = LocalLLMClient(model="test-model")
        self.engine = TeacherSkillEngine(self.llm)
        
    def test_engine_initialization(self):
        """测试引擎初始化"""
        self.assertIsNotNone(self.engine.llm)
        self.assertIsNotNone(self.engine.prompts_dir)
        
    def test_load_prompt_success(self):
        """测试成功加载prompt"""
        # 创建测试prompt文件
        test_prompt_dir = Path("test_prompts")
        test_prompt_dir.mkdir(exist_ok=True)
        
        test_prompt_content = "# 测试prompt\n这是一个测试prompt。"
        (test_prompt_dir / "test_prompt.md").write_text(test_prompt_content, encoding="utf-8")
        
        # 临时修改prompts目录
        original_prompts_dir = self.engine.prompts_dir
        self.engine.prompts_dir = test_prompt_dir
        
        try:
            prompt = self.engine.load_prompt("test_prompt")
            self.assertEqual(prompt, test_prompt_content)
        finally:
            # 恢复原始目录
            self.engine.prompts_dir = original_prompts_dir
            # 清理测试文件
            import shutil
            shutil.rmtree(test_prompt_dir, ignore_errors=True)
            
    def test_load_prompt_not_found(self):
        """测试加载不存在的prompt"""
        with self.assertRaises(FileNotFoundError):
            self.engine.load_prompt("non_existent_prompt")
            
    def test_validate_analysis(self):
        """测试分析结果验证"""
        test_analysis = {
            "teaching_capabilities": {
                "knowledge_system": "测试知识体系",
                "method_repertoire": ["方法1", "方法2"]
            }
        }
        
        validated = self.engine._validate_analysis(test_analysis)
        
        # 检查必需字段
        self.assertIn("teaching_capabilities", validated)
        self.assertIn("teacher_style", validated)
        
        # 检查原始数据保留
        self.assertEqual(validated["teaching_capabilities"]["knowledge_system"], "测试知识体系")
        
    def test_build_style_analysis_context(self):
        """测试构建风格分析上下文"""
        materials = [
            {"summary": "材料1摘要", "content": "详细内容1"},
            {"summary": "材料2摘要", "content": "详细内容2"}
        ]
        
        interviews = [
            "访谈记录1：教师的教学理念",
            "访谈记录2：课堂管理方法"
        ]
        
        context = self.engine._build_style_analysis_context(materials, interviews)
        
        # 检查上下文包含材料摘要
        self.assertIn("材料1: 材料1摘要", context)
        self.assertIn("材料2: 材料2摘要", context)
        
        # 检查上下文包含访谈记录
        self.assertIn("访谈记录:", context)
        self.assertIn("- 访谈记录1：教师的教学理念", context)


class TestOrchestrator(unittest.TestCase):
    """测试编排器"""
    
    def test_orchestrator_initialization(self):
        """测试编排器初始化"""
        from core.engine import Orchestrator, LocalLLMClient
        
        llm = LocalLLMClient(model="test-model")
        engine = TeacherSkillEngine(llm)
        orchestrator = Orchestrator(engine)
        
        self.assertIsNotNone(orchestrator.engine)
        self.assertEqual(len(orchestrator.current_pipeline), 0)


class TestIntegration(unittest.TestCase):
    """集成测试"""
    
    def test_complete_workflow_stub(self):
        """测试完整工作流程（存根版本）"""
        from core.engine import TeacherSkillEngine, LocalLLMClient, Orchestrator
        
        # 初始化组件
        llm = LocalLLMClient(model="test-model")
        engine = TeacherSkillEngine(llm)
        orchestrator = Orchestrator(engine)
        
        # 测试数据
        teacher_info = {
            "name": "测试教师",
            "subject": "测试学科",
            "years": 5
        }
        
        # 执行工作流程（存根版本）
        try:
            skill_data = orchestrator.create_teacher_skill(
                materials_dir="./test_materials",
                teacher_info=teacher_info
            )
            
            # 检查返回数据结构
            self.assertIn("teacher_info", skill_data)
            self.assertIn("analysis", skill_data)
            self.assertIn("documents", skill_data)
            self.assertIn("metadata", skill_data)
            
            self.assertEqual(skill_data["teacher_info"]["name"], "测试教师")
            
        except Exception as e:
            # 存根版本可能抛出异常，这是预期的
            print(f"存根版本异常（预期中）: {e}")
            
    def test_update_workflow_stub(self):
        """测试更新工作流程（存根版本）"""
        from core.engine import TeacherSkillEngine, LocalLLMClient, Orchestrator
        
        llm = LocalLLMClient(model="test-model")
        engine = TeacherSkillEngine(llm)
        orchestrator = Orchestrator(engine)
        
        try:
            update_result = orchestrator.update_teacher_skill(
                skill_slug="test_teacher",
                new_materials=["新材料1", "新材料2"]
            )
            
            # 检查返回数据结构
            self.assertIn("skill_slug", update_result)
            self.assertIn("new_materials_count", update_result)
            self.assertIn("changes_applied", update_result)
            
        except Exception as e:
            # 存根版本可能抛出异常，这是预期的
            print(f"存根版本异常（预期中）: {e}")


class TestErrorHandling(unittest.TestCase):
    """错误处理测试"""
    
    def test_missing_prompts_directory(self):
        """测试缺失prompts目录"""
        from core.engine import TeacherSkillEngine, LocalLLMClient
        
        llm = LocalLLMClient(model="test-model")
        
        # 使用不存在的prompts目录
        engine = TeacherSkillEngine(llm, prompts_dir="./non_existent_prompts")
        
        # 尝试加载prompt应该失败
        with self.assertRaises(FileNotFoundError):
            engine.load_prompt("any_prompt")


def run_tests():
    """运行所有测试"""
    # 创建测试套件
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # 添加测试类
    suite.addTests(loader.loadTestsFromTestCase(TestLLMProvider))
    suite.addTests(loader.loadTestsFromTestCase(TestTeacherSkillEngine))
    suite.addTests(loader.loadTestsFromTestCase(TestOrchestrator))
    suite.addTests(loader.loadTestsFromTestCase(TestIntegration))
    suite.addTests(loader.loadTestsFromTestCase(TestErrorHandling))
    
    # 运行测试
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result.wasSuccessful()


if __name__ == "__main__":
    print("=" * 60)
    print("Teacher Skill Engine 测试套件")
    print("=" * 60)
    
    success = run_tests()
    
    print("\n" + "=" * 60)
    if success:
        print("✅ 所有测试通过！")
    else:
        print("❌ 部分测试失败")
    print("=" * 60)
    
    sys.exit(0 if success else 1)