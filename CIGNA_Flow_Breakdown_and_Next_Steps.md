# CIGNA Experiment — Flow Breakdown & Next Steps
**For: Madhav (while waiting for Govinde's reply)**

---

## The Draw.io Flow — Step by Step (Simple Language)

Here's what the **FAQ AI Agent Query Flow** diagram shows, in plain English:

```
Customer (Actor)
    │
    ▼
┌──────────────────┐
│ ① Amazon Connect  │  ← Customer calls or chats
└────────┬─────────┘
         │
         ▼
┌──────────────────┐     ┌─────┐
│ ② Auth Lambda     │────▶│ DB  │  ← Verify who the customer is
│    (2a)           │◀────│(2b) │
└────────┬─────────┘     └─────┘
         │
         ▼
┌──────────────────┐
│ ③ Lex (3a)        │  ← Understands what the customer said
└────────┬─────────┘
         │
    ┌────┴────┐
    ▼         ▼
┌────────┐ ┌──────────┐
│AI Intent│ │Bedrock   │  ← Figures out the customer's INTENT
│Identifier│ │LLM (3c)  │     using AI
│  (3b)  │ └──────────┘
└────┬───┘
     │
     ▼
┌──────────────────┐     ┌─────────────┐
│ ④ Fulfillment     │────▶│⑤ OpenSearch  │  ← Searches for answers
└────────┬─────────┘     └─────────────┘
         │
         ▼
┌──────────────────┐     ┌─────────────┐
│ ⑥a FAQ AI Agent   │◀───│⑥c Kendra RAG │  ← Gets knowledge from docs
└────────┬─────────┘     └─────────────┘
         │
         ▼
   ┌───────────┐
   │ ⑥b Bedrock │  ← Generates the final answer
   │    LLM     │
   └───────────┘
         │
         ▼
   Response back to Customer
```

---

## What Each Step Does (Beginner Version)

### Step ① — Amazon Connect
**What:** This is the entry point. The customer either **calls** (voice) or **types** (chat) to reach the system.  
**Think of it as:** The reception desk that picks up the phone.

### Step ② — Authentication (Lambda + DB)
**What:** Before helping the customer, the system verifies **who they are**. A Lambda function checks their identity against a database.  
**Think of it as:** "Can I have your policy number and date of birth to verify your account?"

### Step ③ — Lex + AI Intent Identifier + Bedrock LLM
**What:** This is where the system **understands** what the customer wants. Three things work together:
- **Lex (3a):** Listens to the customer's words (voice-to-text if on a call)
- **AI Intent Identifier (3b):** Figures out the "intent" — what does the customer actually want?
- **Bedrock LLM (3c):** Uses a large language model to understand complex or unclear requests

**Think of it as:** The smart assistant that listens and thinks, "Okay, this person wants to know about their claim status."

### Step ④ — Fulfillment
**What:** Now that the system knows what the customer wants, this step **acts on it**. It triggers the right process to get the answer.  
**Think of it as:** The assistant saying, "Let me look that up for you."

### Step ⑤ — OpenSearch
**What:** Searches through indexed data to find relevant results. This could be searching through structured data like claims, policies, etc.  
**Think of it as:** A fast search engine looking through the company's data.

### Step ⑥ — FAQ AI Agent + Kendra RAG + Bedrock LLM
**What:** This is the **brain** of the system. Three things work together:
- **Kendra RAG (6c):** Pulls relevant information from company documents (PDFs, policies, FAQs that were ingested earlier)
- **FAQ AI Agent (6a):** Takes the retrieved info and figures out the best answer
- **Bedrock LLM (6b):** Generates a natural, human-like response

**Think of it as:** The expert who reads the relevant policy documents, understands them, and explains the answer to the customer in simple words.

---

## The Three Big Pieces of this System

| Piece | What It Does | AWS Services Used |
|-------|-------------|-------------------|
| **1. Document Ingestion** | Loads company docs into the system so AI can search them | S3 → Kendra (crawl, parse, chunk, index) |
| **2. Understanding the Customer** | Figures out what the customer is asking | Amazon Connect → Lex → Bedrock LLM |
| **3. Finding & Delivering Answers** | Searches docs, generates a smart answer | Kendra RAG + OpenSearch → Bedrock LLM → Response |

---

## What You Should Study Next (While Waiting for Reply)

Here's your study roadmap — in order of priority:

### 🔴 Priority 1: Understand the Core Services (Do This First)

#### 1. Amazon Connect — The Contact Center
- **What to learn:** How calls/chats enter the system, what a "contact flow" is
- **Where:** [Amazon Connect Overview](https://docs.aws.amazon.com/connect/latest/adminguide/what-is-amazon-connect.html)
- **Focus on:** Contact flows, channels (voice + chat), and the Agentic CX block (you already know this from your ACXD research!)

#### 2. Amazon Lex — The Conversation Engine
- **What to learn:** How Lex understands spoken/typed words, what "intents" and "slots" are
- **Where:** [Amazon Lex Docs](https://docs.aws.amazon.com/lexv2/latest/dg/what-is.html)
- **Key terms to understand:**
  - **Intent** = What the customer wants (e.g., "CheckClaimStatus", "AskAboutCoverage")
  - **Slot** = The details needed (e.g., policy number, date of birth)
  - **Utterance** = The actual words the customer says (e.g., "What's my claim status?")

#### 3. Amazon Kendra — The Knowledge Search (RAG)
- **What to learn:** How Kendra ingests documents, indexes them, and retrieves relevant answers
- **Where:** [Amazon Kendra Docs](https://docs.aws.amazon.com/kendra/latest/dg/what-is-kendra.html)
- **Key terms:**
  - **RAG** = Retrieval-Augmented Generation (search docs first, then generate answer)
  - **Data Source** = Where docs come from (S3 bucket in this case)
  - **Index** = The searchable database Kendra creates from your docs

#### 4. Amazon Bedrock — The AI Brain
- **What to learn:** What Bedrock is, what LLMs are available, how it generates responses
- **Where:** [Amazon Bedrock Docs](https://docs.aws.amazon.com/bedrock/latest/userguide/what-is-bedrock.html)
- **Focus on:** Foundation models (Claude, Titan), and how Bedrock is used for text generation

### 🟡 Priority 2: Supporting Services

#### 5. AWS Lambda — The Glue
- **What to learn:** Lambda runs small pieces of code when triggered. In this flow, it handles authentication.
- **Simple version:** Lambda is like a mini-program that runs only when needed, does its job, and stops. No server to manage.

#### 6. Amazon OpenSearch — The Search Engine
- **What to learn:** How OpenSearch indexes and searches structured data
- **Simple version:** Think of it as a super-fast search engine for your company's data (different from Kendra which is more for documents/FAQs)

### 🟢 Priority 3: Connect It Back to ACXD

#### 7. Map This Flow to ACXD Concepts
Since Govinde wants this built using **Agentic CX Designer**, think about how each step maps:

| Draw.io Step | ACXD Equivalent |
|-------------|-----------------|
| Amazon Connect entry | Contact Flow → Agentic CX Block |
| Authentication (Lambda + DB) | Deterministic Node (Data Request / API call) |
| Lex + Intent Identification | Agentic AI Node (Generative Journey) |
| Bedrock LLM for understanding | Built into ACXD's agentic nodes |
| Kendra RAG | Knowledge Base node in ACXD |
| OpenSearch | Data Request node (API integration) |
| FAQ AI Agent response | Agentic AI Node (response generation) |
| Live Agent escalation | Transfer/Escalation node |

---

## Key Terms Cheat Sheet

| Term | What It Means (Simple) |
|------|----------------------|
| **RAG** | Search real docs first, then use AI to write the answer. Prevents the AI from making things up. |
| **LLM** | Large Language Model — the AI that understands and generates human language (like ChatGPT) |
| **Intent** | What the customer wants to do (e.g., check claim, ask about coverage) |
| **Slot** | The specific details needed to fulfill the intent (e.g., policy number) |
| **Kendra** | AWS's smart document search service — reads your PDFs and finds answers |
| **Bedrock** | AWS's AI platform — gives you access to powerful AI models |
| **Lambda** | A small piece of code that runs on-demand — no server needed |
| **OpenSearch** | A search and analytics engine for structured data |
| **Fulfillment** | The step where the system actually does what was requested |
| **Chunking** | Breaking large documents into smaller pieces so AI can search them better |
| **Indexing** | Organizing document chunks so they can be found quickly |

---

## Quick Action Plan

```
RIGHT NOW (while waiting for reply):
  ✅ Read about Amazon Lex — intents, slots, utterances
  ✅ Read about Amazon Kendra — what RAG is, how document ingestion works
  ✅ Read about Amazon Bedrock — what models are available

WHEN GOVINDE REPLIES:
  □ Clarify: Are we building this in ACXD specifically, or using the 
    individual services (Connect + Lex + Kendra + Bedrock)?
  □ Clarify: What documents/PDFs will be used for the Kendra knowledge base?
  □ Clarify: Is the "live agent" escalation for when AI can't answer?
  □ Clarify: Voice + Text both — are we using the same flow for both?

GOOD QUESTIONS TO ASK GOVINDE:
  • "Should I map this Draw.io flow to ACXD nodes as a next step?"
  • "For the RAG piece, do we have sample CIGNA documents to test with?"
  • "For authentication, is there an existing Lambda/DB, or do we build it?"
```

---

*You're doing great — you already understand the flow. Now just fill in the gaps on each service.* 👊
