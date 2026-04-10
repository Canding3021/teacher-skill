# 架构设计文档

## 🏗️ 整体架构

```
┌─────────────────────────────────────────────────────────┐
│                   用户界面层                            │
│  (CLI / Web UI / API Gateway)                          │
└─────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────┐
│                   AI核心引擎层                           │  ← 项目的灵魂
│  ┌─────────────────────────────────────────────────┐   │
│  │           TeacherSkillEngine                    │   │
│  │  • analyze_teaching_materials()                │   │
│  │  • analyze_teacher_style()                     │   │
│  │  • generate_teaching_document()                │   │
│  │  • merge_updates()                             │   │
│  └─────────────────────────────────────────────────┘   │
│  ┌─────────────────────────────────────────────────┐   │
│  │             LLMProvider (抽象)                   │   │
│  │  • OpenAI / Claude / 本地模型                   │   │
│  │  • 统一接口，可插拔设计                         │   │
│  └─────────────────────────────────────────────────┘   │
│  ┌─────────────────────────────────────────────────┐   │
│  │               Orchestrator                      │   │
│  │  • 端到端工作流管理                            │   │
│  │  • 错误处理和监控                             │   │
│  └─────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────┐
│                专业Prompt模板层                          │  ← 领域知识封装
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐   │
│  │教学分析  │ │风格建模  │ │文档生成  │ │智能合并  │   │
│  │模板      │ │模板      │ │模板      │ │模板      │   │
│  └──────────┘ └──────────┘ └──────────┘ └──────────┘   │
│  • 基于教育学的专业分析框架                            │
│  • 5层人格结构建模                                    │
│  • 语义级理解，非正则匹配                             │
└─────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────┐
│                 数据持久化层                            │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐                │
│  │Skill存储 │ │版本管理  │ │元数据    │                │
│  │(.md文件) │ │(本地备份)│ │(.json)   │                │
│  └──────────┘ └──────────┘ └──────────┘                │
└─────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────┐
│                 辅助工具层                              │  ← 只是辅助
│  ┌──────────┐ ┌──────────┐ ┌──────────┐                │
│  │文件解析器│ │文件管理器│ │版本控制器│                │
│  │(文本提取)│ │(目录操作)│ │(备份回滚)│                │
│  └──────────┘ └──────────┘ └──────────┘                │
│  • 不包含AI逻辑                                        │
│  • 只是数据准备和文件操作                              │
└─────────────────────────────────────────────────────────┘
```

## 🔄 数据流设计

### 创建教师Skill的完整流程
```
1. 数据准备阶段
   ┌─────────────┐    ┌─────────────┐    ┌─────────────┐
   │  原始材料   │───▶│ 文件解析器  │───▶│  原始文本   │
   │(教案/课件)  │    │ (tools/)    │    │             │
   └─────────────┘    └─────────────┘    └─────────────┘

2. AI分析阶段（核心价值）
   ┌─────────────┐    ┌─────────────┐    ┌─────────────┐
   │  原始文本   │───▶│ AI分析引擎  │───▶│结构化分析  │
   │             │    │  (core/)    │    │   结果      │
   └─────────────┘    │• 大模型调用 │    └─────────────┘
                      │• Prompt工程 │
                      └─────────────┘

3. 文档生成阶段
   ┌─────────────┐    ┌─────────────┐    ┌─────────────┐
   │结构化分析  │───▶│ AI生成引擎  │───▶│专业文档     │
   │   结果      │    │  (core/)    │    │(.md文件)    │
   └─────────────┘    │• 文档生成   │    └─────────────┘
                      │• 格式优化   │
                      └─────────────┘

4. 文件输出阶段
   ┌─────────────┐    ┌─────────────┐    ┌─────────────┐
   │专业文档     │───▶│ 文件管理器  │───▶│Skill目录   │
   │(.md文件)    │    │ (tools/)    │    │结构        │
   └─────────────┘    └─────────────┘    └─────────────┘
```

### 智能更新流程（解决"精神分裂"问题）
```
传统方法（有问题）：
现有文档 + 新内容 → 文本拼接 → 冲突文档

我们的方法（语义级合并）：
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│  现有文档   │    │   新内容    │    │ 智能合并    │
│             │    │             │    │  引擎       │
└─────────────┘    └─────────────┘    │ (core/)    │
        │               │              │• 冲突检测  │
        └───────────────┼──────────────▶│• 语义融合  │
                        │              │• 一致性保持│
                        │              └─────────────┘
                        │                      │
                        └──────────────────────┘
                                      ▼
                              ┌─────────────┐
                              │ 融合后文档  │
                              │（无冲突）   │
                              └─────────────┘
```

## 🧩 核心组件设计

### 1. TeacherSkillEngine (`core/engine.py`)
```python
class TeacherSkillEngine:
    """教师Skill蒸馏引擎 - 真正的AI核心"""
    
    def __init__(self, llm_provider: LLMProvider):
        self.llm = llm_provider  # 可插拔的大模型提供商
    
    def analyze_teaching_materials(self, raw_text: str) -> Dict[str, Any]:
        """核心AI分析：教学材料 → 结构化分析结果"""
        # 1. 加载专业分析prompt
        analyzer_prompt = self.load_prompt("teaching_analyzer")
        
        # 2. 调用大模型进行深度分析
        analysis_result = self.llm.call(
            prompt=analyzer_prompt,
            context=raw_text,
            temperature=0.2,
            response_format={"type": "json_object"}
        )
        
        return analysis_result
    
    def merge_updates(self, original_doc: str, updates: List[str]) -> str:
        """智能合并：语义级合并，非文本拼接"""
        merger_prompt = self.load_prompt("merger")
        
        # 构建合并上下文
        context = {"original": original_doc, "updates": updates}
        
        merged_result = self.llm.call(
            prompt=merger_prompt,
            context=json.dumps(context),
            temperature=0.25
        )
        
        return merged_result.get("merged_content")
```

