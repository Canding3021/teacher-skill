# Teacher.skill - AI教师技能蒸馏框架

<div align="center">

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.9+-green.svg)
![AI](https://img.shields.io/badge/AI-Agent%20Framework-orange.svg)

**将优秀教师的教学智慧转化为可传承的AI Skill**

[English](./README_EN.md) | 中文

</div>

## 🎯 项目简介

Teacher.skill 是一个端到端的 **AI Agent 框架**，专门用于蒸馏优秀教师的教学能力、人格特征和学科知识，生成结构化的 AI 教师技能文件。

> **这不是一个传统的Python脚本项目，而是一个完整的AI Agent框架。**

### 🌟 核心价值

- **教学经验数字化**：将优秀教师的教学智慧转化为可复用的AI模型
- **教师专业发展**：帮助教师进行教学反思和专业成长
- **教育资源共享**：建立可传承的教学经验库
- **个性化学习支持**：为学生提供个性化的AI教师辅导

## 🏗️ 架构设计

### 三层架构设计

```
┌─────────────────────────────────────────┐
│           AI核心层 (core/)              │  ← 项目的灵魂
│  • TeacherSkillEngine (大模型集成)      │
│  • LLMProvider (多模型支持)             │
│  • Orchestrator (端到端流水线)          │
└─────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────┐
│          专业Prompt层 (prompts/)         │  ← 领域知识封装
│  • teaching_analyzer.md (教学分析)       │
│  • teacher_analyzer.md (风格建模)        │
│  • 5层人格结构分析模板                   │
└─────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────┐
│          辅助工具层 (tools/)             │  ← 辅助工具
│  • 文件解析器 (文本提取)                 │
│  • 文件管理器 (目录操作)                 │
│  • 版本控制器 (本地备份)                 │
└─────────────────────────────────────────┘
```

### 5层人格结构模型

我们采用专业的5层人格结构分析教师风格：

1. **教育理念层**：教学哲学、教育价值观
2. **教师身份层**：职业认同、角色认知  
3. **沟通风格层**：语言特点、表达方式、非语言行为
4. **课堂决策层**：教学决策、问题处理、应急反应
5. **师生关系层**：互动模式、情感连接、边界设定

## 🚀 快速开始

### 安装

```bash
# 克隆项目
git clone https://github.com/Canding3021/teacher-skill.git
cd teacher-skill

# 安装依赖
pip install -r requirements.txt

# 配置环境变量
export OPENAI_API_KEY="your-api-key-here"
```

### 基本使用

```python
from core.engine import TeacherSkillEngine, OpenAIClient

# 1. 初始化AI引擎
llm = OpenAIClient(model="gpt-4")
engine = TeacherSkillEngine(llm)

# 2. 分析教学材料
raw_text = "从教案、课件等提取的文本"
analysis = engine.analyze_teaching_materials(raw_text)

# 3. 生成教师Skill
teaching_doc = engine.generate_teaching_document(analysis)
teacher_doc = engine.generate_teacher_document(analysis)

# 4. 保存Skill
from tools.skill_writer import SkillWriter
writer = SkillWriter()
writer.create_skill("zhang_teacher", {
    "teacher_info": {"name": "张老师", "subject": "数学"},
    "documents": {"teaching": teaching_doc, "teacher": teacher_doc}
})
```

### 命令行使用

```bash
# 创建新教师Skill
python -m core.engine

# 解析教学材料
python tools/teaching_material_parser.py --file 教案.docx

# 管理教师Skill
python tools/skill_writer.py --action list
```

## 📁 项目结构

```
teacher-skill/
├── core/                          # 🎯 AI核心层
│   └── engine.py                 # 教师Skill蒸馏引擎
├── prompts/                       # 🧠 专业Prompt层
│   ├── intake.md                 # 信息录入模板
│   ├── teaching_analyzer.md      # 教学能力分析模板
│   ├── teacher_analyzer.md       # 教师风格分析模板
│   ├── teaching_builder.md       # 教学文档生成模板
│   ├── teacher_builder.md        # 风格文档生成模板
│   ├── merger.md                 # 智能合并模板
│   └── correction_handler.md     # 纠正处理模板
├── tools/                         # 🔧 辅助工具层
│   ├── teaching_material_parser.py  # 教学材料解析器
│   ├── skill_writer.py           # Skill文件写入器
│   └── version_manager.py        # 版本管理器
├── teachers/                      # 📂 生成的Skill
│   └── example_teacher/          # 示例教师
│       ├── meta.json            # 元数据
│       ├── teaching.md          # 教学能力文档
│       └── teacher.md           # 教师风格文档
├── docs/                          # 📚 文档
│   ├── ARCHITECTURE.md          # 架构设计文档
│   └── PRD.md                   # 产品需求文档
├── tests/                         # 🧪 测试
│   └── test_engine.py           # 引擎测试
├── README.md                     # 项目说明（本文档）
├── README_EN.md                  # 英文说明
├── SKILL.md                      # Claude Skill入口文件
├── INSTALL.md                    # 详细安装说明
├── LICENSE                       # MIT许可证
├── requirements.txt              # Python依赖
└── .gitignore                    # Git忽略文件
```

## 🔧 核心功能

### 1. 智能分析
- **教学能力分析**：识别教学方法、课堂管理、评估策略
- **教师风格建模**：5层人格结构分析
- **学科知识提取**：专业知识体系、教学难点、学习路径

### 2. 智能生成
- **专业文档生成**：生成结构化的教学能力文档
- **人格特征描述**：生成详细的教师风格描述
- **Skill文件整合**：生成可直接使用的AI Skill文件

### 3. 智能管理
- **版本控制**：完整的版本管理和回滚功能
- **增量更新**：支持基于新材料的智能更新
- **冲突解决**：语义级合并，避免"精神分裂"

### 4. 多模型支持
- **OpenAI GPT系列**：GPT-4, GPT-3.5-Turbo
- **Claude系列**：Claude-3-Opus, Claude-3-Sonnet
- **本地模型**：支持Ollama、vLLM等本地部署

## 🎨 示例

项目包含一个完整的示例教师：

### 张老师（数学，15年教龄）
- **教学特点**：注重思维训练，善于用生活实例解释抽象概念
- **人格特征**：严谨认真但富有幽默感，鼓励学生提问
- **专业知识**：擅长将数学知识与现实问题结合

查看完整示例：`teachers/example_teacher/`

## 📊 技术特色

### 1. 真正的AI Agent架构
- 端到端的大模型集成
- 语义级理解，非文本匹配
- 智能决策和冲突解决

### 2. 专业的教育领域适配
- 基于教育学的分析框架
- 支持多种教学场景
- 符合教师专业发展规律

### 3. 可扩展的设计
- 模块化架构，易于扩展
- 支持多种数据源和输出格式
- 可插拔的大模型提供商

### 4. 工程化质量
- 完整的错误处理和日志
- 版本控制和数据备份
- 详细的文档和示例

## 🔄 工作流程

### 创建教师Skill
```
1. 数据采集 → 2. AI分析 → 3. 文档生成 → 4. Skill整合
   ↓           ↓           ↓           ↓
教学材料    结构化分析   专业文档   可用Skill
```

### 更新教师Skill
```
现有Skill + 新材料 → AI智能合并 → 更新后Skill
      ↓                    ↓
  文本拼接（传统）    语义级合并（我们的方法）
```

## 🛠️ 开发指南

### 环境设置
```bash
# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 或 venv\Scripts\activate  # Windows

# 安装开发依赖
pip install -r requirements.txt
pip install pytest black flake8  # 开发工具
```

### 运行测试
```bash
# 运行所有测试
pytest tests/

# 运行特定测试
pytest tests/test_engine.py -v
```

### 代码规范
```bash
# 代码格式化
black core/ tools/

# 代码检查
flake8 core/ tools/
```

## 🤝 贡献指南

我们欢迎各种形式的贡献！

### 报告问题
- 使用 [GitHub Issues](https://github.com/Canding3021/teacher-skill/issues)
- 提供详细的重现步骤和环境信息

### 提交代码
1. Fork 本仓库
2. 创建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

### 开发规范
- 遵循 PEP 8 代码规范
- 添加适当的注释和文档
- 编写单元测试
- 更新相关文档

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

## 🙏 致谢

- 灵感来自 [colleague-skill](https://github.com/titanwings/colleague-skill) 项目
- 感谢所有贡献者和用户的支持
- 特别感谢教育工作者们的宝贵经验

---

</div>