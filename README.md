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
| `AWS_ROLE_ARN` | Yes | ARN of the IAM role assumed via GitHub OIDC (e.g., `arn:aws:iam::123456789:role/github-actions-deploy`) with permissions for ECR, ECS, CloudFormation, EC2, ELB, IAM, CloudWatch Logs, etc. |
| `DOMAIN_NAME` | No | Your domain name (e.g., `api.example.com`), enables HTTPS when configured |
| `CERTIFICATE_ARN` | No | ACM Certificate ARN (e.g., `arn:aws:acm:us-east-1:123456789:certificate/xxx`) |

### Configure IAM Role (OIDC)

Authentication uses GitHub OIDC, so no long-lived AWS keys are needed.

1. **Create the OIDC identity provider** (one-time per account) in IAM → Identity providers → Add provider:
   - Provider type: `OpenID Connect`
   - Provider URL: `https://token.actions.githubusercontent.com`
   - Audience: `sts.amazonaws.com`
2. **Create the IAM role** in IAM → Roles → Create role:
   - Trusted entity type: **Web identity**
   - Identity provider: `token.actions.githubusercontent.com`, Audience: `sts.amazonaws.com`
   - GitHub organization/repository/branch: your owner, `FastAPIDemo`, `main`
   - Attach permissions for ECR, ECS, CloudFormation, EC2, ELB, IAM, CloudWatch Logs
3. Copy the role ARN into the `AWS_ROLE_ARN` secret.

Or do it entirely from the CLI (replace `OWNER` with your GitHub org/username and the account ID `123456789`):

```bash
# 1. Create the OIDC identity provider (skip if it already exists)
aws iam create-open-id-connect-provider \
  --url https://token.actions.githubusercontent.com \
  --client-id-list sts.amazonaws.com

# 2. Write the trust policy
cat > trust-policy.json <<'EOF'
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Federated": "arn:aws:iam::123456789:oidc-provider/token.actions.githubusercontent.com"
      },
      "Action": "sts:AssumeRoleWithWebIdentity",
      "Condition": {
        "StringEquals": {
          "token.actions.githubusercontent.com:aud": "sts.amazonaws.com"
        },
        "StringLike": {
          "token.actions.githubusercontent.com:sub": "repo:OWNER/FastAPIDemo:ref:refs/heads/main"
        }
      }
    }
  ]
}
EOF

# 3. Create the role
aws iam create-role \
  --role-name github-actions-deploy \
  --assume-role-policy-document file://trust-policy.json

# 4. Attach permissions (PowerUserAccess is broad; scope it down for production)
aws iam attach-role-policy \
  --role-name github-actions-deploy \
  --policy-arn arn:aws:iam::aws:policy/PowerUserAccess
```

### Obtain AWS_ROLE_ARN

After creating the IAM role above, copy its ARN into the `AWS_ROLE_ARN` secret.

From the console: IAM → Roles → open your role → copy the **ARN** shown at the top (e.g., `arn:aws:iam::123456789:role/github-actions-deploy`).

Or from the CLI:

```bash
aws iam get-role \
  --role-name github-actions-deploy \
  --query "Role.Arn" --output text
```

Put that ARN into the `AWS_ROLE_ARN` secret.

### Deployment

- Push code to the `main` branch to trigger automatic deployment
- Or manually trigger the workflow from the GitHub Actions page

**HTTP Mode (default):**
- Only requires `AWS_ROLE_ARN`
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
