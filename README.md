# Cloud Task Manager – DevOps Deployment Project

Overview

Cloud Task Manager is a sample Flask application designed to demonstrate an end-to-end DevOps workflow. The application itself is intentionally simple; the primary focus is on the surrounding infrastructure, automation, containerization, orchestration, and observability.

This project demonstrates how a Flask application can be containerized with Docker, deployed to Kubernetes, automated via GitHub Actions, and monitored using Prometheus and Grafana.

⸻

Tech Stack

Application

* Python
* Flask

DevOps & Cloud

* Docker
* Kubernetes (Kind)
* Helm
* GitHub Actions
* Prometheus
* Grafana

Version Control

* Git
* GitHub

⸻

Project Architecture

Developer
    │
    ▼
GitHub Repository
    │
    ▼
GitHub Actions (CI Pipeline)
    │
    ▼
Docker Image Build
    │
    ▼
Docker Hub Registry
    │
    ▼
Kubernetes Cluster (Kind)
    │
    ▼
Flask Application Pods
    │
    ▼
Prometheus (Metrics Collection)
    │
    ▼
Grafana (Visualization)

⸻

Features

* Dockerized Flask application
* CI pipeline using GitHub Actions
* Automated Docker image build and push to Docker Hub
* Kubernetes Deployment and Service configuration
* Scalable deployment with multiple replicas
* Resource requests and limits for containers
* Monitoring with Prometheus
* Dashboards with Grafana
* Local Kubernetes environment using Kind

⸻

Project Structure

cloud-task-manager/
│
├── .github/
│   └── workflows/
│       └── ci.yml
│
├── kubernetes/
│   ├── deployment.yaml
│   └── service.yaml
│
├── app.py
├── Dockerfile
├── requirements.txt
├── README.md
└── .gitignore

⸻

Getting Started

Clone the repository

git clone https://github.com/Amit021020/cloud-task-manager.git
cd cloud-task-manager

Build the Docker image

docker build -t cloud-task-manager .

Create a Kind cluster

kind create cluster --name cloud-project

Load the Docker image into Kind

kind load docker-image cloud-task-manager --name cloud-project

Deploy the application

kubectl apply -f kubernetes/

Verify deployment

kubectl get pods
kubectl get services

⸻

Monitoring

The monitoring stack is deployed using Helm.

Components

* Prometheus
* Grafana
* kube-state-metrics
* Node Exporter

Observability Coverage

* Kubernetes cluster health
* Pod status and lifecycle
* CPU utilization
* Memory usage
* Application-level metrics

⸻

CI Pipeline

The GitHub Actions workflow automates the following steps:

* Source code checkout
* Dependency installation
* Docker image build
* Docker image push to Docker Hub

⸻

Skills Demonstrated

* Docker containerization
* Kubernetes deployments and services
* Helm package management
* CI/CD with GitHub Actions
* Docker Hub image registry
* Prometheus monitoring
* Grafana dashboards
* Linux environment usage
* Git and GitHub workflows
* Kubernetes troubleshooting

⸻



⸻

Author

Amit Suyal

If you found this project useful, feel free to star the repository.