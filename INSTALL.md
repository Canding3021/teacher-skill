# 安装指南

## 📋 系统要求

### 操作系统
- **Linux** (Ubuntu 20.04+, CentOS 7+)
- **macOS** (10.15+)
- **Windows** (10+, 建议使用WSL2)

### Python版本
- Python 3.9 或更高版本
- 推荐使用 Python 3.10+

### 硬件要求
- **内存**: 至少 4GB RAM
- **存储**: 至少 500MB 可用空间
- **网络**: 稳定的互联网连接（用于API调用）

## 🚀 快速安装

### 方法一：直接克隆（推荐）

```bash
# 克隆项目
git clone https://github.com/Canding3021/teacher-skill.git
cd teacher-skill

# 创建虚拟环境
python -m venv venv

# 激活虚拟环境
# Linux/Mac:
source venv/bin/activate
# Windows:
# venv\Scripts\activate

# 安装依赖
pip install -r requirements.txt
```

### 方法二：使用pip安装（开发中）

```bash
# 项目发布后可用
pip install teacher-skill
```

### 方法三：Docker安装

```bash
# 构建Docker镜像
docker build -t teacher-skill .

# 运行容器
docker run -it --rm -v $(pwd)/data:/app/data teacher-skill
```

## 🔧 详细安装步骤

### 1. 环境准备

#### Linux/Ubuntu
```bash
# 更新系统包
sudo apt update && sudo apt upgrade -y

# 安装Python和pip
sudo apt install python3 python3-pip python3-venv -y

# 安装开发工具
sudo apt install git curl wget -y
```

#### macOS
```bash
# 使用Homebrew安装Python
brew install python@3.10

# 验证安装
python3 --version
pip3 --version
```

#### Windows
```bash
# 使用WSL2（推荐）
# 1. 启用WSL2功能
# 2. 从Microsoft Store安装Ubuntu
# 3. 按照Linux步骤继续

# 或使用Python官方安装包
# 下载地址：https://www.python.org/downloads/
```

### 2. 项目配置

#### 克隆项目
```bash
# 克隆主仓库
git clone https://github.com/Canding3021/teacher-skill.git

# 或克隆特定分支
git clone -b develop https://github.com/Canding3021/teacher-skill.git

# 进入项目目录
cd teacher-skill
```

#### 虚拟环境设置
```bash
# 创建虚拟环境
python3 -m venv venv

# 激活虚拟环境
# Linux/Mac:
source venv/bin/activate
# Windows PowerShell:
# .\venv\Scripts\Activate.ps1
# Windows CMD:
# venv\Scripts\activate.bat

# 验证激活
which python  # 应该显示venv/bin/python
```

#### 安装依赖
```bash
# 升级pip
pip install --upgrade pip

# 安装项目依赖
pip install -r requirements.txt

# 安装开发依赖（可选）
pip install pytest black flake8 mypy
```

### 3. API密钥配置

#### OpenAI API
```bash
# 设置环境变量
export OPENAI_API_KEY="sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"

# 或创建.env文件
echo "OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx" > .env
```

#### Claude API
```bash
# 设置环境变量
export ANTHROPIC_API_KEY="sk-ant-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"

# 或添加到.env文件
echo "ANTHROPIC_API_KEY=sk-ant-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx" >> .env
```

#### 本地模型配置
```bash
# 如果使用本地模型（如Ollama）
# 1. 安装Ollama
curl -fsSL https://ollama.com/install.sh | sh

# 2. 下载模型
ollama pull qwen2.5:7b

# 3. 设置环境变量
export LOCAL_LLM_URL="http://localhost:11434"
export LOCAL_LLM_MODEL="qwen2.5:7b"
```

### 4. 验证安装

#### 运行测试
```bash
# 运行单元测试
pytest tests/ -v

# 运行特定测试
pytest tests/test_engine.py -v
```

#### 快速验证
```bash
# 检查Python版本
python --version

# 检查依赖安装
python -c "import requests; print('requests:', requests.__version__)"
python -c "import openai; print('openai:', openai.__version__)"

# 运行示例
python -m core.engine
```

## 🎯 不同使用场景的安装

### 场景一：开发者/研究者

```bash
# 完整开发环境
git clone https://github.com/Canding3021/teacher-skill.git
cd teacher-skill
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install -r requirements-dev.txt  # 开发依赖
pre-commit install  # 安装代码检查钩子
```

### 场景二：教育机构/学校

```bash
# 生产环境部署
git clone https://github.com/Canding3021/teacher-skill.git
cd teacher-skill

# 使用Docker Compose
docker-compose up -d

# 或使用系统服务
sudo cp systemd/teacher-skill.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable teacher-skill
sudo systemctl start teacher-skill
```

### 场景三：个人用户/教师

