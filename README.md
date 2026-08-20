# 🎓 0$ University LinkedIn Growth Engine (v1.0 Production)

An enterprise-grade, autonomous LinkedIn publishing, educational curriculum curation, and multi-actor network engagement engine managing **0$ University** for **Arif Alam** (~292K+ Followers | Founder at *0$ University* & *Data Science Reality*).

---

## 📌 Core Mission & Operational Architecture

**0$ University** democratizes world-class computer science and AI education by curating 100% free roadmaps, Ivy League curricula (MIT, Stanford, Harvard, UC Berkeley), open-source repositories, and system design masterclasses.

### 🛡️ Profile Isolation & Safety Directives
- **Personal Profile Isolation:** The personal profile `Arif Alam` is never posted to by this engine.
- **Dedicated Company Admin Routing:** The runner navigates directly to 0$ University's Organization Admin Dashboard (`https://www.linkedin.com/company/startup-founderss/admin/dashboard/?createPageAssets=true`).
- **Standardized Topmate Suite & WhatsApp:** All posts embed verified resources and links inside the post body.
- **1st Comment Pinning:** Pinned Topmate free education vault comment submitted immediately post-publication.

---

## ⏰ 5x Daily Posting Schedule

| Slot | Time (IST) | Time (UTC) | Content Focus & Document Type |
| :-: | :-: | :-: | :--- |
| **Slot 1** | **08:00 AM IST** | 02:30 AM UTC | Full CS / AI Degree Open-Source Roadmap (Multi-Page PDF) |
| **Slot 2** | **11:00 AM IST** | 05:30 AM UTC | Stanford & MIT Deep Learning / ML Vault (Lecture Cheatsheet PDF) |
| **Slot 3** | **02:00 PM IST** | 08:30 AM UTC | Free Harvard CS50 / SQL Engineering Foundations |
| **Slot 4** | **05:00 PM IST** | 11:30 AM UTC | Distributed Systems & Big Data Cheatsheets (PySpark / Dask) |
| **Slot 5** | **08:30 PM IST** | 03:00 PM UTC | FAANG Coding, System Design & Transformer Architectures |

---

## ⚡ 8-Actor Cross-Engagement Booster

Immediately following publication:
1. The engine navigates to the live post permalink (`https://www.linkedin.com/feed/update/{urn}/`).
2. Sequentially switches active identity across all 8 managed identities:
   - `0$ University` (Author)
   - `Data Science Reality`
   - `100DaysOfAI`
   - `Web3Schools`
   - `Data Science Myth`
   - `Data Science For Schools`
   - `Probability and Statistics`
   - `Arif Alam`
3. Dispatches verified Like reaction from each brand page.
4. Posts the 0$ University pinned education resource suite in the first comment.

---

## 📂 Repository Structure

```text
Zero_Dollar_University_Pipeline/
├── README.md                                 # Master Operational Documentation
├── requirements.txt                          # Python dependencies (Playwright, Requests, Pillow)
├── Run_0Dollar_Uni.command                   # Double-clickable macOS launcher
├── run_pipeline.sh                           # Shell pipeline execution script
├── .gitignore                                # Git ignore rules
├── .github/
│   └── workflows/
│       └── zero_dollar_uni_pipeline.yml      # 5x daily scheduled GitHub Actions workflow
├── config/
│   ├── config.json                           # Brand parameters, links, and engagement actors
│   ├── zero_dollar_uni_catalog.json          # Curated educational roadmap & document catalog
│   ├── zero_dollar_uni_posted_history.json   # Deduplication ledger
│   └── full_browser_cookies.json             # Local authenticated session cookies
├── documents/
│   └── pdf_vault/                            # Authentic Stanford/MIT/Harvard PDF Carousels
├── scripts/
│   ├── zero_dollar_uni_runner.py             # Playwright automation engine
│   └── qa_dedup_auditor.py                   # Catalog consistency & PDF integrity auditor
└── logs/                                     # Execution logs & screenshot proofs
```

---

## 🚀 Setup & Deployment Guide

### Option 1: Autonomous GitHub Actions (Cloud 24/7)

1. Create a private GitHub repository:
   ```bash
   git init
   git add .
   git commit -m "feat: initial 0$ university pipeline release"
   git branch -M main
   git remote add origin git@github.com:iamarifalam/zero-dollar-university-pipeline.git
   git push -u origin main
   ```
2. In your GitHub repository, navigate to **Settings > Secrets and variables > Actions** and add the following repository secrets:
   - `LI_AT`: LinkedIn `li_at` cookie value
   - `JSESSIONID`: LinkedIn `JSESSIONID` cookie value
   - `BCOOKIE`: LinkedIn `bcookie` cookie value (optional)
   - `BSCOOKIE`: LinkedIn `bscookie` cookie value (optional)

### Option 2: Local Execution (macOS)

1. Install dependencies:
   ```bash
   python3 -m pip install -r requirements.txt
   playwright install chromium
   ```
2. Run QA validation:
   ```bash
   python3 scripts/qa_dedup_auditor.py
   ```
3. Run dry-run test:
   ```bash
   python3 scripts/zero_dollar_uni_runner.py --dry-run
   ```
4. Execute live post:
   ```bash
   ./run_pipeline.sh
   # OR double-click Run_0Dollar_Uni.command in Finder
   ```

---

## 👨‍💻 Creator & Links
- **Founder:** [Arif Alam](https://www.linkedin.com/in/iamarifalam/)
- **Brand Page:** [0$ University on LinkedIn](https://www.linkedin.com/company/startup-founderss/)
