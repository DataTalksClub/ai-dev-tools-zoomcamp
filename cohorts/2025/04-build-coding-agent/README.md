# Module 4 — Create a Coding Agent  

[▶️ Workshop Video](https://www.youtube.com/watch?v=Sue_mn0JCsY)  
[📹 Demo TODO App with Z-ai](https://www.loom.com/share/b4c47e3491504375b9244ea69fe095df)  

---

## Overview  

- Build your own **coding agent** that can scaffold and extend projects.  
- Use a **Django template** as the base project.  
- Learn how **agents act as project bootstrappers**.  
- Explore multiple **agent orchestration frameworks**.  
- Outcome: a Django app created and modified by your AI agent.  

---

## Prerequisites  

- Python 3.8+  
- Jupyter Notebook  
- OpenAI API key (required)  
- Anthropic API key (optional)  
- GitHub account (optional, for Codespaces)  

---

## Environment  

- Run locally with Python + Jupyter, or in **GitHub Codespaces**.  
- Configure API keys in environment variables or Codespaces secrets.  
- Install required libraries:  
	```bash
	pip install jupyter django uv openai toyaikit
	```  

---

## OpenAI API Recap  

- Review of **responses API** for system + user prompts.  
- Function calling: extend model with custom Python functions.  
- Prepares for agent tool integration.  

---

## Django Template Project  

- Use a prebuilt **Django template repo** or create one from scratch.  
- Add `Makefile` for install/migrate/run commands.  
- Create templates (`base.html`, `home.html`) with TailwindCSS + Font Awesome.  

---

## Building the Agent  

- Define tools: read/write files, execute shell commands, search files, view file tree.  
- Create a **developer prompt** describing the Django project.  
- Run agent using [ToyAIKit](https://github.com/alexeygrigorev/toyaikit).  

---

## Alternative Frameworks  

- **OpenAI Agents SDK** — define tools with `@function_tool`, run with `OpenAIAgentsSDKRunner`.  
- **PydanticAI** — lightweight agent library with tool support, easy provider switching.  
- **Z.ai** — OpenAI-compatible API with alternative LLMs.  

---

## Learning Outcomes  

- Understand how coding agents function as **intelligent project bootstrapper tools**.  
- Gain practical experience in setting up **Django with AI assistance**.  
- Learn to integrate **tools into agents** across multiple frameworks.  
- Build agents that can adapt to different **LLM providers**.  
