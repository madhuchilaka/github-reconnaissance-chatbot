# AI-Powered GitHub Reconnaissance Chatbot

An AI-assisted GitHub reconnaissance system designed for **authorized analysis of public GitHub repositories**.

The project combines **GitHub REST API**, **MCP**, **FastAPI**, and an **AI agent** to collect repository intelligence, analyze technologies and exposed domains/APIs, identify security indicators, and present reconnaissance results through APIs and a React-based chat interface.

---

## 🚀 Project Overview

The AI-Powered GitHub Reconnaissance Chatbot provides a structured reconnaissance workflow for GitHub repositories.

Instead of allowing the AI to directly interact with GitHub, the system separates responsibilities into multiple layers:

1. React Frontend
2. FastAPI Backend
3. AI Agent
4. MCP Client
5. GitHub MCP Server
6. GitHub REST API

This architecture keeps GitHub operations structured and separates external API interaction from AI reasoning.

---

## 🏗️ System Architecture

```text
┌──────────────────────────┐
│      React Frontend      │
│       Chat Interface     │
└────────────┬─────────────┘
             │
             ▼
┌──────────────────────────┐
│       FastAPI API        │
│ /chat /recon /tools      │
└────────────┬─────────────┘
             │
             ▼
┌──────────────────────────┐
│        AI Agent          │
│  Reasoning + Tool Calls  │
└────────────┬─────────────┘
             │
             ▼
┌──────────────────────────┐
│        MCP Client        │
└────────────┬─────────────┘
             │
             ▼
┌──────────────────────────┐
│     GitHub MCP Server    │
│      Reconnaissance      │
│          Tools           │
└────────────┬─────────────┘
             │
             ▼
┌──────────────────────────┐
│     GitHub REST API      │
└──────────────────────────┘
```

---

## ✨ Main Features

### GitHub Reconnaissance

- GitHub repository discovery
- Repository metadata collection
- Repository tree retrieval
- Git blob retrieval
- Branch collection
- Commit collection
- Pull-request collection
- Contributor collection
- Release collection

### Repository Analysis

- File detection
- Technology detection
- Domain extraction
- API endpoint extraction
- Security indicator detection
- Repository reconnaissance analysis

### Security Analysis

- Security indicator detection
- Sensitive-looking value detection
- Secret redaction
- Security finding classification
- Finding relationship handling
- Evidence preservation
- Finding status tracking
- SQLite persistence

### AI and MCP

- AI-assisted reconnaissance workflow
- MCP-based GitHub tools
- Structured tool execution
- Tool argument validation
- MCP result serialization
- Safe tool-error handling
- Structured reconnaissance results

### Web Application

- FastAPI backend
- React frontend
- Chat interface
- Repository analysis API
- Tool execution API
- Health-check API

### Testing

- Unit tests
- Service-level tests
- API tests
- MCP tests
- AI integration tests
- Security pipeline tests
- Error-handling tests

---

## 🛠️ Technology Stack

### Backend

- Python 3.13+
- FastAPI
- Pydantic
- HTTPX
- SQLite
- Pytest

### AI

- OpenAI API
- OpenAI Responses API
- MCP

### GitHub Integration

- GitHub REST API
- GitHub authentication through environment variables

### Frontend

- React
- ReactDOM
- Vite
- ESLint

---

## 📁 Project Structure

```text
github-recon-chatbot/
│
├── app/
│   ├── ai/
│   ├── api/
│   ├── config/
│   ├── github/
│   ├── mcp/
│   ├── recon/
│   ├── security/
│   └── ...
│
├── data/
│
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── App.jsx
│   │   ├── api.js
│   │   └── ...
│   ├── package.json
│   └── vite.config.js
│
├── tests/
│
├── .env
├── .gitignore
├── pytest.ini
├── requirements.txt
├── github_manual_test.py
├── ai_mcp_manual_test.py
└── README.md
```

> The internal module structure may evolve as the project is extended.

---

## ⚙️ Setup & Installation

### 1. Clone the Repository

```powershell
git clone <your-repository-url>
cd github-recon-chatbot
```

### 2. Create the Python Virtual Environment

```powershell
python -m venv .venv
```

Activate the virtual environment on Windows:

```powershell
.venv\Scripts\Activate.ps1
```

### 3. Install Backend Dependencies

