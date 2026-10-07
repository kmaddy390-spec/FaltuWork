# Pre-Meeting Prep: Everything You Need to Know
## ACXD + CIGNA POC — One Document to Rule Them All
**Read time: ~15 minutes | For: Madhav's call with Charit**

---

# PART 1: ACXD — The Tool We'll Build With

---

## What is ACXD?

ACXD = **Agentic CX Designer**

It's a **drag-and-drop canvas** inside Amazon Connect where you design AI-powered customer service bots — without writing code.

**Simple analogy:** Imagine making a flowchart in PowerPoint, but each box actually DOES something — one box talks to the customer, another checks a database, another uses AI to understand what they want.

---

## Why "Agentic"?

A regular chatbot follows a fixed script. An **agentic** bot can:
- **Think** — understand what the customer actually means, even if they say it in a weird way
- **Plan** — break a complex request into steps
- **Act** — call APIs, search documents, update accounts
- **Decide** — choose what to do next based on the situation
- **Escalate** — hand off to a human when it's stuck

---

## The Two Types of Building Blocks

Everything in ACXD is built with **nodes** (boxes on the canvas). There are two flavors:

### Deterministic Nodes = Fixed Rules
These do exactly what you tell them. No AI, no guessing.

**When to use:** When the answer MUST be exact.

| Node | What It Does | Example |
|------|-------------|---------|
| Message | Shows/says a fixed message | "Welcome to CIGNA support" |
| Data Request | Collects specific info with validation | "Enter your policy number" |
| Condition | If-this-then-that logic | If policy active → Path A, else → Path B |
| API Call | Calls a backend system | Check claim status in database |
| Transfer | Send to human agent | Route to live agent with full context |

### Agentic AI Nodes = Smart AI
These use AI (LLMs) to think, understand, and respond naturally.

**When to use:** When the conversation could go many ways and needs flexibility.

| Node | What It Does | Example |
|------|-------------|---------|
| Generative AI | Free-form conversation using AI | "Tell me about your issue" — AI handles it |
| Knowledge Base | Search company docs for answers (RAG) | Look up CIGNA's coverage policy from PDFs |
| Tool Use (MCP) | AI decides which API to call | AI figures out it needs the claims API |
| Guardrail | Safety filter around AI responses | Block PII, keep AI on-topic |

### The Golden Rule
> **Use deterministic nodes for things that MUST be exact** (authentication, compliance, payments).  
> **Use AI nodes for things that need flexibility** (understanding questions, troubleshooting, explaining policies).

---

## How ACXD Connects to Amazon Connect

```
Customer calls/chats
        ↓
Amazon Connect (contact flow)
        ↓
Agentic CX Block  ← This is the bridge
        ↓
ACXD Application (your flow runs here)
```

The **Agentic CX Block** is a special block in the Amazon Connect contact flow that says "now hand this conversation over to my ACXD application."

---

## Key ACXD Features You Should Know

### 1. Knowledge Bases (RAG)
- Connects to company documents (PDFs, FAQs, policies)
- AI searches these docs first, then generates an answer based on what it found
- This prevents the AI from making things up

### 2. Guardrails
- Safety rules that wrap around the AI
- Block sensitive topics, prevent PII leaks, enforce company policies
- Think of it as invisible walls the AI can't cross

### 3. A2A (Agent-to-Agent)
- Multiple AI agents can collaborate during one conversation
- Example: Main agent talks to customer, silently asks a fraud agent to check risk in the background

### 4. Live Sync
- AI can control the customer's web/mobile screen during a call
- Currently in preview

### 5. Omnichannel
- Same flow works for voice, chat, SMS, and email
- Build once, deploy everywhere

---

## Deployment — Important Gotcha

> **ACXD does NOT use CloudFormation or regular Connect APIs.**  
> It has its own SDK: `amazon-connect-acxd-sdk`  
> Keep this in mind when Charit discusses deployment.

---

---

# PART 2: The AWS Services in the CIGNA Flow

