# Cloud Resume Challenge - Backend

## Overview
Visitor counter API.

## Architecture

<img width="1600" height="1550" alt="891b83e0fb75b8ad88abf7d6ef210ffc" src="https://github.com/user-attachments/assets/4ddc66a8-4e9b-4bc4-b1cb-8783e1b49466" />


API Gateway
    ↓
Lambda
    ↓
DynamoDB

## Tech Stack
- Python
- AWS Lambda
- API Gateway
- DynamoDB
- Terraform

## Infrastructure
Terraform manages:
- Lambda
- API Gateway
- DynamoDB
- IAM

## Testing
pytest
