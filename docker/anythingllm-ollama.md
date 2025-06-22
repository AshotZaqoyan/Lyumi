# 🚀 AnythingLLM + Ollama Docker Installation Guide

This guide will help you deploy **AnythingLLM** and **Ollama** together using Docker Compose to power a local, private AI assistant. It includes everything from installation to embedding model setup, LLM configuration, and API key generation.

---

## 📦 Quick Start

### ✅ Option 1: Combined Setup (Recommended)

Use this method if you're setting up both services on the same machine.

Create a `docker-compose.yml` file:

```yaml
version: '3.8'
services:
  ollama:
    image: ollama/ollama
    container_name: ollama
    volumes:
      - ollama_data:/root/.ollama
    ports:
      - "11434:11434"
    restart: unless-stopped
    networks:
      - ai_network

  anythingllm:
    image: mintplexlabs/anythingllm
    container_name: anythingllm
    depends_on:
      - ollama
    ports:
      - "3001:3001"
    cap_add:
      - SYS_ADMIN
    environment:
      - STORAGE_DIR=/app/server/storage
      - JWT_SECRET=${JWT_SECRET:-$(openssl rand -hex 32)}
      - LLM_PROVIDER=openai
      - OPEN_MODEL_PREF=gpt-4o-mini
      - EMBEDDING_ENGINE=ollama
      - EMBEDDING_BASE_PATH=http://ollama:11434
      - EMBEDDING_MODEL_PREF=nomic-embed-text:latest
      - EMBEDDING_MODEL_MAX_CHUNK_LENGTH=8192
      - VECTOR_DB=lancedb
      - WHISPER_PROVIDER=local
      - TTS_PROVIDER=native
      - PASSWORDMINCHAR=8
    volumes:
      - anythingllm_storage:/app/server/storage
    restart: always
    networks:
      - ai_network

volumes:
  ollama_data:
  anythingllm_storage:

networks:
  ai_network:
    driver: bridge
```

---

### 🧩 Option 2: Separate Services

For advanced users running containers individually.

**ollama-compose.yml**

```yaml
version: "3.8"
services:
  ollama:
    image: ollama/ollama
    container_name: ollama
    volumes:
      - ollama:/root/.ollama
    ports:
      - "11434:11434"
    restart: unless-stopped
volumes:
  ollama:
```

**anythingllm-compose.yml**

```yaml
version: '3.8'
services:
  anythingllm:
    image: mintplexlabs/anythingllm
    container_name: anythingllm
    ports:
      - "3001:3001"
    cap_add:
      - SYS_ADMIN
    environment:
      - STORAGE_DIR=/app/server/storage
      - JWT_SECRET=${JWT_SECRET:-$(openssl rand -hex 32)}
      - LLM_PROVIDER=openai
      - OPEN_MODEL_PREF=gpt-4o-mini
      - EMBEDDING_ENGINE=ollama
      - EMBEDDING_BASE_PATH=http://127.0.0.1:11434
      - EMBEDDING_MODEL_PREF=nomic-embed-text:latest
      - EMBEDDING_MODEL_MAX_CHUNK_LENGTH=8192
      - VECTOR_DB=lancedb
      - WHISPER_PROVIDER=local
      - TTS_PROVIDER=native
      - PASSWORDMINCHAR=8
    volumes:
      - anythingllm_storage:/app/server/storage
    restart: always
volumes:
  anythingllm_storage:
```

---

## ⚙️ Setup Instructions

### 1. Run Docker Services

**Combined Setup:**

```bash
docker-compose up -d
```

**Separate Setup:**

```bash
docker-compose -f ollama-compose.yml up -d
docker-compose -f anythingllm-compose.yml up -d
```

---

### 2. Install Embedding Model

```bash
docker exec -it ollama ollama pull nomic-embed-text
```

---

### 3. Configure AnythingLLM

Visit: [http://localhost:3001](http://localhost:3001)

#### 🔧 Settings:

* **LLM Provider**: `OpenAI`
* **API Key**: Your valid OpenAI API Key
* **Model**: `gpt-4o-mini`

#### 📚 Embedding:

* **Embedding Provider**: `Ollama`
* **Embedding Model**: `nomic-embed-text:latest`
* **Embedding Base URL**:

  * `http://ollama:11434` (Combined setup)
  * `http://127.0.0.1:11434` (Separate setup)

#### 🔐 Security:

* Go to **Settings → Security**
* Enable **Multi-User Mode**
* Set and save a **strong password**

---

### 4. Generate API Key

* Go to **Settings → API Keys**
* Click **Create New API Key**
* Save this key securely for your bot (it's for ANYTHINGLLM_API_KEY)

---

## 🧪 Verify Your Setup

### ✅ Check Running Containers

```bash
docker ps
```

### 📋 Logs

```bash
docker logs ollama
docker logs anythingllm
```

### 🔍 Test Embeddings

```bash
curl -X POST http://localhost:11434/api/embeddings \
  -H "Content-Type: application/json" \
  -d '{"model": "nomic-embed-text", "prompt": "test"}'
```

---

## 🛑 Shut Down & Clean Up

```bash
# Stop services
docker-compose down

# Remove volumes (DANGER: Deletes all data)
docker-compose down -v
```

---

## 🔐 Security Tips

* Always use strong passwords
* Keep your API keys safe
* Set up reverse proxy for production (e.g. Nginx with HTTPS)
* Regularly back up your volumes (`ollama_data`, `anythingllm_storage`)

---

🎉 **You're all set!** You now have a full local AI assistant powered by AnythingLLM + Ollama. Enjoy embedding-rich conversations with custom documents in a secure, private environment. Now you can go [here](../README.md) and continue.