---

Each box in the CIGNA Draw.io flow uses a specific AWS service. Here's what each one does:

## 1. Amazon Connect
**What:** Cloud contact center — handles phone calls and chat messages  
**Role in CIGNA flow:** Entry point — the customer contacts CIGNA through this  
**Think of it as:** The phone system + chat system combined  
**Supports:** Voice and Chat (both channels are in scope for this POC)

## 2. AWS Lambda
**What:** Serverless functions — small pieces of code that run on-demand  
**Role in CIGNA flow:** Handles authentication — verifies the customer's identity  
**Think of it as:** A bouncer that checks your ID before letting you in  
**How it works:** Customer gives policy number → Lambda checks the database → confirms identity  
**Key point:** No servers to manage. Lambda runs, does its job, stops. You only pay when it runs.

## 3. Amazon Lex
**What:** Conversational AI service — understands spoken/typed language  
**Role in CIGNA flow:** Listens to what the customer says and figures out their intent  
**Think of it as:** The ears and initial brain of the system

**Three key Lex concepts:**

| Term | What It Means | Example |
|------|-------------|---------|
| **Intent** | What the customer wants to DO | "CheckClaimStatus", "AskCoverage", "FileComplaint" |
| **Slot** | The specific DETAILS needed | Policy number, date of birth, claim ID |
| **Utterance** | The actual WORDS the customer says | "What's happening with my claim?", "I want to check my coverage" |

**How it works:**  
Customer says → "I want to know about my claim"  
Lex identifies → Intent: CheckClaimStatus  
Lex asks → "What's your claim number?" (collecting the Slot)

## 4. Amazon Bedrock (LLM)
**What:** AWS's AI platform — gives you access to powerful AI models  
**Role in CIGNA flow:** The brain — understands complex questions, generates human-like answers  
**Think of it as:** The ChatGPT-like intelligence behind the system

**Available models:**
- **Claude** (by Anthropic) — very good at reasoning and following instructions
- **Amazon Titan** — Amazon's own model
- **Llama** (by Meta) — open-source model
- You can choose which model to use based on your needs

**Used in two places in the CIGNA flow:**
1. **Step 3c** — Helps identify the customer's intent (understanding complex questions)
2. **Step 6b** — Generates the final natural-language answer

## 5. Amazon Kendra (RAG)
**What:** Intelligent document search service  
**Role in CIGNA flow:** Searches through CIGNA's documents (policies, FAQs, coverage info) to find relevant answers  
**Think of it as:** A super-smart search engine that actually reads and understands your documents

**How RAG works (step by step):**
```
BEFORE the conversation (Document Ingestion):
PDF documents → Upload to S3 bucket → Kendra reads them
→ Breaks into chunks → Indexes them (makes them searchable)

DURING the conversation (Retrieval):
Customer asks a question
→ Kendra searches through indexed documents
→ Finds the most relevant chunks
→ Sends them to Bedrock LLM
→ LLM generates a natural answer based on those chunks
```

**Why RAG matters:**
- Without RAG: AI might make up answers (hallucinate)
- With RAG: AI only answers based on actual CIGNA documents = accurate answers

## 6. Amazon OpenSearch
**What:** Search and analytics engine  
**Role in CIGNA flow:** Searches through structured data (claims, accounts, etc.)  
**Think of it as:** A fast database search

**Kendra vs OpenSearch — what's the difference?**

| | Kendra | OpenSearch |
|---|--------|-----------|
| **Searches** | Documents (PDFs, FAQs, policies) | Structured data (databases, logs) |
| **Best for** | "What does my policy cover?" | "What's the status of claim #12345?" |
| **Type** | Unstructured text search | Structured data search |

Both are used in the CIGNA flow — Kendra for document-based answers, OpenSearch for data lookups.

---

---

# PART 3: The CIGNA Flow — Step by Step

---

## The Big Picture — Three Stages

