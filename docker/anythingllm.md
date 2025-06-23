# 🚀 AnythingLLM Docker Installation Guide (OpenAI Only)

This guide will help you deploy **AnythingLLM** using Docker Compose to power a local AI assistant using **OpenAI** as both the LLM and embedding provider. It includes everything from installation to embedding setup, configuration, and API key generation.

---

## 📦 Quick Start

### ✅ Setup with Docker Compose

Create a `docker-compose.yml` file:

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
      - EMBEDDING_ENGINE='openai'
      - EMBEDDING_MODEL_PREF=text-embedding-3-small # or text-embedding-ada-002
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

### 1. Run Docker Service

```bash
docker compose up -d
```

---

### 2. Configure AnythingLLM

Visit: [http://localhost:3001](http://localhost:3001)

#### 🔧 Settings:

* **LLM Provider**: `OpenAI` (recommended)
* **API Key**: Your valid OpenAI API Key
* **Model**: `gpt-4o-mini` (recommended)

#### 📚 Embedding:

* **Embedding Provider**: `OpenAI`

#### 🔐 Security:

* Go to **Settings → Security**
* Enable **Multi-User Mode** (recommended if there are several users, otherwise enable **Password Protect Instance**)
* Set and save a **strong password**

---

### 3. Generate API Key

* Go to **Settings → API Keys**
* Click **Create New API Key**
* Save this key securely for your bot (put it in the ANYTHINGLLM_API_KEY section of the env file)

---

### 🧠 4. Create a Workspace & Embed Example Document

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
* Regularly back up your volumes (`anythingllm_storage`)

---

🎉 **You're all set!** You now have a full local AI assistant powered by AnythingLLM with OpenAI. Enjoy embedding-rich conversations with custom documents in a secure, private environment.
