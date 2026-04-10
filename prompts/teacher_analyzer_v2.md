# 教师风格分析模板 v2 - 结构化契约版

## 🎯 核心指令

**严格遵循以下JSON Schema输出，不要添加任何额外文本。**
**不要使用空泛的形容词（如"优秀"、"负责"），必须引用材料中的具体行为。**

## 📋 输出契约

```typescript
interface TeacherStyleAnalysis {
  // Layer 0: 教育理念（核心原则）
  layer_0: {
    core_beliefs: string[];           // 根本教育信念（必须从材料中推导）
    non_negotiables: string[];        // 不可妥协的规则
    value_hierarchy: {                // 价值排序（必须有证据支持）
      primary: string;
      secondary: string;
      tertiary: string;
    };
  };
  
  // Layer 1: 教师身份（职业认知）
  layer_1: {
    primary_role: "知识传授者" | "学习引导者" | "成长陪伴者" | "人生导师" | "严师慈母/父";
    secondary_roles: string[];
    professional_identity: {
      strength: string;               // 专业优势（具体领域）
      mission: string;                // 职业使命
      challenge: string;              // 面临的挑战
    };
    self_efficacy: {
      confidence: number;             // 0-1，必须有行为证据
      growth_mindset: boolean;        // 必须有学习行为证据
      adaptability: number;           // 0-1，必须有适应行为证据
    };
  };
  
  // Layer 2: 沟通风格（表达方式）
  layer_2: {
    verbal_habits: {
      catchphrases: string[];         // 口头禅（必须出现在材料中）
      high_frequency: string[];       // 高频词（统计频率>3次）
      sentence_patterns: string[];    // 句式模式
    };
    communication_style: {
      formality: number;              // 0-1，0最随意，1最正式
      directness: number;             // 0-1，0最委婉，1最直接
      humor_level: number;            // 0-1，0无幽默，1幽默频繁
      warmth: number;                 // 0-1，0冷淡，1温暖
    };
    feedback_patterns: {
      praise: string[];               // 表扬方式（具体例子）
      correction: string[];           // 纠正方式（具体例子）
      encouragement: string[];        // 鼓励方式（具体例子）
    };
  };
  
  // Layer 3: 课堂决策（行为模式）
  layer_3: {
    decision_making: {
      primary_mode: "分析型" | "直觉型" | "民主型" | "权威型";
      secondary_mode: string;
      process: string[];              // 决策流程步骤
      criteria: string[];             // 决策标准
      speed: "快速" | "中等" | "谨慎";
    };
    problem_solving: {
      approach: string;               // 问题解决方式
      steps: string[];                // 解决步骤
      resources: string[];            // 依赖资源
    };
    time_management: {
      planning: string;               // 计划方式
      prioritization: string;         // 优先级原则
      delegation: string;             // 授权方式
    };
  };
  
  // Layer 4: 师生关系（人际互动）
  layer_4: {
    relationship_style: {
      primary: "权威型" | "民主型" | "朋友型" | "导师型";
      secondary: string;
      distance: "亲密" | "适度亲近" | "疏远";
      boundaries: string;             // 边界设置方式
      trust_building: string[];       // 信任建立行为
    };
    emotional_support: {
      availability: string;           // 情感支持可及性
      approach: string;               // 支持方式
      methods: string[];              // 具体方法
    };
    conflict_management: {
      prevention: string[];           // 冲突预防策略
      resolution: string[];           // 冲突解决步骤
      learning: string[];             // 从冲突中学到什么
    };
  };
  
  // 元数据
  metadata: {
    consistency_score: number;        // 0-1，风格一致性
    authenticity_score: number;       // 0-1，与材料匹配度
    distinctiveness: number;          // 0-1，独特性
    evidence_count: number;           // 引用的具体行为数量
    confidence_level: "high" | "medium" | "low";  // 分析置信度
  };
}
```

## 🚫 负面约束（必须遵守）

1. **禁止空泛形容词**：
   - ❌ "优秀"、"负责"、"认真"、"热情"
   - ✅ "在材料第3页，当学生提问时，他花了15分钟详细解释"
   - ✅ "在课堂记录中，他使用了'我们来思考一下'共8次"

2. **禁止无证据推断**：
   - ❌ "他应该很关心学生"
   - ✅ "在学生日记中提到'老师课后留下来帮我补课'"
   - ✅ "家长群聊天记录显示他每周发3次学习提醒"

3. **禁止过度概括**：
   - ❌ "他总是很有耐心"
   - ✅ "在10次学生提问中，有9次他回答时间超过2分钟"
   - ✅ "在5个课堂冲突案例中，他都采用了私下谈话方式"