```
Stage 1: INGESTION (happens beforehand)
  CIGNA PDFs → S3 → Kendra indexes them

Stage 2: UNDERSTANDING (during conversation)  
  Customer speaks → Connect → Auth → Lex → Bedrock understands intent

Stage 3: ANSWERING (during conversation)
  Fulfillment → OpenSearch/Kendra find info → Bedrock generates answer
```

## Detailed Flow

### Step ① — Customer Contacts (Amazon Connect)
- Customer either **calls** or **chats** with CIGNA
- Amazon Connect receives the interaction
- Both **voice and text** channels are in scope

### Step ② — Authentication (Lambda + Database)
- **2a:** A Lambda function is triggered
- **2b:** Lambda checks the customer's identity against a database
- Could be: policy number + date of birth verification
- This is a **deterministic step** — fixed rules, no AI guessing

### Step ③ — Understanding the Customer (Lex + AI + Bedrock)
- **3a — Lex** listens to what the customer said (converts speech to text if voice)
- **3b — AI Intent Identifier** figures out what the customer wants
- **3c — Bedrock LLM** helps understand complex or unclear requests
- Output: The system now knows the customer's **intent** (e.g., "check claim status")

### Step ④ — Fulfillment
- The system now acts on the identified intent
- Triggers the right process to get the answer
- Think of it as the "let me look that up" moment

### Step ⑤ — Data Search (OpenSearch)
- Searches through structured data (claims, accounts, policy details)
- Returns specific data points (claim status, coverage details, etc.)

### Step ⑥ — AI Answer Generation (FAQ AI Agent + Kendra + Bedrock)
- **6c — Kendra RAG** searches through CIGNA's documents for relevant info
- **6a — FAQ AI Agent** takes all the retrieved info and processes it
- **6b — Bedrock LLM** generates a natural, human-like response
- The answer is delivered back to the customer

### Bonus — Live Agent Escalation (In Scope)
- If the AI can't handle the question → transfer to a real person
- Full conversation context is passed (transcript + summary)
- The human agent doesn't start from scratch

---

## How This CIGNA Flow Maps to ACXD

This is important — Govinde wants to **build this using ACXD**:

| CIGNA Flow Step | ACXD Node Type | Why |
|----------------|---------------|-----|
| Amazon Connect entry | Contact Flow → Agentic CX Block | Bridge to ACXD |
| Authentication (Lambda + DB) | **Deterministic** — Data Request / API Call | Must be exact, no AI guessing |
| Lex (understanding speech) | **Agentic AI** — Generative Journey node | Needs flexibility for natural language |
| Bedrock (intent identification) | Built into agentic nodes automatically | ACXD uses Bedrock under the hood |
| Fulfillment | **Deterministic** — Condition + API Call | Follow fixed logic based on intent |
| OpenSearch (data lookup) | **Deterministic** — Data Request node | Exact data retrieval |
| Kendra RAG (document search) | **Agentic AI** — Knowledge Base node | Search docs and generate answers |
| Bedrock (answer generation) | Built into Knowledge Base node | ACXD handles this automatically |
| Live Agent escalation | **Deterministic** — Transfer node | Route to human with full context |

---

---

# PART 4: RAG Deep Dive (You'll Definitely Be Asked About This)

---

## What is RAG?

**RAG = Retrieval-Augmented Generation**

In simple terms:
1. **Retrieval** — First, search for relevant information from real documents
2. **Augmented** — Add that information to the AI's context
3. **Generation** — Then let the AI generate an answer based on what it found

## Why Not Just Use AI Without RAG?

| Without RAG | With RAG |
|------------|----------|
| AI answers from memory (training data) | AI answers from your actual documents |
| Might make things up (hallucinate) | Answers based on real, verified content |
| Can't know company-specific info | Knows your exact policies, FAQs, products |
| Outdated information | As current as your latest documents |

## RAG in the CIGNA Flow

