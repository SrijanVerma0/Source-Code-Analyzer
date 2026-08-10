# RealTime Source Code Analyzer

An automated Git repository ingestion and RAG-based codebase analyzer. This tool clones any GitHub repository locally, processes its Python source code files into semantic vectors, and allows you to chat dynamically to analyze the project's logic and architecture in real-time.

## Features

- **Automated Git Clone**: Directly fetch codes using a GitHub URL via the frontend.
- **Semantic Chunking**: Intelligent code splitting tailored explicitly for Python scripts using Langchain Text Splitters.
- **RAG Architecture**: Highly available vectorized document interactions run atop ChromaDB and OpenRouter generative LLMs.
- **Cross-Platform Compatibility**: Fully compatible with Linux, macOS, and Windows.

---

## 🛠 Prerequisites

Before starting, ensure you have:
- [Python 3.10+](https://www.python.org/downloads/)
- [Git](https://git-scm.com/downloads) installed and added to sys path.
- An API Key from **OpenRouter**.

---

## 🚀 Quick Setup & Installation

Follow these steps exactly to run the workspace seamlessly using `uv` (recommended for ultra-fast environments):

### 1. Clone the Source Code Analyzer Repository
```bash
git clone <your-repo-url-here>
cd Source-Code-Analyzer
```

### 2. Create and Activate Virtual Environment
```bash
# Create venv using uv
uv venv

# Activate (Windows)
.venv\Scripts\activate

# Activate (Mac/Linux)
source .venv/bin/activate
```

### 3. Install Dependencies
All dependencies are cleanly pinned to the modern Langchain standard (v0.2+). Wait for installation to finish:
```bash
uv pip install -r requirements.txt
```

### 4. Configure Ecosystem Variables
Create a file named `.env` in the root folder of this project, and paste your OpenRouter API Key inside it.
```env
OPENROUTER_API_KEY="sk-or-v1-xxxxxxxxxxxxxxxxxxxxx..."
```

---

## 🖥 Target Usage

Running the application takes two seamless steps:

**Start the Flask Server:**
```bash
python app.py
```
Open `http://localhost:8080` in your web browser.

**Execution Flow in Browser:**
1. **Ingest Repo**: Type/Paste an external Github Repositiory URL into the input initially, and it will trigger cloning and indexing into the local `db/` folder via Vector Store. 
2. **Chat & Retrieve**: Once indexing finishes, chat normally. The analyzer retrieves architectural chunks and responds contextually based on the downloaded source code.

> **Note**: To wipe the scraped data locally, type `clear` in the Chat UI. This executes a fast reset and clears the cloned git index.

---

## 🧩 Architectural Fixes Note
Recently, the project has been aggressively migrated to `langchain=0.2+` standalone modular structures (`langchain-core`, `langchain-community`, `langchain-openai`, `langchain-classic`, `langchain-text-splitters`) resolving breaking syntax anomalies out-of-the-box. Running `pip install -r requirements.txt` now natively guarantees zero legacy compatibility issues.