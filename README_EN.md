# Teacher.skill - AI Teacher Skill Distillation Framework

<div align="center">

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.9+-green.svg)
![AI](https://img.shields.io/badge/AI-Agent%20Framework-orange.svg)

**Transform excellent teachers' pedagogical wisdom into inheritable AI Skills**

[中文](./README.md) | English

</div>

## 🎯 Project Overview

Teacher.skill is an end-to-end **AI Agent Framework** specifically designed to distill excellent teachers' teaching abilities, personality traits, and subject knowledge into structured AI teacher skill files.

> **This is not a traditional Python script project, but a complete AI Agent framework.**

### 🌟 Core Value

- **Digitizing Teaching Experience**: Transform excellent teachers' pedagogical wisdom into reusable AI models
- **Teacher Professional Development**: Help teachers with teaching reflection and professional growth
- **Educational Resource Sharing**: Build an inheritable teaching experience repository
- **Personalized Learning Support**: Provide students with personalized AI teacher tutoring

## 🏗️ Architecture Design

### Three-Layer Architecture

```
┌─────────────────────────────────────────┐
│        AI Core Layer (core/)            │  ← Soul of the project
│  • TeacherSkillEngine (LLM Integration) │
│  • LLMProvider (Multi-model Support)    │
│  • Orchestrator (End-to-end Pipeline)   │
└─────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────┐
│     Professional Prompt Layer (prompts/) │  ← Domain knowledge encapsulation
│  • teaching_analyzer.md (Teaching Analysis)│
│  • teacher_analyzer.md (Style Modeling) │
│  • 5-layer Personality Structure Templates│
└─────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────┐
│      Auxiliary Tools Layer (tools/)     │  ← Auxiliary tools
│  • File Parser (Text Extraction)        │
│  • File Manager (Directory Operations)  │
│  • Version Controller (Local Backup)    │
└─────────────────────────────────────────┘
```

### 5-Layer Personality Structure Model

We employ a professional 5-layer personality structure to analyze teacher styles:

1. **Educational Philosophy Layer**: Teaching philosophy, educational values
2. **Teacher Identity Layer**: Professional identity, role perception
3. **Communication Style Layer**: Language characteristics, expression methods, non-verbal behaviors
4. **Classroom Decision Layer**: Teaching decisions, problem handling, emergency responses
5. **Teacher-Student Relationship Layer**: Interaction patterns, emotional connections, boundary setting

## 🚀 Quick Start

### Installation

```bash
# Clone the project
git clone https://github.com/Canding3021/teacher-skill.git
cd teacher-skill

# Install dependencies
pip install -r requirements.txt

# Configure environment variables
export OPENAI_API_KEY="your-api-key-here"
```

### Basic Usage

```python
from core.engine import TeacherSkillEngine, OpenAIClient

# 1. Initialize AI engine
llm = OpenAIClient(model="gpt-4")
engine = TeacherSkillEngine(llm)

# 2. Analyze teaching materials
raw_text = "Text extracted from lesson plans, courseware, etc."
analysis = engine.analyze_teaching_materials(raw_text)

# 3. Generate teacher skill
teaching_doc = engine.generate_teaching_document(analysis)
teacher_doc = engine.generate_teacher_document(analysis)

# 4. Save skill
from tools.skill_writer import SkillWriter
writer = SkillWriter()
writer.create_skill("zhang_teacher", {
    "teacher_info": {"name": "Teacher Zhang", "subject": "Mathematics"},
    "documents": {"teaching": teaching_doc, "teacher": teacher_doc}
})
```

### Command Line Usage

```bash
# Create new teacher skill
python -m core.engine

# Parse teaching materials
python tools/teaching_material_parser.py --file lesson_plan.docx

# Manage teacher skills
python tools/skill_writer.py --action list
```

## 📁 Project Structure

```
teacher-skill/
├── core/                          # 🎯 AI Core Layer
│   └── engine.py                 # Teacher Skill Distillation Engine
├── prompts/                       # 🧠 Professional Prompt Layer
│   ├── intake.md                 # Information intake template
│   ├── teaching_analyzer.md      # Teaching ability analysis template
│   ├── teacher_analyzer.md       # Teacher style analysis template
│   ├── teaching_builder.md       # Teaching document generation template
│   ├── teacher_builder.md        # Style document generation template
│   ├── merger.md                 # Intelligent merge template
│   └── correction_handler.md     # Correction handling template
├── tools/                         # 🔧 Auxiliary Tools Layer
│   ├── teaching_material_parser.py  # Teaching material parser
│   ├── skill_writer.py           # Skill file writer
│   └── version_manager.py        # Version manager
├── teachers/                      # 📂 Generated Skills
│   └── example_teacher/          # Example teacher
│       ├── meta.json            # Metadata
│       ├── teaching.md          # Teaching ability document
│       └── teacher.md           # Teacher style document
├── docs/                          # 📚 Documentation
│   ├── ARCHITECTURE.md          # Architecture design document
│   └── PRD.md                   # Product requirements document
├── tests/                         # 🧪 Tests
│   └── test_engine.py           # Engine tests
├── README.md                     # Project description (Chinese)
├── README_EN.md                  # Project description (English)
├── SKILL.md                      # Claude Skill entry file
├── INSTALL.md                    # Detailed installation instructions
├── LICENSE                       # MIT License
├── requirements.txt              # Python dependencies
└── .gitignore                    # Git ignore file
```

## 🔧 Core Features

### 1. Intelligent Analysis
- **Teaching Ability Analysis**: Identify teaching methods, classroom management, assessment strategies
- **Teacher Style Modeling**: 5-layer personality structure analysis
- **Subject Knowledge Extraction**: Professional knowledge systems, teaching difficulties, learning paths

### 2. Intelligent Generation
- **Professional Document Generation**: Generate structured teaching ability documents
- **Personality Trait Description**: Generate detailed teacher style descriptions
- **Skill File Integration**: Generate directly usable AI skill files

### 3. Intelligent Management
- **Version Control**: Complete version management and rollback functionality
- **Incremental Updates**: Support intelligent updates based on new materials
- **Conflict Resolution**: Semantic-level merging to avoid "schizophrenia"

### 4. Multi-model Support
- **OpenAI GPT Series**: GPT-4, GPT-3.5-Turbo
- **Claude Series**: Claude-3-Opus, Claude-3-Sonnet
- **Local Models**: Support for local deployments like Ollama, vLLM

## 🎨 Examples

The project includes a complete example teacher:

### Teacher Zhang (Mathematics, 15 years of experience)
- **Teaching Characteristics**: Focuses on thinking training, good at explaining abstract concepts with real-life examples
- **Personality Traits**: Rigorous and serious but humorous, encourages students to ask questions
- **Professional Knowledge**: Skilled at combining mathematical knowledge with real-world problems

View the complete example: `teachers/example_teacher/`

## 📊 Technical Features

### 1. True AI Agent Architecture
- End-to-end large model integration
- Semantic-level understanding, not text matching
- Intelligent decision-making and conflict resolution

### 2. Professional Education Domain Adaptation
- Analysis framework based on pedagogy
- Support for multiple teaching scenarios
- Conforms to teacher professional development patterns

### 3. Extensible Design
- Modular architecture, easy to extend
- Support for multiple data sources and output formats
- Pluggable large model providers

### 4. Engineering Quality
- Complete error handling and logging
- Version control and data backup
- Detailed documentation and examples

## 🔄 Workflow

### Creating Teacher Skills
```
1. Data Collection → 2. AI Analysis → 3. Document Generation → 4. Skill Integration
   ↓               ↓               ↓               ↓
Teaching      Structured      Professional    Usable
Materials     Analysis        Documents       Skills
```

### Updating Teacher Skills
```
Existing Skill + New Materials → AI Intelligent Merge → Updated Skill
      ↓                            ↓
Text Concatenation          Semantic-level Merge
  (Traditional)                (Our Approach)
```

## 🛠️ Development Guide

### Environment Setup
```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or venv\Scripts\activate  # Windows

# Install development dependencies
pip install -r requirements.txt
pip install pytest black flake8  # Development tools
```

### Running Tests
```bash
# Run all tests
pytest tests/

# Run specific tests
pytest tests/test_engine.py -v
```

### Code Standards
```bash
# Code formatting
black core/ tools/

# Code checking
flake8 core/ tools/
```

## 🤝 Contributing

We welcome contributions of all kinds!

### Reporting Issues
- Use [GitHub Issues](https://github.com/Canding3021/teacher-skill/issues)
- Provide detailed reproduction steps and environment information

### Submitting Code
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Development Standards
- Follow PEP 8 code standards
- Add appropriate comments and documentation
- Write unit tests
- Update relevant documentation

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.


## 🙏 Acknowledgments

- Inspired by the [colleague-skill](https://github.com/titanwings/colleague-skill) project
- Thanks to all contributors and users for their support
- Special thanks to educators for their valuable experience

---


</div>