```
CIGNA Policy PDFs
    ↓
Upload to S3 Bucket
    ↓
Amazon Kendra reads them
    ↓
Breaks into small chunks (paragraphs/sections)
    ↓
Indexes chunks (makes them searchable)
    ↓
--- READY TO USE ---
    ↓
Customer asks: "Does my plan cover dental?"
    ↓
Kendra searches indexed chunks
    ↓
Finds relevant chunks about dental coverage
    ↓
Sends chunks to Bedrock LLM
    ↓
Bedrock reads chunks and generates:
"Yes, your CIGNA PPO plan includes dental coverage
 for preventive care. Cleanings and checkups are
 covered at 100%. Major procedures are covered at 50%
 after your deductible."
```

---

---

# PART 5: Key Terms Cheat Sheet

---

| Term | What It Means | One-Line Example |
|------|-------------|-----------------|
| **ACXD** | Agentic CX Designer — the visual tool to build AI bots | The canvas where you design the flow |
| **RAG** | Search docs first, then AI writes the answer | Prevents AI from making things up |
| **LLM** | Large Language Model — AI that understands/generates text | Like ChatGPT behind the scenes |
| **Intent** | What the customer wants to do | "CheckClaimStatus" |
| **Slot** | Details needed to fulfill the intent | Policy number, claim ID |
| **Utterance** | Actual words the customer says | "What's my claim status?" |
| **Bedrock** | AWS's AI platform with multiple models | Where Claude/Titan models live |
| **Kendra** | Smart document search service | Reads PDFs, finds answers |
| **Lex** | Conversation engine — understands speech/text | Ears of the system |
| **Lambda** | Serverless code that runs on-demand | Authentication checker |
| **OpenSearch** | Fast search engine for structured data | Look up claim #12345 |
| **Guardrails** | Safety rules around AI | "Don't share credit card numbers" |
| **MCP** | Model Context Protocol — how AI discovers tools | AI finds the right API to call |
| **A2A** | Agent-to-Agent collaboration | Multiple AI agents working together |
| **Node** | A single step/block on the ACXD canvas | One box in the flowchart |
| **Deterministic** | Fixed rules, predictable outcome | If X then Y, always |
| **Agentic** | AI-powered, flexible, can reason | AI decides what to do |
| **POC** | Proof of Concept — a trial build | Build a small version to test it works |
| **Chunking** | Breaking big docs into small pieces | So AI can search them efficiently |
| **Indexing** | Organizing chunks for fast search | Like a book's table of contents |
| **Fulfillment** | The step where the system acts on the request | "Let me look that up for you" |
| **Contact Flow** | The path a call/chat takes in Amazon Connect | The overall journey |
| **Agentic CX Block** | Bridge between Connect flow and ACXD app | The handoff point |
| **S3** | Simple Storage Service — file storage in AWS | Where you upload PDFs |
| **PII** | Personally Identifiable Information | SSN, credit card, DOB |

---

---

# PART 6: What to Ask / Say on the Call

---

## If Charit Explains the Flow
- "Got it, I've already gone through the Draw.io. Just to confirm — we're building this entire flow using ACXD, right?"
- "For the authentication step, is there an existing Lambda, or do we build one?"

## If Charit Asks What You Know
- "I've explored ACXD in detail and submitted documentation to Govinde. I also went through the CIGNA flow — the document ingestion into Kendra, the FAQ agent query flow, and how RAG works in this context."

## If Charit Asks About ACXD Specifically
- You know this inside out — refer to PART 1 above
- Key point: "ACXD lets us mix fixed rules for auth/compliance with AI for understanding and answering — which is exactly what this CIGNA flow needs."

## Smart Questions to Ask
- "What's our timeline for the POC?"
- "Do we have sample CIGNA documents to load into Kendra?"
- "When are we getting AWS access?"
- "Are we starting with voice, chat, or both?"
- "Is the live agent piece in the first phase, or a later addition?"

## If You Don't Know Something
> "That's a good question — let me look into that and get back to you."

Never guess. Always better to be honest.

---

**You're well-prepared. Go in confident — you know this stuff.** 💪