```powershell
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file in the project root:

```env
GITHUB_TOKEN=your_github_token
OPENAI_API_KEY=your_openai_api_key
```

Never commit `.env` or expose API credentials.

### 5. Install Frontend Dependencies

Open another terminal and navigate to the frontend directory:

```powershell
cd frontend
npm install
```

---

## ▶️ Running the Application

### Start the Backend

From the project root:

```powershell
uvicorn app.api.main:app --reload
```

### Start the Frontend

From the `frontend` directory:

```powershell
npm run dev
```

The frontend communicates with the FastAPI backend through the configured API endpoints.

---

## 🔌 API Endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| `GET` | `/health` | Check backend health |
| `POST` | `/tools/execute` | Execute a registered reconnaissance tool |
| `POST` | `/recon/analyze` | Analyze a GitHub repository |
| `POST` | `/chat` | Interact with the AI reconnaissance chatbot |

### Health Check

```http
GET /health
```

Used to verify that the FastAPI backend is running.

### Tool Execution

```http
POST /tools/execute
```

Provides access to the registered GitHub reconnaissance tools through the backend API.

### Repository Analysis

```http
POST /recon/analyze
```

Runs the repository reconnaissance and analysis workflow for a GitHub repository.

### AI Chat

```http
POST /chat
```

Provides the chatbot interface for AI-assisted GitHub reconnaissance.

---

## 🔍 Reconnaissance Workflow

The reconnaissance workflow follows a structured process for collecting and analyzing information from an authorized GitHub repository.

```text
Repository Input
       │
       ▼
Repository Metadata Collection
       │
       ▼
Repository Tree Collection
       │
       ▼
Git Blob / File Retrieval
       │
       ▼
Repository Analysis
       │
       ├── File Detection
       │
       ├── Technology Detection
       │
       ├── Domain Extraction
       │
       ├── API Extraction
       │
       └── Security Indicator Detection
       │
       ▼
Security Analysis
       │
       ├── Secret Redaction
       ├── Finding Classification
       └── Evidence Preservation
       │
       ▼
Structured Reconnaissance Result
```

### Collection Phase

The system collects repository information including:

- Repository metadata
- Repository tree
- Git blobs
- Branches
- Commits
- Pull requests
- Contributors
- Releases

### Analysis Phase

Collected repository data is analyzed to identify:

- Files and file types
- Technologies and frameworks
- Domains
- API endpoints
- Security indicators

### Security Analysis Phase

Security-related indicators are processed through the security pipeline.

The pipeline can:

- Detect sensitive-looking values
- Redact sensitive-looking values
- Preserve useful evidence
- Create structured findings
- Classify findings
- Track finding relationships and status

### Result Phase

The collected and analyzed information is returned as a structured reconnaissance result that can be consumed by the FastAPI API, MCP tools, and AI agent.

---

## 🤖 AI + MCP Architecture

The project uses the **Model Context Protocol (MCP)** to provide a structured interface between the AI agent and GitHub reconnaissance capabilities.

```text
┌──────────────────────┐
│       AI Agent       │
│ Reasoning + Planning │
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│      MCP Client      │
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│   GitHub MCP Server  │
│                      │
│  ┌────────────────┐  │
│  │ Repository     │  │
│  │ Search         │  │
│  ├────────────────┤  │
│  │ Repository     │  │
│  │ Metadata       │  │
│  ├────────────────┤  │
│  │ Contents       │  │
│  ├────────────────┤  │
│  │ Code Search    │  │
│  ├────────────────┤  │
│  │ File Retrieval │  │
│  ├────────────────┤  │
│  │ Commits        │  │
│  ├────────────────┤  │
│  │ Branches       │  │
│  ├────────────────┤  │
│  │ Pull Requests  │  │
│  ├────────────────┤  │
│  │ Contributors   │  │
│  ├────────────────┤  │
│  │ Releases       │  │
│  └────────────────┘  │
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│   GitHub REST API    │
└──────────────────────┘
```

### AI Agent

The AI agent is responsible for:

- Understanding reconnaissance requests
- Selecting appropriate tools
- Preparing tool arguments
- Processing structured tool results
- Continuing the reconnaissance workflow
- Producing a structured response

### MCP Client

The MCP client provides the communication layer between the AI agent and the GitHub MCP server.

### GitHub MCP Server

The MCP server exposes GitHub reconnaissance capabilities as structured tools.

The server separates GitHub API operations from the AI reasoning layer.

### Tool Execution

Tool execution includes validation and error handling so that malformed arguments and tool failures do not directly expose raw exceptions to the AI layer.

### Structured Results

MCP tool results are serialized into structured data before being passed between system components. This keeps the communication boundary predictable and easier to test.

---

## 🔐 Security Design

Security is an important part of the reconnaissance pipeline. Repository content is treated as **untrusted input** throughout the analysis process.

The security pipeline is designed to identify security-related indicators while reducing the risk of exposing sensitive-looking values.

### Security Pipeline

```text
Repository Data
       │
       ▼
