# 🛍️ PriceOye Customer Service Agent

An AI-powered customer service automation system built for [PriceOye](https://priceoye.pk) — Pakistan's leading e-commerce platform. This agent handles customer inquiries automatically, providing instant responses with intelligent query resolution.

---

## 🎯 Problem

Customer service teams spend hours daily answering repetitive questions — order status, return policies, product availability. This creates delays, inconsistent responses, and high operational costs.

## 💡 Solution

An AI agent that:
- **Understands customer intent** from natural language queries
- **Retrieves real-time data** (order status, product info, FAQs)
- **Responds instantly** with accurate, contextual answers
- **Escalates intelligently** when human intervention is needed

---

## 🏗️ Architecture

```
Customer Query
     ↓
  AI Agent (Claude/OpenAI)
     ↓
  Intent Classification
     ↓
  ┌──────────────────┐
  │ FAQ Lookup (RAG)  │
  │ Order Status API  │
  │ Product Search    │
  │ Escalation Logic  │
  └──────────────────┘
     ↓
  Response Generation
     ↓
  Customer Response
```

---

## 🛠️ Tech Stack

![N8N](https://img.shields.io/badge/N8N-EA4B71?style=flat&logo=n8n&logoColor=white)
![Claude AI](https://img.shields.io/badge/Claude_AI-191919?style=flat)
![Python](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white)
![Qdrant](https://img.shields.io/badge/Qdrant-DC382D?style=flat)

- **N8N** — Workflow orchestration and API integrations
- **Claude AI** — Natural language understanding and response generation
- **Qdrant** — Vector database for FAQ retrieval (RAG)
- **Python** — Custom logic and data processing

---

## ✨ Features

- 🤖 Automated customer inquiry handling
- 🔍 RAG-based FAQ retrieval for accurate answers
- 📦 Real-time order status lookup
- 🔄 Intelligent escalation to human agents
- 📊 Multi-channel support (chat widget, email)
- ⚡ Sub-second response times

---

## 📫 Contact

**Wajid Javed** — [LinkedIn](https://www.linkedin.com/in/wajidjaved160/) | [YouTube](https://youtube.com/@PhotiqAI) | [Portfolio](https://wajid-javed-portfolio.vercel.app/)
