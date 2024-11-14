Here’s a detailed README file template tailored to your Jenkins CI/CD pipeline setup with AWS resources. This template includes all necessary sections, configurations, and instructions for setting up and maintaining the pipeline.

---

# Jenkins Multi-Branch Pipeline CI/CD with AWS

This project sets up a multi-branch Jenkins CI/CD pipeline on AWS, supporting development, staging, and production environments. The pipeline handles code build, scan, Docker image creation, ECR image storage, and deployment to EC2 instances, with GitHub webhooks for automated builds.

## Table of Contents
- [Architecture](#architecture)
- [Prerequisites](#prerequisites)
- [Setup Instructions](#setup-instructions)
  - [1. GitHub Repository Setup](#1-github-repository-setup)
  - [2. EC2 Instances for Jenkins](#2-ec2-instances-for-jenkins)
  - [3. IAM Roles and Policies](#3-iam-roles-and-policies)
  - [4. Jenkins Multi-Branch Pipeline Configuration](#4-jenkins-multi-branch-pipeline-configuration)
- [Pipeline Stages](#pipeline-stages)
- [Testing and Validation](#testing-and-validation)
- [Troubleshooting](#troubleshooting)

---

## Architecture

- **Jenkins Master & Slave EC2 Instances**: T3 large instances in the Canada (ca-central-1) region.
- **Jenkins Pipeline**: Multi-branch pipeline to automate CI/CD for different branches (dev, staging, main).
- **GitHub**: Hosted repository with branches for environment-specific code.
- **AWS Services**:
  - **IAM**: Role-based access control for Jenkins operations.
  - **ECR**: Docker image storage.
  - **EC2**: Hosts Jenkins and deploys containerized applications.

## Prerequisites

- AWS account with administrative access.
- GitHub account.
- SSH access to EC2 instances.
- Jenkins knowledge and basic Docker experience.

## Setup Instructions

### 1. GitHub Repository Setup

#### Step 1.1: Create GitHub Repository and Branches

1. **Repository**: Create a new repository to store your application code, Dockerfile, and `Jenkinsfile`.
2. **Branches**:
   - `main`: Production-ready code.
   - `staging`: Pre-production testing.
   - `dev`: Development.
3. **Branch Protection**:
   - Go to **Settings > Branches**.
   - Add branch protection rules for `dev`, `staging`, and `main` to require pull requests and status checks.

### 2. EC2 Instances for Jenkins

#### Step 2.1: Jenkins Master Setup

1. **Launch EC2 Instance**:
   - Instance type: Amazon Linux AMI, t3.large
   - Security Group: Allow ports 8080 (Jenkins) and 22 (SSH).
2. **Install Docker**:
   ```bash
   sudo yum update -y
   sudo yum install docker -y
   sudo service docker start
   sudo usermod -aG docker ec2-user
   ```
3. **Run Jenkins as a Docker Container**:
   ```bash
   docker pull jenkins/jenkins:lts
   docker run -d -p 8080:8080 -p 50000:50000 --name jenkins-master \
   -v jenkins_home:/var/jenkins_home \
   -v /var/run/docker.sock:/var/run/docker.sock \
   jenkins/jenkins:lts
   ```
4. **Set Up Jenkins**:
   - Retrieve the Jenkins initial password:
     ```bash
     docker exec -it jenkins-master cat /var/jenkins_home/secrets/initialAdminPassword
     ```
   - Access Jenkins: `http://<Jenkins-Master-EC2-Public-IP>:8080`.

#### Step 2.2: Jenkins Slave (Agent) Setup

1. **Launch Jenkins Agent EC2 Instance**:
   - Instance type: Amazon Linux AMI, t3.large
   - Security Group: Allow port 22 (SSH).
2. **Install Java and Docker**:
   ```bash
   sudo yum install -y java-1.8.0-openjdk docker
   sudo service docker start
   sudo usermod -aG docker ec2-user
   ```
3. **Configure SSH Access**:
   - Generate SSH key pair on the master instance and copy the public key to the agent instance.
   - Add Jenkins Agent in the Jenkins UI under **Manage Nodes and Clouds** with SSH credentials.

### 3. IAM Roles and Policies

1. **Create IAM Role**:
   - Role Name: `Jenkins-EC2-Role`
   - Policies: Attach `AmazonEC2ContainerRegistryFullAccess` and `SecretsManagerReadWrite`.
2. **Attach IAM Role**:
   - Assign the IAM role to both Jenkins Master and Slave EC2 instances.

### 4. Jenkins Multi-Branch Pipeline Configuration

1. **GitHub Webhook Setup**:
   - Go to **GitHub > Settings > Webhooks** and add the webhook URL: `http://<Jenkins-Master-EC2-Public-IP>:8080/github-webhook/`.
2. **Email Notification Setup**:
   - In Jenkins, go to **Manage Jenkins > Configure System**.
   - Configure SMTP settings (e.g., `smtp.gmail.com`).
3. **Multi-Branch Pipeline Creation**:
   - In Jenkins, go to **New Item** and select **Multi-branch Pipeline**.
   - Configure the pipeline to detect branches (`dev`, `staging`, `main`) and use the `Jenkinsfile` in the repository.

---

## Pipeline Stages

1. **Checkout**: Clones the code from GitHub.
2. **Build Docker Image**: Builds the Docker image for the application.
3. **Trivy Security Scan**: Runs a security scan using Trivy.
4. **Push to ECR**: Pushes the Docker image to AWS ECR.
5. **Cleanup Previous Containers**: Removes older versions of the container to free up resources.
6. **Test**: Deploys the application for testing.
7. **Deploy**: Deploys to production if the branch is `main`.

## Testing and Validation

1. **Create PRs**: Verify automatic triggers for `dev`, `staging`, and `main`.
2. **Email Notification**: Check for successful notifications after ECR pushes.
3. **Deployment Check**: Access deployed applications on each environment’s EC2 IP.

## Troubleshooting

- **403 Error for ECR**: Verify IAM roles and ensure permissions for ECR actions.
- **Pipeline Fails During Clone**: Check GitHub webhook and verify Git is installed on Jenkins agent.
- **Docker Permission Issues**: Ensure `ec2-user` is added to the Docker group on both master and slave instances.
