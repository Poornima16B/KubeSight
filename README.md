# ☸️ KubeSight — Enterprise Kubernetes Observability & GitOps Platform

[![Kubernetes](https://img.shields.io/badge/Kubernetes-v1.31-326CE5?logo=kubernetes&logoColor=white)](https://kubernetes.io/)
[![FastAPI](https://img.shields.io/badge/FastAPI-Python_3.11-009688?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/React-18-61DAFB?logo=react&logoColor=black)](https://react.dev/)
[![Docker](https://img.shields.io/badge/Docker-Compose-2496ED?logo=docker&logoColor=white)](https://www.docker.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-4169E1?logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![Azure](https://img.shields.io/badge/Deploy-Microsoft_Azure-0078D4?logo=microsoftazure&logoColor=white)](https://azure.microsoft.com/)

**KubeSight** is a comprehensive, multi-cluster Kubernetes observability, security posture management, and GitOps delivery platform. Designed to eliminate the complexity of raw `kubectl` command-line interfaces, KubeSight provides deep visibility into cluster health, live pod workloads, automated CIS security compliance, resource cost estimation, and interactive web terminals.

---

## 📸 Key Features

- **🖥️ Multi-Cluster Management:** Monitor local clusters (Docker Desktop, Kind, Minikube) or cloud-managed clusters (**AWS EKS**, **Azure AKS**, **Google Cloud GKE**, on-premise bare-metal).
- **🛡️ Security & Compliance Auditing:** Automated CIS Kubernetes Benchmark checks, Pod Security Standards verification, RBAC permission auditing, and secret expiration tracking.
- **💰 Real-Time Cost Analysis:** Granular cost allocation by namespace and workloads with rightsizing recommendations in Indian Rupees (**₹**).
- **⚡ In-Browser Kubectl Terminal:** Execute live `kubectl` and shell commands directly from the web browser with built-in safety guardrails.
- **🚀 GitOps & CI/CD Pipelines:** Native integrations with ArgoCD and Jenkins for visual release tracking and deployment rollbacks.
- **📈 Cluster Health & Resource Metrics:** Real-time CPU and memory utilization metrics across nodes and pods with automated capacity fallbacks.
- **👥 Role-Based Access Control (RBAC):** Multi-tier user management (`Admin`, `Operator`, `Developer`, `Viewer`) with secure JWT authentication and audit trails.

---

## 🏗️ Architecture Overview

```
┌────────────────────────────────────────────────────────┐
│                   CLIENT BROWSER                       │
│     React 18 + Vite + Tailwind CSS + WebSockets        │
│                (Port: 3001 or 80)                      │
└───────────────────────────┬────────────────────────────┘
                            │ Reverse Proxy / REST & WS
┌───────────────────────────▼────────────────────────────┐
│                    NGINX PROXY                         │
│       Routes frontend SPA & proxies /api to Backend    │
└───────────────────────────┬────────────────────────────┘
                            │
┌───────────────────────────▼────────────────────────────┐
│                  FASTAPI BACKEND                       │
│        Python 3.11 Async Engine (Port: 8000)           │
│   Auth • K8s Service • Cost Service • Security Scanner │
└─────────────┬───────────────────────────┬──────────────┘
              │                           │
     ┌────────▼────────┐        ┌─────────▼─────────────┐
     │   POSTGRESQL    │        │  KUBERNETES CLUSTER   │
     │      (16)       │        │  Live API & Kubelet   │
     │  Users & Audit  │        │ (Local, AKS, EKS)     │
     └─────────────────┘        └───────────────────────┘
```

---

## 🛠️ Tech Stack

| Layer | Technologies |
|---|---|
| **Frontend** | React 18, TypeScript, Vite, Tailwind CSS, Lucide Icons, Headless UI |
| **Backend** | Python 3.11, FastAPI, SQLAlchemy 2.0 (Async), Alembic, Pydantic v2 |
| **Datastores** | PostgreSQL 16, Redis 7 (caching & session store) |
| **Kubernetes API** | `kubernetes-asyncio`, official Python Kubernetes SDK, `kubectl` |
| **DevOps / Hosting** | Docker, Docker Compose, Microsoft Azure (VM / AKS), Nginx |

---

## 🚀 Quick Start (Local Setup)

### Prerequisites
- [Docker Desktop](https://www.docker.com/products/docker-desktop/) (with Kubernetes enabled, or Kind/Minikube)
- [Git](https://git-scm.com/)

### 1. Clone the Repository
```bash
git clone https://github.com/Poornima16B/KubeSight.git
cd KubeSight
```

### 2. Configure Environment Variables
Create a `.env` file in the project root:
```env
GROQ_API_KEY=your_groq_api_key_here
```

### 3. Launch with Docker Compose
```bash
docker-compose up -d
```

### 4. Access the Dashboard
- **URL:** [http://localhost:3001](http://localhost:3001)
- **Default Username:** `admin`
- **Default Password:** `admin123`

---

## ☁️ Deployment on Microsoft Azure

Deploying KubeSight on an Azure Virtual Machine provides an instantly accessible public endpoint for reviews and presentations:

1. **Create an Ubuntu VM in Azure Portal:**
   - Image: **Ubuntu Server 22.04 LTS (x64)**
   - Size: `Standard_B2s` (2 vCPUs, 4 GiB memory — eligible for Azure Student credits)
   - Inbound ports: **SSH (22)**, **HTTP (80)**

2. **Open Port 3001 in Azure Network Security Group (NSG):**
   - In your VM's **Network settings**, add an inbound rule for destination port `3001` (TCP, Allow).

3. **SSH into the VM & Run:**
   ```bash
   # Install Docker & Docker Compose
   sudo apt update && sudo apt install -y docker.io docker-compose
   sudo usermod -aG docker $USER
   newgrp docker

   # Clone & Launch KubeSight
   git clone https://github.com/Poornima16B/KubeSight.git
   cd KubeSight
   docker-compose up -d
   ```

4. **Access Live:**
   Navigate to `http://<YOUR_AZURE_PUBLIC_IP>:3001` in any browser.

---

## 🛡️ Security Audit & Finding Categories

KubeSight scans clusters for critical misconfigurations and compliance violations:

- **Workload Security:** Detects containers running with root privileges (`UID 0`), missing read-only root filesystems, and excessive Linux capabilities.
- **Network & Exposure:** Identifies services exposed directly via public `LoadBalancer` rather than governed ingress controllers.
- **Secret Management:** Flags unrotated Kubernetes secrets older than 90 days.
- **CIS Benchmarks:** Automated checks for anonymous authentication, RBAC policy bindings, and namespace workload isolation.

---

## 📁 Repository Structure

```text
KubeSight/
├── backend/
│   ├── alembic/                # Database migrations
│   ├── app/
│   │   ├── api/routes/         # REST API endpoints (Kubernetes, Auth, Cost, Security)
│   │   ├── core/               # Security, DB connections, configs
│   │   ├── models/             # SQLAlchemy ORM models
│   │   ├── schemas/            # Pydantic data validation schemas
│   │   └── services/           # Business logic & K8s client integrations
│   ├── requirements.txt        # Python dependencies
│   └── entrypoint.sh           # Container startup & migration script
├── frontend/
│   ├── dist/                   # Production-compiled React application
│   └── nginx.conf              # Nginx web server & reverse proxy configuration
├── docker-compose.yml          # Container orchestration manifest
├── .gitignore
└── README.md
```

---

## 🔒 Default Credentials

| Username | Password | Role | Description |
|---|---|---|---|
| `admin` | `admin123` | **Admin** | Full cluster management, security scans, user management |

---

## 📄 License
This project is developed for educational and enterprise cluster observability purposes.
