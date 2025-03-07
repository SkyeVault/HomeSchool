# Homeschool System - Raspberry Pi + Rust

## Overview
This guide provides a **step-by-step** method for setting up a **self-contained AI-powered homeschool system** on a **Raspberry Pi**, using **Rust** for the backend and a **long-term stable software stack**. The system will work **offline-first**, with optional internet connectivity for updates.

## Hardware Requirements
- **Raspberry Pi 4 or newer** (Recommended: 8GB RAM for AI models)
- **External SSD or large SD card** (Minimum 128GB for AI models and curriculum storage)
- **HDMI Display or Touchscreen** (For user interface)
- **USB Keyboard & Mouse**
- **Optional: Arduino Boards** (For STEM & engineering projects)

## Software Stack
### Backend (Rust-based API & Data Management)
- **Rust (`Axum` or `Actix-web`)** - Web API framework
- **SQLite** - Local database (fast, embedded, durable)
- **SurrealDB (optional)** - For real-time syncing when online
- **Llama 3 AI Model** - Runs locally for AI-driven lessons

### Frontend (User Interface)
- **Tauri (Rust-based)** - Lightweight UI framework
- **SvelteKit** - Web interface with long-term maintainability
- **HTMX (optional)** - Minimalist JavaScript alternative for UI interactions

### Storage & File System
- **Local Filesystem (`/curriculum`, `/media`, `/ai/models`)** - For storing lessons, videos, and AI-generated content
- **GitHub/GitLab Repository** - For public codebase and backup system
- **MinIO or AWS S3 (optional)** - If cloud storage is needed

### Offline AI Model
- **Llama 3 or Mistral AI** - Open-source AI model for lesson generation
- **ggml/llama.cpp** - Runs AI models on CPU without internet

## Step 1: Setting Up Raspberry Pi
### 1.1 Install Raspberry Pi OS
Download and install **Raspberry Pi OS (64-bit, Lite recommended)**:
```sh
sudo apt update && sudo apt upgrade -y
```

### 1.2 Install Essential Software
```sh
sudo apt install git curl build-essential python3-pip libsqlite3-dev
```

## Step 2: Install Rust & Toolchain
```sh
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
source $HOME/.cargo/env
```

Install dependencies for compiling Rust projects:
```sh
sudo apt install pkg-config libssl-dev libclang-dev
```

## Step 3: Setting Up Backend API (Rust)
### 3.1 Create Rust Project
```sh
cargo new homeschool_ai
cd homeschool_ai
```

### 3.2 Add Dependencies
Edit `Cargo.toml` and add:
```toml
[dependencies]
axum = "0.6"
tokio = { version = "1", features = ["full"] }
sqlx = { version = "0.6", features = ["sqlite", "runtime-tokio-native-tls"] }
serde = { version = "1", features = ["derive"] }
tower-http = { version = "0.3", features = ["cors"] }
```

### 3.3 Create API Endpoints
Edit `src/main.rs`:
```rust
use axum::{routing::get, Router};
use std::net::SocketAddr;

async fn health_check() -> &'static str {
    "Server is running"
}

#[tokio::main]
async fn main() {
    let app = Router::new()
        .route("/health", get(health_check));

    let addr = SocketAddr::from(([0, 0, 0, 0], 8080));
    println!("Running on http://{}", addr);
    axum::Server::bind(&addr)
        .serve(app.into_make_service())
        .await
        .unwrap();
}
```
Run the API:
```sh
cargo run
```
Test:
```sh
curl http://localhost:8080/health
```

## Step 4: Setting Up SQLite Database
```sh
cargo install sqlx-cli
sqlx database create
```
Define schema in `migrations/01_init.sql`:
```sql
CREATE TABLE lessons (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    subject TEXT NOT NULL,
    grade TEXT NOT NULL,
    content TEXT NOT NULL
);
```
Apply migration:
```sh
sqlx migrate run
```

## Step 5: AI Integration (Offline Llama 3)
### 5.1 Install Llama.cpp
```sh
git clone https://github.com/ggerganov/llama.cpp.git
cd llama.cpp
make -j4
```

### 5.2 Download Llama 3 Model
```sh
mkdir -p ~/ai/models
cd ~/ai/models
wget [MODEL_URL] -O llama-3.bin
```

### 5.3 Test AI Model
```sh
./main -m ~/ai/models/llama-3.bin -p "What is 2+2?"
```

## Step 6: Build Frontend (Tauri + Svelte)
### 6.1 Install Tauri & Svelte
```sh
cargo install tauri-cli
npm create svelte@latest homeschool-ui
cd homeschool-ui
npm install
```

### 6.2 Build UI
Edit `src/App.svelte`:
```svelte
<script>
    let lesson = "Loading...";
    fetch("http://localhost:8080/lesson").then(res => res.text()).then(data => lesson = data);
</script>

<h1>Homeschool AI</h1>
<p>{lesson}</p>
```

Run frontend:
```sh
npm run dev
```

## Step 7: Backup System
### 7.1 GitHub/GitLab Sync
```sh
git init
git remote add origin https://github.com/YOUR_USERNAME/homeschool_ai.git
git add .
git commit -m "Initial commit"
git push origin main
```
### 7.2 Automatic Backup Script
Create `/usr/local/bin/backup.sh`:
```sh
#!/bin/bash
tar -czvf ~/backup.tar.gz ~/homeschool_ai ~/ai/models ~/data
scp ~/backup.tar.gz user@remote:/backups
```
Make it executable:
```sh
chmod +x /usr/local/bin/backup.sh
```
Schedule a weekly backup:
```sh
crontab -e
```
Add:
```sh
0 2 * * 0 /usr/local/bin/backup.sh
```

## Conclusion
This system ensures **offline-first homeschooling**, **AI-generated lessons**, and **long-term durability**. Updates can be pulled manually or **auto-synced when online**.

Next steps:
- Expand **lesson module structure**.
- Add **student progress tracking**.
- Improve **AI question-answering capabilities**.

This setup guarantees **educational continuity**, even in a **changing tech landscape**.

