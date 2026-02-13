Coreon × ERC-8004 Integration

An Execution-Level AI Agent with On-Chain Identity & Reputation

This document corresponds to the coreon-erc8004 branch

⸻

📌 Background

As an AI Execution Engine, Coreon MCP already provides:
	•	Multi-step ToolCall execution (Plan → Execute)
	•	Cross on-chain / off-chain tool orchestration
	•	Interaction interfaces via Telegram / CLI

However, in an open Agent ecosystem, execution capability alone is insufficient for secure collaboration:
	•	Agents lack verifiable on-chain identity
	•	Historical execution quality is not traceable
	•	Task delegation lacks a reputation-based trust mechanism

ERC-8004 introduces an on-chain standard for AI Agents, including:
	•	Identity
	•	Reputation
	•	Verifiable Feedback

This branch aims to explore and implement:

Upgrading Coreon into a discoverable, trustable, and delegatable on-chain execution Agent

⸻

🎯 Integration Goals

By integrating with ERC-8004, Coreon will achieve:
	1.	On-Chain Agent Registration (Identity)
	•	Coreon registers as an execution Agent in the ERC-8004 Registry
	•	Gains a discoverable on-chain identity and capability tags
	2.	Task Execution Receipt (Task Receipt)
	•	Each ToolCall execution generates a unique task_id
	•	A result summary is hashed (result_hash)
	•	The hash can be recorded on-chain for verification
	3.	On-Chain User Feedback (Feedback)
	•	Users can evaluate execution results (e.g. 👍/👎 or rating)
	•	Feedback is bound to the corresponding task_id
	4.	On-Chain Reputation Accumulation (Reputation)
	•	Feedback drives updates to Agent reputation
	•	Reputation serves as a reference for future task delegation and routing
	5.	Reputation-Based Agent Routing (Routing)
	•	In multi-Agent scenarios, Coreon can select the optimal executor based on on-chain reputation
	•	Or execute tasks itself when it is the best option

⸻

🏗 System Architecture (Logical Flow)

User Input
   │
   ▼
Coreon MCP Planner
   │
   ▼
Execution (ToolCalls)
   │
   ▼
Task Receipt Generator
   │
   ├── result_hash
   └── task_id
   ▼
ERC-8004 Feedback Registry
   │
   ▼
Reputation Update
   │
   ▼
Agent Router (subsequent task selection)


⸻

🧩 New Module Design
	•	erc8004_identity_client
	•	Agent registration / capability updates
	•	erc8004_reputation_client
	•	Read / submit user feedback
	•	Query Agent reputation
	•	task_receipt
	•	Generate execution receipt (task_id)
	•	Compute result summary hash (result_hash)
	•	agent_router
	•	Select execution Agent based on on-chain reputation (optional)

⸻

🔔 Event Definitions (Example)
	•	TaskExecuted(task_id, agent, result_hash)
	•	FeedbackSubmitted(task_id, rating)

⸻

🗺 Roadmap
	•	Coreon MCP Execution Engine
	•	ERC-8004 Agent Identity Registration
	•	Task Execution Receipt Generation (task_id)
	•	Result Summary Hash Recording
	•	On-Chain User Feedback
	•	Reputation Query Interface
	•	Reputation-Based Agent Routing (optional)

⸻

📎 Notes

This branch explores Coreon’s integration under the ERC-8004 standard,
combining execution capability with on-chain trust mechanisms,
and advancing the adoption of Agent-to-Agent (A2A) collaboration.

