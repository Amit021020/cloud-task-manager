Cloud Task Manager - DevOps Deployment Project

Overview

Cloud Task Manager is a sample Flask application created to demonstrate a complete DevOps workflow. The primary focus of this project is not the application itself, but the infrastructure, automation, containerization, orchestration, and monitoring built around it.

The project showcases how an application can be containerized using Docker, deployed on Kubernetes, automated using GitHub Actions, and monitored with Prometheus and Grafana.

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
GitHub Actions
    │
    ▼
Docker Image
    │
    ▼
Docker Hub
    │
    ▼
Kubernetes (Kind)
    │
    ▼
Flask Application
    │
    ▼
Prometheus
    │
    ▼
Grafana

⸻

Features

* Containerized Flask application using Docker
* Automated CI pipeline with GitHub Actions
* Docker image build and push to Docker Hub
* Kubernetes Deployment and Service
* Multiple application replicas
* Resource requests and limits for containers
* Monitoring with Prometheus
* Visualization using Grafana
* Local Kubernetes cluster using Kind

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

Verify the deployment

kubectl get pods
kubectl get services

⸻

Monitoring

The project includes a monitoring stack deployed using Helm.

Components

* Prometheus
* Grafana
* kube-state-metrics
* Node Exporter

These components provide visibility into:

* Kubernetes cluster health
* Pod status
* CPU usage
* Memory usage
* Application metrics

⸻

CI Pipeline

The GitHub Actions workflow automatically:

* Checks out the source code
* Installs project dependencies
* Builds the Docker image
* Pushes the image to Docker Hub

⸻

Skills Demonstrated

* Docker Containerization
* Kubernetes Deployments
* Kubernetes Services
* Helm
* GitHub Actions
* CI/CD
* Docker Hub
* Prometheus Monitoring
* Grafana Dashboards
* Linux
* Git & GitHub
* Troubleshooting Kubernetes deployments

⸻

Future Improvements

* Automatic Kubernetes deployment after CI
* Application testing in the CI pipeline
* Image versioning strategy
* Production-ready Kubernetes manifests
* Cloud deployment on AWS, Azure, or Google Cloud

⸻

Author

Amit Suyal

If you found this project helpful, feel free to star the repository.