### 2. LLMProvider抽象层
```python
class LLMProvider(ABC):
    """大模型提供商抽象接口"""
    
    @abstractmethod
    def call(self, prompt: str, context: str, **kwargs) -> Dict[str, Any]:
        """调用大模型API"""
        pass
    
    @abstractmethod
    def stream(self, prompt: str, context: str, **kwargs):
        """流式调用"""
        pass


class OpenAIClient(LLMProvider):
    """OpenAI实现"""
    
    def call(self, prompt: str, context: str, **kwargs) -> Dict[str, Any]:
        # 实际调用OpenAI API
        pass


class ClaudeClient(LLMProvider):
    """Claude实现"""
    
    def call(self, prompt: str, context: str, **kwargs) -> Dict[str, Any]:
        # 实际调用Claude API
        pass


class LocalLLMClient(LLMProvider):
    """本地模型实现"""
    
    def call(self, prompt: str, context: str, **kwargs) -> Dict[str, Any]:
        # 调用本地模型服务
        pass
```

### 3. Orchestrator编排器
```python
class Orchestrator:
    """编排器 - 端到端工作流管理"""
    
    def create_teacher_skill(self, materials_dir: str, teacher_info: Dict) -> Dict[str, Any]:
        """完整的教师Skill创建流水线"""
        # 1. 数据准备
        raw_materials = self._prepare_materials(materials_dir)
        
        # 2. AI分析（核心）
        teaching_analysis = self.engine.analyze_teaching_materials(raw_materials)
        style_analysis = self.engine.analyze_teacher_style(raw_materials)
        
        # 3. AI生成
        teaching_doc = self.engine.generate_teaching_document(teaching_analysis)
        teacher_doc = self.engine.generate_teacher_document(style_analysis)
        
        # 4. 整合输出
        return {
            "teacher_info": teacher_info,
            "analysis": {"teaching": teaching_analysis, "style": style_analysis},
            "documents": {"teaching": teaching_doc, "teacher": teacher_doc}
        }
```

## 🎯 设计原则

### 1. 清晰的职责分离
- **AI核心层** (`core/`): 大模型集成、语义分析、智能生成
- **领域知识层** (`prompts/`): 专业分析模板、教育领域适配
- **辅助工具层** (`tools/`): 文本提取、文件管理、版本控制

### 2. 可插拔架构
- 支持多种大模型提供商
- 可替换的分析模板
- 可扩展的输出格式

### 3. 语义级处理
- 不用正则表达式硬抠文本
- 用大模型真正理解内容
- 智能合并解决冲突

### 4. 专业领域适配
- 基于教育学的分析框架
- 教师专业发展支持
- 教学经验数字化

## ⚙️ 技术选型

### AI/ML层
- **大模型API**: OpenAI GPT-4, Claude 3, 本地模型
- **Prompt工程**: 结构化模板，few-shot learning
- **输出格式**: JSON Schema约束，保证结构化

### 应用层
- **语言**: Python 3.9+
- **Web框架**: FastAPI (用于API服务)
- **任务队列**: Celery (用于异步处理)

### 数据层
- **文件存储**: 本地文件系统 + 版本控制
- **元数据**: JSON格式，易于解析
- **缓存**: Redis (用于API响应缓存)

### 工具层
- **文档解析**: pdfplumber, python-docx
- **文本处理**: jieba, pypinyin
- **版本控制**: 自定义版本管理系统

## 🚀 扩展性设计

### 1. 添加新的大模型提供商
```python
class NewLLMProvider(LLMProvider):
    def call(self, prompt: str, context: str, **kwargs) -> Dict[str, Any]:
        # 实现新的大模型调用逻辑
        pass
```

### 2. 添加新的分析维度
```python
# 在prompts/目录添加新的分析模板
# 在engine.py中添加新的分析方法
def analyze_new_dimension(self, materials: List[Dict]) -> Dict[str, Any]:
    new_prompt = self.load_prompt("new_analyzer")
    return self.llm.call(prompt=new_prompt, context=json.dumps(materials))
```

### 3. 支持新的输出格式
```python
def export_to_openai_assistant(self, skill_data: Dict) -> Dict[str, Any]:
    """导出为OpenAI Assistant格式"""
    pass

def export_to_langchain_agent(self, skill_data: Dict) -> Dict[str, Any]:
    """导出为LangChain Agent格式"""
    pass
```

## 📊 性能考虑

### 1. 大模型调用优化
- **批处理**: 合并多个小请求
- **缓存**: 缓存相似的分析结果
- **流式响应**: 支持实时生成

### 2. 内存管理
- **分块处理**: 大文件分块分析
- **懒加载**: 按需加载prompt模板
- **清理机制**: 及时释放大模型响应

### 3. 并发处理
- **异步调用**: 支持并发的大模型请求
- **队列管理**: 控制并发数量
- **超时处理**: 防止长时间阻塞

## 🔒 安全考虑

### 1. 数据隐私
- **本地处理**: 敏感数据不上传
- **匿名化**: 移除个人信息
- **加密存储**: 敏感数据加密

### 2. API安全
- **密钥管理**: 安全的API密钥存储
- **访问控制**: 基于角色的权限
- **审计日志**: 记录所有API调用

### 3. 内容安全
- **内容过滤**: 防止生成不当内容
- **事实核查**: 验证生成内容的准确性
- **透明度**: 明确标注AI生成内容

---

**这不是一个传统的软件项目，而是一个AI Agent框架的标准实现。**