```bash
# 简化安装
git clone https://github.com/Canding3021/teacher-skill.git
cd teacher-skill

# 使用安装脚本
chmod +x install.sh
./install.sh

# 或使用图形界面安装器（如果提供）
python setup_gui.py
```

## 🔧 高级配置

### 配置文件

创建 `config.yaml` 文件：

```yaml
# config.yaml
llm:
  provider: "openai"  # openai, claude, local
  model: "gpt-4"
  temperature: 0.2
  max_tokens: 4000

paths:
  teachers_dir: "./teachers"
  prompts_dir: "./prompts"
  logs_dir: "./logs"

features:
  enable_versioning: true
  enable_backup: true
  enable_analytics: false

logging:
  level: "INFO"
  format: "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
  file: "teacher_skill.log"
```

### 环境变量

```bash
# 核心配置
export TEACHER_SKILL_LLM_PROVIDER="openai"
export TEACHER_SKILL_MODEL="gpt-4"
export TEACHER_SKILL_TEACHERS_DIR="./teachers"

# 性能配置
export TEACHER_SKILL_MAX_WORKERS="4"
export TEACHER_SKILL_CACHE_SIZE="100"
export TEACHER_SKILL_REQUEST_TIMEOUT="30"

# 日志配置
export TEACHER_SKILL_LOG_LEVEL="INFO"
export TEACHER_SKILL_LOG_FILE="teacher_skill.log"
```

### 数据库配置（可选）

```bash
# 安装数据库依赖
pip install sqlalchemy alembic psycopg2-binary

# 初始化数据库
alembic upgrade head

# 或使用SQLite（默认）
# 无需额外配置
```

## 🐛 故障排除

### 常见问题

#### 1. Python版本问题
```bash
# 检查Python版本
python --version

# 如果版本低于3.9，升级Python
# Ubuntu:
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt install python3.10 python3.10-venv

# macOS:
brew install python@3.10
```

#### 2. 虚拟环境问题
```bash
# 如果venv命令不可用
python3 -m ensurepip --upgrade
python3 -m pip install virtualenv

# 重新创建虚拟环境
rm -rf venv
python3 -m venv venv
source venv/bin/activate
```

#### 3. 依赖安装失败
```bash
# 使用国内镜像源
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

# 或逐个安装
pip install requests
pip install openai
# ...
```

#### 4. API密钥问题
```bash
# 检查环境变量
echo $OPENAI_API_KEY

# 重新设置
export OPENAI_API_KEY="your-key-here"

# 永久设置（添加到~/.bashrc或~/.zshrc）
echo 'export OPENAI_API_KEY="your-key-here"' >> ~/.bashrc
source ~/.bashrc
```

#### 5. 权限问题
```bash
# 如果遇到权限错误
sudo chmod -R 755 /path/to/teacher-skill

# 或使用用户目录
mkdir -p ~/projects/teacher-skill
cd ~/projects/teacher-skill
```

### 获取帮助

1. **查看日志**
   ```bash
   tail -f teacher_skill.log
   ```

2. **启用调试模式**
   ```bash
   export TEACHER_SKILL_LOG_LEVEL="DEBUG"
   python -m core.engine
   ```

3. **查看帮助**
   ```bash
   python -m core.engine --help
   python tools/skill_writer.py --help
   ```

4. **联系支持**
   - GitHub Issues: https://github.com/Canding3021/teacher-skill/issues
   - 邮件: 查看项目README中的联系方式

## 🔄 更新与升级

### 更新项目
```bash
# 拉取最新代码
git pull origin main

# 更新依赖
pip install -r requirements.txt --upgrade

# 运行数据库迁移（如果有）
alembic upgrade head
```

### 升级到新版本
```bash
# 备份当前数据
cp -r teachers/ teachers_backup_$(date +%Y%m%d)

# 重新克隆
cd ..
rm -rf teacher-skill
git clone https://github.com/Canding3021/teacher-skill.git
cd teacher-skill

# 恢复数据
cp -r ../teachers_backup_$(date +%Y%m%d)/ teachers/

# 重新安装
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## 📚 下一步

安装完成后，建议：

1. **阅读文档**
   ```bash
   # 查看架构设计
   cat docs/ARCHITECTURE.md
   
   # 查看使用指南
   cat docs/USAGE.md
   ```

2. **运行示例**
   ```bash
   # 运行示例脚本
   python examples/basic_usage.py
   
   # 查看示例教师
   ls teachers/example_teacher/
   ```

3. **开始使用**
   ```bash
   # 创建第一个教师Skill
   python -m core.engine --create
   
   # 或使用命令行工具
   python tools/cli.py create --name "张老师" --subject "数学"
   ```

4. **加入社区**
   - 关注GitHub仓库获取更新
   - 参与讨论和贡献
   - 报告问题和建议

---

**安装遇到问题？** 请查看 [GitHub Issues](https://github.com/Canding3021/teacher-skill/issues) 或创建新的issue。