# FastAPI Demo

A simple Python FastAPI demo project that provides REST API services.

## Prerequisites

- macOS
- Python 3.12+
- Docker (optional)

## Quick Start

### Option 1: Run Locally

1. **Install Python (if not installed)**
   ```bash
   brew install python@3.12
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   python app.py
   ```

4. **Test the API**
   ```bash
   curl http://localhost:8080/
   # Returns: Welcome to FastAPI Demo

   curl http://localhost:8080/hello
   # Returns: Hello from FastAPI
   ```

### Option 2: Run with Docker

1. **Build the image**
   ```bash
   docker build -t fastapidemo .
   ```

2. **Run the container**
   ```bash
   docker run -p 8080:8080 fastapidemo
   ```

3. **Test the API**
   ```bash
   curl http://localhost:8080/
   # Returns: Welcome to FastAPI Demo

   curl http://localhost:8080/hello
   # Returns: Hello from FastAPI
   ```

## API Endpoints

| Method | Path | Description | Response |
|--------|------|-------------|----------|
| GET | / | Welcome page | `Welcome to FastAPI Demo` |
| GET | /hello | Hello endpoint | `Hello from FastAPI` |

## Deploy to AWS ECS Fargate

This project includes a GitHub Actions workflow for automatic deployment to AWS ECS Fargate + ALB.

### GitHub Secrets Configuration

Configure the following Secrets in your GitHub repository (Settings → Secrets and variables → Actions):

| Secret Name | Required | Description |
|-------------|----------|-------------|
| `AWS_ACCESS_KEY_ID` | Yes | AWS IAM user Access Key ID with permissions for ECR, ECS, CloudFormation, EC2, ELB, IAM, CloudWatch Logs, etc. |
| `AWS_SECRET_ACCESS_KEY` | Yes | AWS IAM user Secret Access Key |
| `DOMAIN_NAME` | No | Your domain name (e.g., `api.example.com`), enables HTTPS when configured |
| `CERTIFICATE_ARN` | No | ACM Certificate ARN (e.g., `arn:aws:acm:us-east-1:123456789:certificate/xxx`) |

### Deployment

- Push code to the `main` branch to trigger automatic deployment
- Or manually trigger the workflow from the GitHub Actions page

**HTTP Mode (default):**
- Only requires `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY`
- ALB listens on port 80

**HTTPS Mode (optional):**
- Additionally configure `DOMAIN_NAME` and `CERTIFICATE_ARN` secrets
- ALB listens on port 443, port 80 automatically redirects to 443

### Deployment Configuration

- Default instance count: 1
- Default region: us-east-1
- Container port: 8080

## Project Structure

```
FastAPIDemo/
├── app.py                           # FastAPI application
├── requirements.txt                 # Python dependencies
├── Dockerfile                       # Docker build file
├── README.md                        # Project documentation
├── .gitignore                       # Git ignore file
└── .github/
    ├── workflows/
    │   └── deploy-ecs.yml           # GitHub Actions deployment workflow
    └── cloudformation/
        └── ecs-fargate-alb.yml      # AWS CloudFormation template
```

## Port

Default port: `8080`
