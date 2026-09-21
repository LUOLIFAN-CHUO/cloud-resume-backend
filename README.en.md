# Cloud Resume Challenge — Backend

[日本語](./README.md) | English

An AWS serverless API that records Cloud Resume visits. API Gateway, a Python Lambda function, and DynamoDB are provisioned with Terraform.

**Demo:** https://dyp8879eswsdu.cloudfront.net/

## System architecture

[![AI-Powered Cloud Portfolio architecture](docs/architecture/AI-Powered-Cloud-Portfolio.png)](docs/architecture/AI-Powered-Cloud-Portfolio.html)

Click the image to open the interactive diagram. This repository owns the visitor-counter path shown in the architecture.

```text
Portfolio UI
  → GET /count
  → Amazon API Gateway
  → AWS Lambda (Python)
  → DynamoDB UpdateItem (ADD)
  → { "views": number }
```

## Design highlights

- Atomic counter updates with DynamoDB `UpdateItem` and `ADD`
- IAM policy scoped to Lambda's DynamoDB access
- Synchronous API Gateway-to-Lambda invocation
- Browser-compatible CORS response
- Python 3.13 runtime
- Reproducible infrastructure managed with Terraform

## Key files

```text
lambda_function.py        Lambda handler that increments and returns the count
test_lambda_function.py   Lambda unit tests
main.tf                   DynamoDB, IAM, Lambda, and API Gateway resources
```

## API response

```json
{
  "views": 123
}
```

## Tests

```powershell
python -m pytest -p no:cacheprovider
```

## Terraform

```powershell
terraform fmt -check
terraform init
terraform validate
terraform plan
```

Terraform state, generated ZIP files, and AWS credentials must not be committed. Production deployment should use GitHub OIDC or securely managed secrets.

## Related repositories

- [cloud-resume-frontend](https://github.com/LUOLIFAN-CHUO/cloud-resume-frontend) — resume site that displays the counter
- [rag-practice](https://github.com/LUOLIFAN-CHUO/rag-practice) — resume RAG assistant

## Architecture artifacts

- [Interactive HTML](docs/architecture/AI-Powered-Cloud-Portfolio.html)
- [Archify source specification](docs/architecture/AI-Powered-Cloud-Portfolio.architecture.json)
- [PNG preview](docs/architecture/AI-Powered-Cloud-Portfolio.png)
