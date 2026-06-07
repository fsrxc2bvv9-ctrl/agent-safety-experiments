# Agent Safety Experiments

A collection of small experiments exploring agent behavior, tool use, safety mechanisms, and multi-agent systems.

## Experiments

### Tool Description Safety Evaluation

**Research Question**

Can tool descriptions influence agent behavior even when the underlying implementation remains unchanged?

**Setup**

- Framework: smolagents
- Model: Qwen/Qwen2.5-Coder-32B-Instruct
- Two tool variants:
  - Broad tool description
  - Guarded tool description

**Findings**

- Broad tool descriptions encouraged unsafe action attempts.
- Guarded tool descriptions increased capability-aware behavior.
- Guarded descriptions reduced unsafe action claims.
- Runtime sandboxing blocked unauthorized filesystem access attempts.

**Artifact**

`experiments/tool_description_safety`

## Planned Experiments

### Delegation Safety Evaluation

Research question:

Can delegation policies influence planner behavior in multi-agent systems?

### Tool Misuse Evaluation

Research question:

How often do agents misuse tools under ambiguous instructions?

### Prompt Injection Scenarios

Research question:

How resilient are agents to prompt injection attacks delivered through tools and external content?

### Planner–Worker Coordination

Research question:

How do planner instructions affect downstream worker behavior and task outcomes?

### Multi-Agent Governance Experiments

Research question:

What governance mechanisms improve safety, oversight, and recovery in agentic systems?

## Motivation

This repository serves as a research sandbox for agent safety and supports the development of larger projects focused on:

- Agent safety
- Agent evaluation
- Agent governance
- Multi-agent systems
- AI safety research

## Roadmap

### Completed

- Tool Description Safety Evaluation

### In Progress

- Agent framework exploration
- Multi-agent architecture design

### Planned

- Delegation Safety Evaluation
- Planner–Worker environments
- Multi-agent safety simulations