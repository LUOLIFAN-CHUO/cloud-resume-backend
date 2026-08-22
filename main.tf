# 1. 指定 AWS Provider 基础信息
terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = "ap-northeast-1" 
}

# 2. 定义 DynamoDB 数据库表
resource "aws_dynamodb_table" "stats_table" {
  name         = "cloud-resume-stats"
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "id"

  attribute {
    name = "id"
    type = "S"
  }
}

# 3. 创建 Lambda 函数所需的 IAM 执行角色（Role）
resource "aws_iam_role" "lambda_role" {
  name = "cloud_resume_lambda_role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "lambda.amazonaws.com"
        }
      }
    ]
  })
}

# 4. 给 Lambda 角色注入读写 DynamoDB 及写入 CloudWatch 日志的权限
resource "aws_iam_role_policy" "lambda_policy" {
  name = "cloud_resume_lambda_policy"
  role = aws_iam_role.lambda_role.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "dynamodb:GetItem",
          "dynamodb:UpdateItem",
          "dynamodb:PutItem"
        ]
        Resource = aws_dynamodb_table.stats_table.arn
      },
      {
        Effect = "Allow"
        Action = [
          "logs:CreateLogGroup",
          "logs:CreateLogStream",
          "logs:PutLogEvents"
        ]
        Resource = "arn:aws:logs:*:*:*"
      }
    ]
  })
}

# 5. 打包 Python 核心代码为 zip
data "archive_file" "lambda_zip" {
  type        = "zip"
  source_file = "${path.module}/lambda_function.py"
  output_path = "${path.module}/lambda_function.zip"
}

# 6. 定义 AWS Lambda 函数
resource "aws_lambda_function" "stats_lambda" {
  filename         = data.archive_file.lambda_zip.output_path
  function_name    = "cloud-resume-counter"
  role             = aws_iam_role.lambda_role.arn
  handler          = "lambda_function.lambda_handler"
  source_code_hash = data.archive_file.lambda_zip.output_base64sha256
  runtime          = "python3.13"
}