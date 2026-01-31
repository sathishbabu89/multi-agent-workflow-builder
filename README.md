# 🤖 DevHero - Multi-Agent Workflow Automation

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Streamlit](https://img.shields.io/badge/streamlit-1.28+-red.svg)](https://streamlit.io)
[![CrewAI](https://img.shields.io/badge/crewai-latest-green.svg)](https://github.com/joaomdmoura/crewAI)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

DevHero is an intelligent AI orchestration platform that transforms natural language requirements into working code through dynamic multi-agent collaboration with human oversight.

## ✨ Key Features

- 🧠 **Dynamic Agent Creation** - Automatically generates specialized AI agents based on your requirements
- 👥 **Human-in-the-Loop** - Approve or refine each phase before proceeding
- 🔄 **Adaptive Planning** - Manager agent creates minimal, efficient execution plans
- 📦 **Multiple Export Options** - Download as ZIP or push directly to GitHub
- 🎯 **Smart File Detection** - Automatic file type detection and code extraction
- 🔧 **Tech-Agnostic** - Supports React, Spring Boot, Angular, Python, Go, and more

## 🚀 Quick Start

### Prerequisites
```bash
Python 3.8+
Git (for GitHub integration)
OpenAI API key or compatible LLM API
```

### Installation

1. Clone the repository
```bash
git clone https://github.com/YOUR_USERNAME/devhero-ai-orchestrator.git
cd devhero-ai-orchestrator
```

2. Install dependencies
```bash
pip install -r requirements.txt
```

3. Configure environment variables
```bash
cp .env.example .env
# Edit .env with your API keys
```

4. Run the application
```bash
streamlit run app.py
```

## 📋 Configuration

Create a `.env` file with the following variables:
```env
# LLM Configuration
DEVZERO_LLM_MODEL=deepseek-chat
DEEPSEEK_API_KEY=your_api_key_here
DEEPSEEK_BASE_URL=https://api.deepseek.com/v1
DEVZERO_TEMPERATURE=0.3

# GitHub Integration (Optional)
GITHUB_REPO=https://github.com/username/repo
GITHUB_TOKEN=your_github_token
GITHUB_BRANCH=main
```

## 🎯 Usage

1. **Describe Your Requirement**
   - Enter a natural language description of what you want to build
   - Example: "Create a login page with React frontend and Spring Boot backend"

2. **Review the Plan**
   - DevHero's manager agent analyzes your request
   - Creates an optimized multi-agent execution plan
   - Optionally refine the plan with feedback

3. **Execute Phase-by-Phase**
   - Each agent executes its specialized task
   - Review output and approve before continuing
   - Download code or push to GitHub

## 🏗️ Architecture
```
User Input → Manager Agent → Dynamic Plan → Specialized Agents → Output
                ↑                                    ↓
                └────────── Human Approval ─────────┘
```

## 📸 Screenshots

[Add screenshots of your UI here]

## 🛠️ Tech Stack

- **Frontend**: Streamlit
- **AI Framework**: CrewAI
- **LLM**: DeepSeek (configurable)
- **Version Control**: GitPython
- **Language**: Python 3.8+

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the project
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built with [CrewAI](https://github.com/joaomdmoura/crewAI)
- Powered by [Streamlit](https://streamlit.io)
- LLM capabilities via DeepSeek/OpenAI

## 📧 Contact

Your Name - [@yourtwitter](https://twitter.com/yourtwitter)

Project Link: [https://github.com/YOUR_USERNAME/devhero-ai-orchestrator](https://github.com/YOUR_USERNAME/devhero-ai-orchestrator)

## ⭐ Star History

If you find this project useful, please consider giving it a star!
```

### Additional Repository Files

**.gitignore**
```
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
ENV/
build/
dist/
*.egg-info/

# Streamlit
.streamlit/

# Environment
.env
.env.local

# Cache
repo_cache/
*.zip

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db
```

**requirements.txt**
```
streamlit>=1.28.0
python-dotenv>=1.0.0
gitpython>=3.1.40
crewai>=0.1.0
```

**.env.example**
```
# LLM Configuration
DEVZERO_LLM_MODEL=deepseek-chat
DEEPSEEK_API_KEY=your_api_key_here
DEEPSEEK_BASE_URL=https://api.deepseek.com/v1
DEVZERO_TEMPERATURE=0.3

# GitHub Integration (Optional)
GITHUB_REPO=https://github.com/username/repo
GITHUB_TOKEN=your_github_token
GITHUB_BRANCH=main
```

### GitHub Repository Settings

**Topics/Tags** (add these in GitHub settings):
```
ai, machine-learning, automation, crewai, streamlit, 
multi-agent, code-generation, devops, workflow-automation,
human-in-the-loop, llm, deepseek, ai-agents
```

**About Section** (short description):
```
🤖 AI-powered multi-agent workflow automation with human-in-the-loop approval and GitHub integration
