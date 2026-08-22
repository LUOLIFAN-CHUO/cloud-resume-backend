import json
import boto3

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('cloud-resume-stats')

def lambda_handler(event, context):
    try:
        # 更新并获取最新 views
        response = table.update_item(
            Key={'id': 'visitors'},
            UpdateExpression='ADD #v :incr',
            ExpressionAttributeNames={'#v': 'views'},
            ExpressionAttributeValues={':incr': 1},
            ReturnValues='UPDATED_NEW'
        )
        
        # 强制转为 int，确保数据类型绝对安全
        views_count = int(response['Attributes']['views'])
        
        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Headers': '*',
                'Access-Control-Allow-Methods': 'GET,OPTIONS'
            },
            'body': json.dumps({'views': views_count})
        }
    except Exception as e:
        print(f"Error: {str(e)}")
        return {
            'statusCode': 500,
            'headers': {
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({'error': str(e)})
        }