4. **禁止主观评价**：
   - ❌ "这种方法很好"
   - ✅ "这种方法在材料中被使用了3次"
   - ✅ "学生反馈显示这种方法接受度较高"

## 🔍 分析流程

### 步骤1：证据收集
对于每个Layer，必须：
1. **定位具体材料**：标注材料来源（文件、页码、时间戳）
2. **统计出现频率**：关键行为/语言的重复次数
3. **记录上下文**：行为发生的情境

### 步骤2：模式识别
1. **行为聚类**：将相似行为归类
2. **频率分析**：计算行为频率
3. **情境分析**：识别行为触发条件

### 步骤3：结构化编码
1. **映射到Schema**：将证据映射到JSON字段
2. **计算数值**：基于证据计算数值字段
3. **评估置信度**：基于证据充分性评估置信度

## 📊 证据要求

### 最低证据标准
- **Layer 0-1**：至少3个独立证据
- **Layer 2**：至少5个语言样本
- **Layer 3**：至少2个决策案例
- **Layer 4**：至少3个互动记录

### 证据质量分级
- **A级**：直接引用、具体行为、可验证
- **B级**：间接推断、合理推测
- **C级**：模糊描述、需要更多证据

## 🎨 示例输出

```json
{
  "layer_0": {
    "core_beliefs": [
      "在教案反思中写道：'错误是学习的最好机会，不要怕犯错'（材料：教案_20240315.docx，第2页）",
      "在教研会议记录中说：'每个学生都有闪光点，只是需要时间发现'（材料：教研记录_20240320.txt，第3段）"
    ],
    "non_negotiables": [
      "课堂规则第一条：'绝不公开批评学生'（材料：课堂规则.pdf）",
      "作业要求：'必须当天批改反馈'（材料：学生作业样本，10份中有9份当天批改）"
    ],
    "value_hierarchy": {
      "primary": "学生成长",
      "secondary": "知识掌握", 
      "tertiary": "考试成绩"
    }
  },
  "layer_1": {
    "primary_role": "学习引导者",
    "secondary_roles": ["知识传授者", "成长陪伴者"],
    "professional_identity": {
      "strength": "数学问题解决教学（材料：5个问题解决教案）",
      "mission": "激发学生对数学的兴趣（材料：3次公开课主题）",
      "challenge": "平衡个性化教学与统一进度（材料：教学反思中提到3次）"
    },
    "self_efficacy": {
      "confidence": 0.8,
      "growth_mindset": true,
      "adaptability": 0.75
    }
  },
  "layer_2": {
    "verbal_habits": {
      "catchphrases": ["我们来思考一下", "这个想法很有意思", "还有没有其他可能"],
      "high_frequency": ["理解", "思考", "尝试", "分享"],
      "sentence_patterns": ["如果...那么...", "不仅...而且...", "为什么...因为..."]
    },
    "communication_style": {
      "formality": 0.6,
      "directness": 0.7,
      "humor_level": 0.4,
      "warmth": 0.8
    },
    "feedback_patterns": {
      "praise": ["具体肯定+原因", "公开表扬"],
      "correction": ["私下指出+建议", "先肯定后改进"],
      "encouragement": ["强调进步", "降低焦虑"]
    }
  },
  "metadata": {
    "consistency_score": 0.85,
    "authenticity_score": 0.8,
    "distinctiveness": 0.75,
    "evidence_count": 23,
    "confidence_level": "high"
  }
}
```

## 🔄 验证检查清单

在输出前检查：
- [ ] 所有字段都有值（不允许null）
- [ ] 所有字符串都有材料引用
- [ ] 所有数值都有计算依据
- [ ] 遵守了负面约束
- [ ] 证据数量达到最低要求
- [ ] 置信度评估合理

## 📝 特殊情况处理

### 证据不足
如果某个Layer证据不足：
1. 将对应字段设为空数组/默认值
2. 在metadata.confidence_level中标注"low"
3. 在metadata中说明缺少的证据类型

### 矛盾证据
如果发现矛盾证据：
1. 记录所有证据
2. 分析矛盾原因（情境差异、发展阶段）
3. 在metadata中标注矛盾点
4. 输出最一致的版本，但标注不确定性

### 材料过多
如果材料超过5000 tokens：
1. 分批处理，每批不超过5000 tokens
2. 每批生成部分分析
3. 最后合并分析结果
4. 在metadata中说明分批处理情况

## 🎯 最终指令

**输出必须是纯JSON格式，符合上述Schema。**
**不要添加任何解释、说明或其他文本。**
**JSON必须有效且可解析。**