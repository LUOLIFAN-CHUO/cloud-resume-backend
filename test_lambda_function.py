import os

# 1. 必须在导入 lambda_function 之前设置好默认 Region！
os.environ['AWS_DEFAULT_REGION'] = 'ap-northeast-1'
os.environ['AWS_ACCESS_KEY_ID'] = 'testing'
os.environ['AWS_SECRET_ACCESS_KEY'] = 'testing'
os.environ['AWS_SECURITY_TOKEN'] = 'testing'
os.environ['AWS_SESSION_TOKEN'] = 'testing'

import json
import os
import boto3
from moto import mock_aws
import lambda_function

@mock_aws
def test_lambda_handler_spyccess():
    # 1. 模拟 AWS 环境
    os.environ['AWS_DEFAULT_REGION'] = 'ap-northeast-1'
    dynamodb = boto3.resource('dynamodb', region_name='ap-northeast-1')

    # 2. 在内存中创建一个假的 DynamoDB 表（表名要和 lambda_function.py 里的一致）
    table = dynamodb.create_table(
        TableName='cloud-resume-stats',
        KeySchema=[{'AttributeName': 'id', 'KeyType': 'HASH'}],
        AttributeDefinitions=[{'AttributeName': 'id', 'AttributeType': 'S'}],
        BillingMode='PAY_PER_REQUEST'
    )
    
    # 写入初始数据
    table.put_item(Item={'id': 'visitors', 'views': 5})
    
    # 3. 运行你的 Lambda 函数
    response = lambda_function.lambda_handler({}, None)
    
    # 4. 验证结果：5 + 1 应该等于 6，状态码应该为 200
    assert response['statusCode'] == 200
    body = json.loads(response['body'])
    assert body['views'] == 6