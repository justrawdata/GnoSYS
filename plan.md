# Knowledge Vault Master Plan

*A roadmap from zero to a production‑grade, sovereign, graph‑aware Document & Knowledge Vault (DKV).*

---

## 0  North‑Star Objectives

| # | Goal | Success Metric |
|---|------|----------------|
| 0 | **Local‑first sovereignty** | Vault runs 100 % offline; can sync via encrypted bundles. |
| 1 | **Poly‑format ingestion** | Import Markdown, PDFs, images (OCR), ZIP backups, JSON, CSV, Discord exports. |
| 2 | **Fast search + semantic QA** | < 50 ms keyword search; < 2 s LLM‑powered answer. |
| 3 | **Graph insights** | Visual entity ↔ event ↔ doc network; clickable edges. |
| 4 | **Plugin ecosystem** | FE/BE hooks + manifest spec; CRUD an extension in < 30 min. |
| 5 | **Portable builds** | One‑shot `docker compose up` or single‑binary installer. |

---

## 1  Core Stack Selection

| Layer | Tech | Why |
|-------|------|-----|
| **Storage** | Flat files + **ZIM** container → **CARv2** content‑addressed archive | Immutable chunks, delta‑friendly, easy to sync. |
| **Graph DB** | **TerminusDB** (time‑travel) wrapped by Neo4j‑compatible Bolt bridge | Git‑like history + Cypher querying. |
| **Search** | **Typesense** (Apache 2) | Lightning‑fast fuzzy search; simple Docker image. |
| **OCR / NLP** | **Tesseract** + **spaCy** | On‑device text & entity extraction. |
| **LLM interface** | **LlamaIndex** | Same code‑path for online/offline QA. |
| **API** | **FastAPI** | Async, OpenAPI spec, pydantic schemas. |
| **Task queue** | **Celery** + Redis | Async ingestion & re‑index. |
| **Frontend** | **Next.js** + shadcn/ui + Tailwind | Modern DX; dark theme. |
| **Auth** | JWT (+ optional OIDC) | Can be disabled for single‑user offline mode. |
| **Container** | Docker‑Compose (later Podman) | 1‑command deployment. |

---

## 2  Domain Model (MVP)

```mermaid
erDiagram
    DOCUMENT ||--o{ PAGE : contains
    DOCUMENT {
        string id PK
        string title
        string path
        string mime
        datetime added_at
    }
    PAGE {
        string id PK
        string document_id FK
        int page_no
        text raw_text
        json ocr_chunks
    }
    ENTITY ||--o{ MENTION : has
    ENTITY {
        string id PK
        string type   // Person, Org, Place, Concept
        string name
    }
    MENTION {
        string id PK
        string page_id FK
        string entity_id FK
        int start
        int end
    }
```

---

## 3  System Architecture

```
┌──────── UI (Next.js) ───────┐
│  • Search bar (Typesense)   │
│  • Graph view (d3‑force)    │
│  • Doc viewer (PDF.js)      │
│  • Plugin side‑panel        │
└─────────▲─────┬─────────────┘
          │REST │WS events
┌─────────┴─────▼─────────────┐
│      FastAPI Gateway        │
│  • Auth/JWT                 │
│  • CRUD routes              │
│  • Plugin RPC bridge        │
└─────────▲─────┬─────────────┘
          │Celery tasks
┌─────────┴─────▼─────────────┐
│  Worker Pool                │
│  • Ingestion (ZIP, PDF…)    │
│  • OCR & NLP pipeline       │
│  • Chunk & embed → Typesense│
│  • Graph update → Terminus  │
└─────────▲─────┬─────────────┘
          │PG/Redis
┌─────────┴─────▼─────────────┐
│  Storage Layer              │
│  • ZIM / CARv2 blobs        │
│  • Immutable chunk store    │
│  • Postgres (metadata)      │
│  • TerminusDB (graph)       │
│  • Typesense (index)        │
└─────────────────────────────┘
```

---

## 4  Plugin Framework

| Hook | Payload | Example |
|------|---------|---------|
| **backend_ingest** | `{file_path, mime}` | Auto‑transcribe MP3 → text |
| **post_index** | `{doc_id, embeddings}` | Trigger custom classifier |
| **graph_overlay** | Cypher query | Render relationship heatmap |
| **ui_panel** | React micro‑frontend | Timeline plugin |

*Manifest*: `dkv-plugin.json` with name, version, entrypoint, permissions.

---

## 5  File / Repo Layout

```
knowledge-vault/
  backend/
    app/                # FastAPI src
    celery_worker.py
    plugins/
      core/
      custom/
    Dockerfile
  frontend/
    components/
    pages/
    plugins/            # Micro‑frontends
    docker.Dockerfile
  data/
    zim_blobs/
    car_store/
  compose.yaml
  docs/
    ARCHITECTURE.md
    PLUGIN_SDK.md
```

---

## 6  Development Phases & Milestones

| Phase | Duration | Deliverables |
|-------|----------|--------------|
| **0 Bootstrap** | 1 wk | Repo skeleton, `compose.yaml` (Typesense, Postgres, TerminusDB, Redis). |
| **1 Ingestion MVP** | 2 wks | Upload PDF → OCR → searchable text. REST endpoints + basic UI list. |
| **2 Search & Graph** | 2 wks | Typesense query UI; entity extraction; Cypher graph view. |
| **3 ZIM Packing** | 1 wk | Export/import collections as ZIM; integrity hash checks. |
| **4 Plugins Alpha** | 2 wks | Backend hook system + word‑cloud demo plugin; FE plugin loader. |
| **5 LLM QA** | 1 wk | Langchain wrapper; ask‑the‑vault chat box. |
| **6 CARv2 Migration** | 3 wks | Content‑addressed storage; delta sync; CLI tool. |
| **7 Harden & Ship** | 2 wks | Auth, RBAC, backups, signed releases, doc site. |

_Total: ≈ 14 weeks to v1.0._

---

## 7  Security & Sovereignty Checklist

1. Containers run **rootless** (userns‑remap / Podman).  
2. Optional **FIDO2** hardware keys for admin login.  
3. **AES‑GCM‑256** encryption per ZIM/CAR bundle (Argon2‑derived key).  
4. **No telemetry** by default; opt‑in crash stats.  
5. **Reproducible builds** via Nix flakes (stretch goal).  