Security Indicator Detection
       │
       ▼
Sensitive-Value Identification
       │
       ▼
Secret Redaction
       │
       ▼
Evidence Preservation
       │
       ▼
Finding Classification
       │
       ▼
Finding Relationships / Status
       │
       ▼
Persisted Security Finding
```

### Security Capabilities

The security pipeline supports:

- Security indicator detection
- Sensitive-looking value detection
- Secret redaction
- Security finding creation
- Finding classification
- Evidence preservation
- Finding relationship handling
- Finding status transitions
- SQLite persistence

### Untrusted Repository Content

Repository files, code, comments, configuration files, commit messages, and other collected content are treated as untrusted data.

The system does not assume that repository content is trustworthy simply because it is returned by GitHub.

### Secret Handling

Sensitive-looking values are processed through the security pipeline rather than being treated as confirmed credentials.

The system is designed to preserve useful evidence while reducing unnecessary exposure of sensitive values.

### Human Review

Security findings generated by the system are **indicators for investigation**, not automatically confirmed vulnerabilities.

Human review is required before treating a finding as a confirmed security issue.

---

## 🧪 Testing & Quality

The project includes an automated test suite covering the major components of the reconnaissance system.

### Backend Testing

Run the complete backend test suite from the project root:

```powershell
pytest -q
```

The test suite covers areas including:

- GitHub API client behavior
- GitHub API error handling
- Tool registration and execution
- Tool validation and dispatching
- Repository reconnaissance
- Repository analysis
- Security analysis
- Security finding persistence
- MCP server tools
- MCP result serialization
- AI tool execution
- AI tool-result serialization
- AI error handling
- FastAPI API endpoints
- Reconnaissance error propagation

### Frontend Testing

The frontend project includes linting and production-build validation.

Run frontend linting:

```powershell
npm run lint --prefix frontend
```

Run the production build:

```powershell
npm run build --prefix frontend
```

### Quality Checks

The project uses automated testing and validation to help ensure:

- Components behave as expected
- API errors are handled safely
- Invalid tool arguments are rejected
- MCP results remain structured
- Repository collection failures are not silently converted into empty results
- Security findings remain structured and reviewable
- Frontend code passes linting
- The React application can be built successfully

---

## ⚠️ Current Limitations

### OpenAI API Availability

The AI chat functionality depends on an available OpenAI API quota or credit balance.

If the OpenAI API is unavailable, the backend returns a safe service-unavailable response instead of exposing raw provider errors.

### GitHub API Limits

GitHub API requests are subject to GitHub authentication, rate-limit, permission, and service-availability constraints.

### Repository Size

Large repositories can contain a substantial number of files and Git objects.

The reconnaissance workflow therefore uses Git tree and blob APIs to improve repository collection efficiency.

### Security Findings

Security indicators produced by the system are analysis results and should not automatically be considered confirmed vulnerabilities.

Human verification and review are required before treating a finding as a confirmed security issue.

---

## 🛡️ Responsible Use

This project is intended for **authorized GitHub reconnaissance and security-aware analysis**.

Use the system only against repositories and systems that you are authorized to analyze.

Do not use reconnaissance results to:

- Access unauthorized systems
- Access unauthorized accounts
- Use exposed credentials without authorization
- Bypass authentication or access controls
- Exploit vulnerabilities
- Perform unauthorized security testing

The purpose of this project is information gathering, analysis, and security-aware research within authorized environments.

---

## 🚀 Future Improvements

The project can be extended with additional reconnaissance, security analysis, and user-interface capabilities.

Potential future improvements include:

- Advanced AI-driven repository reasoning
- Expanded technology and framework detection
- Additional security-scanning integrations
- Gitleaks integration
- TruffleHog integration
- Semgrep integration
- Advanced security finding correlation
- More detailed reconnaissance dashboards
- Persistent reconnaissance history
- Advanced repository relationship analysis
- Additional MCP reconnaissance tools
- Improved visualization of reconnaissance results

These improvements can be introduced incrementally while maintaining the existing separation between the AI, MCP, GitHub API, security, and presentation layers.

---

## 📄 Project Information

**Project:** AI-Powered GitHub Reconnaissance Chatbot

**Primary Technologies:**

`Python` · `FastAPI` · `GitHub REST API` · `MCP` · `OpenAI` · `React` · `Vite`

The project is developed as an academic/personal project focused on AI-assisted GitHub reconnaissance and security-aware repository analysis.

---