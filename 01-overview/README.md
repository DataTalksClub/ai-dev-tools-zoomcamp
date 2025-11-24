# Module 1 — Introduction to Vibe Coding  

[▶️ Watch the Workshop Video](https://www.youtube.com/watch?v=NSMXQk4Axig&list=PL3MmuxUbc_hLuyafXPyhTdbF4s_uNhc43)


## Overview 

This module introduces participants to modern AI development tooling, showing how different categories of tools can enhance developer's experience. 

- Chat Applications: great for exploration and brainstorming, but less convenient for iterative development.  
- Coding Assistants / IDE Integrations: help write, refactor, and test code directly inside development environments.  
- Project Bootstrappers: generate starter projects quickly from natural language prompts.  
- Agents: more advanced systems that can operate across files, perform tool-based actions, and automate workflows.  


## Snake Game and Chat Applications

Developing the snake game with ChatGPT and Claude

Chat apps allow quick Q&A and prototyping but often require switching between the chat and IDE.  

- [ChatGPT](https://chatgpt.com/) — General-purpose LLM with strong coding abilities.  
- [Claude](https://claude.ai/) — AI assistant by Anthropic, strong on reasoning and long context handling.  
- [DeepSeek](https://www.deepseek.com/en) — Open-source, performance-optimized LLM for coding and analysis.  
- [Ernie](https://ernie.baidu.com/) — Baidu’s large model platform.  
- [Microsoft Copilot](https://copilot.microsoft.com/) — Microsoft’s general AI assistant (distinct from GitHub Copilot).  



## AI Coding Assistants / IDE Integrations  

These tools are embedded into editors/IDEs to provide inline code suggestions, test generation, multi-file edits, and more.  

- [Claude Code](https://www.anthropic.com/claude-code) — Command-line + IDE companion for AI-powered coding.  
	```bash
	npm install -g @anthropic-ai/claude-code
	```  
- [GitHub Copilot](https://github.com/features/copilot) — GitHub’s AI coding partner integrated into IDEs like VS Code, JetBrains.  
- [Cursor](https://cursor.com/) — An AI-first IDE built around coding with LLMs.  
- [Pear](https://trypear.ai/) — Open-Source AI Assistant.  

## 3. Project Bootstrappers  

Bootstrappers generate entire project from natural language prompts. Useful for quick prototyping.  

- [Bolt.new](https://bolt.new/) — Generate full-stack applications quickly.  
- [Lovable.dev](https://lovable.dev/) — Create applications from prompts with frontend/UI focus.  

## 4. Agents  

Agents are autonomous coding helpers that combine LLMs with tools to read/write files, run commands, and manage projects.  
They form the backbone of many assistants and scaffolders.  

- [Anthropic Computer Use](https://github.com/anthropics/anthropic-quickstarts/tree/main/computer-use-demo) — Demonstration of agents that can interact with computers and files.  
	```bash
	docker run \
		-e ANTHROPIC_API_KEY=$ANTHROPIC_API_KEY \
		-v $HOME/.anthropic:/home/computeruse/.anthropic \
		-p 5900:5900 \
		-p 8501:8501 \
		-p 6080:6080 \
		-p 8080:8080 \
		-it ghcr.io/anthropics/anthropic-quickstarts:computer-use-demo-latest
	```  
- [PR Agent](https://github.com/qodo-ai/pr-agent) — Automates pull request reviews and suggestions.



## Community notes

Did you take notes? You can share them here

* Add a link to your notes above this line

