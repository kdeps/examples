# Agents

This document describes the available agents and their capabilities within the context of this Kdeps examples project.

## Project Context

This repository contains example projects built with Kdeps, a framework for creating AI-powered APIs. The examples include:
- **tools**: MCP-like API with LLM tool selection
- **vision**: Vision model API using moondream
- **ai_ocr_api**: OCR + LLM processing with web interface
- **weather_forecast_ai**: Weather API with external service integration
- **whois**: Individual lookup API with web interface
- **huggingface_imagegen_api**: Image generation using Hugging Face models

## Agent Types

### General Purpose Agent
- **Description**: Handles complex, multi-step tasks autonomously
- **Tools**: All available tools
- **Project Relevance**: 
  - Analyze and modify workflow.pkl files
  - Research LLM configurations across different examples
  - Implement new features across multiple projects
  - Debug API endpoints and their integrations

### Statusline Setup Agent
- **Description**: Configures Claude Code status line settings
- **Tools**: Read, Edit
- **Project Relevance**: 
  - Configure development environment for Kdeps projects
  - Set up status indicators for API development

### Output Style Setup Agent
- **Description**: Creates Claude Code output styles
- **Tools**: Read, Write, Edit, Glob, LS, Grep
- **Project Relevance**: 
  - Customize output formatting for API responses
  - Style JSON output across different example projects

## Project-Specific Use Cases

### Multi-Example Analysis
Use the **General Purpose Agent** when you need to:
- Compare implementations across different example projects
- Find patterns in how different APIs handle LLM integration
- Analyze resource configurations (*.pkl files) across projects

### API Development Tasks
Use agents for:
- Adding new endpoints to existing examples
- Implementing web interfaces for CLI-only examples
- Integrating new LLM models or external services
- Creating new example projects following existing patterns

### Workflow Management
Leverage agents to:
- Understand and modify Kdeps workflow configurations
- Trace data flow through the exec.pkl → llm.pkl → response.pkl pipeline
- Debug resource dependencies and execution flows

## Usage Guidelines

- Launch multiple agents concurrently when possible for better performance
- Each agent invocation is stateless
- Provide detailed task descriptions for autonomous execution
- Specify whether the agent should write code or perform research
- Use specialized agents when tasks match their descriptions
- Consider the Kdeps framework context when planning multi-step tasks