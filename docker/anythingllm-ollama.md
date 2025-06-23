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
docker compose up -d
```

**Separate Setup:**

```bash
docker compose -f ollama-compose.yml up -d
docker compose -f anythingllm-compose.yml up -d
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

* **LLM Provider**: `OpenAI` (recommended)
* **API Key**: Your valid OpenAI API Key
* **Model**: `gpt-4o-mini` (recommended)

#### 📚 Embedding:

* **Embedding Provider**: `Ollama` (recommended)
* **Embedding Model**: `nomic-embed-text:latest` (recommended)
* **Embedding Base URL**:

  * `http://ollama:11434` (Combined setup)
  * `http://127.0.0.1:11434` (Separate setup)

#### 🔐 Security:

* Go to **Settings → Security**
* Enable **Multi-User Mode** (recommended if there are several users otherwise enable **Password Protect Instance**)
* Set and save a **strong password**

---

### 4. Generate API Key

* Go to **Settings → API Keys**
* Click **Create New API Key**
* Save this key securely for your bot (put it in the ANYTHINGLLM_API_KEY section of the env file)

---

### 🧠 5. Create a Workspace & Embed Example Document

After generating your API key:

#### 🏷️ Create a Workspace

* Go to the dashboard
* Click **New Workspace**
* Enter a name (📌 this must match the value in your `.env` under `WORKSPACE_SLUG`)

✅ It’s also recommended to configure your **System Prompt**:

* On the left side, next to the workspace name, click the ⚙️ settings icon
* Navigate to the **Chat Settings** tab
* Modify the **System Prompt** field to control your bot’s behavior
* Example prompt
```text
Դու Լյումին ես՝ բարի և հարգալից օգնական, որը ստեղծվել է ՄԵՄ ՀԿ-ի («Մարզերի երեխաները մարզերում») IT բաժնի կողմից։ Դու նախատեսված ես ՄԵՄ-ի բոլոր անդամներին օգնելու համար։

Դու ունես միայն ՄԵՄ-ի հետ կապված հատուկ գիտելիքների բազա։ Դու պետք է պատասխանես միայն այդ գիտելիքների վրա հիմնվելով։ Եթե չգիտես հարցի պատասխանը, մի փորձիր հորինել կամ կռահել։ Այդ դեպքում ասա՝
«Ներեցեք, այս պահին չեմ կարող պատասխանել այդ հարցին։ Կարող եք գրել այս ալիքում՝ https://discord.com/channels/838687641896484904/852314123496718396 կամ կապ հաստատել համապատասխան բաժնի հետ»։

Եթե քեզ տրվի հարց, որը կապ չունի ՄԵՄ-ի հետ, պետք է պատասխանիր՝
«Ես նախատեսված եմ պատասխանելու միայն ՄԵՄ-ի հետ կապված հարցերին։ Խնդրում եմ, տվեք ՄԵՄ-ի գործունեությանը, անդամներին կամ ծրագրերին վերաբերող հարց»։

Դու պետք է խոսես հարգալից ու մտերմիկ տոնով՝ «Դուք»-ով, բայց մի անցիր մասնագիտական սահմանները։ Կարող ես օգտագործել էմոջիներ 😊, բայց քիչ և նուրբ չափով։

Քո նպատակն է օգնել ՄԵՄ-ի անդամներին՝ հստակ, վստահելի և ընկերական կերպով։
```

#### 📎 Embed a Document

* On the home screen, click **Embed a Document**
* Select **Click to upload or drag and drop**, and upload your file(s)
* On the left panel, check the file(s) you want to embed
* Click **Move to Workspace**
* Then click **Save and Embed**
* Wait for the embedding process to complete and close the window

💬 Optionally, test it by clicking **Send Chat** and asking a question about the content

---

## 🛑 Shut Down & Clean Up

```bash
# Stop services
docker compose down

# Remove volumes (DANGER: Deletes all data)
docker compose down -v
```

---

## 🔐 Security Tips

* Always use strong passwords
* Keep your API keys safe
* Set up reverse proxy for production (e.g. Nginx with HTTPS)
* Regularly back up your volumes (`ollama_data`, `anythingllm_storage`)

---

🎉 **You're all set!** You now have a full local AI assistant powered by AnythingLLM + Ollama. Enjoy embedding-rich conversations with custom documents in a secure, private environment. Now you can go [here](../README.md) and continue.