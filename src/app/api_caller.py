import json
import logging
import psycopg2

DATABASE_NAME = "tm"
HOST = "database-1.cluster-cqnnuqtyqggk.ap-southeast-1.rds.amazonaws.com"
USER = "prachya"
PASSWORD = "prachya2024"
PORT = "5432"

logger = logging.getLogger()
logger.setLevel("INFO")


class HttpMethodAllowed:
    GET = "GET"
    POST = "POST"


bad_request_msg = {
    'statusCode': 400,
    'body': json.dumps({"message": "error bad request"})
}


def lambda_handler(event, context):
    logger.info(event)
    http_method = event.get("httpMethod")

    if http_method != HttpMethodAllowed.GET:
        return bad_request_msg

    username = event.get("queryStringParameters").get("user")
    logger.info("username queried: {}".format(username))

    if not username:
        return bad_request_msg

    conn = psycopg2.connect(database=DATABASE_NAME,
                            host=HOST,
                            user=USER,
                            password=PASSWORD,
                            port=PORT)

    cur = conn.cursor()

    try:
        cur.execute(""" select username as user, project, hours, to_char(timestamp, 'YYYY-mm-dd HH:SS')
                        from daily_checking where username = '{}' ;""".format(username))
        column_names = [desc[0] for desc in cur.description]
        result = cur.fetchall()
        conn.commit()
    finally:
        cur.close()
        conn.close()
    response = assemble_response(column_names, result)
    return {
        'statusCode': 200,
        'body': json.dumps({
            "response": response
        })
    }


def assemble_response(cols, rows):
    tmp = []
    for row in rows:q
    return tmp


if __name__ == '__main__':
    request = {
        "resource": "/get",
        "path": "/get",
        "httpMethod": "GET",
        "headers": {
            "Accept": "*/*",
            "Accept-Encoding": "gzip, deflate, br",
            "Cache-Control": "no-cache",
            "CloudFront-Forwarded-Proto": "https",
            "CloudFront-Is-Desktop-Viewer": "true",
            "CloudFront-Is-Mobile-Viewer": "false",
            "CloudFront-Is-SmartTV-Viewer": "false",
            "CloudFront-Is-Tablet-Viewer": "false",
            "CloudFront-Viewer-ASN": "14618",
            "CloudFront-Viewer-Country": "US",
            "Host": "yef61g0li2.execute-api.ap-southeast-1.amazonaws.com",
            "Postman-Token": "75f11306-6b82-4e32-87cb-abfd6fccf8d5",
            "User-Agent": "PostmanRuntime/7.36.3",
            "Via": "1.1 9584642257cbfecd967367758cd3e13c.cloudfront.net (CloudFront)",
            "X-Amz-Cf-Id": "k08LUnbXbbvUcTT_zU9G-DwAFZTMoKHLhUF8pr-P8sWOaz6LBRKz0Q==",
            "X-Amzn-Trace-Id": "Root=1-65e30551-4ee81a9e5995ec75636fec2d",
            "X-Forwarded-For": "54.86.50.139, 15.158.50.237",
            "X-Forwarded-Port": "443",
            "X-Forwarded-Proto": "https"
        },
        "multiValueHeaders": {
            "Accept": [
                "*/*"
            ],
            "Accept-Encoding": [
                "gzip, deflate, br"
            ],
            "Cache-Control": [
                "no-cache"
            ],
            "CloudFront-Forwarded-Proto": [
                "https"
            ],
            "CloudFront-Is-Desktop-Viewer": [
                "true"
            ],
            "CloudFront-Is-Mobile-Viewer": [
                "false"
            ],
            "CloudFront-Is-SmartTV-Viewer": [
                "false"
            ],
            "CloudFront-Is-Tablet-Viewer": [
                "false"
            ],
            "CloudFront-Viewer-ASN": [
                "14618"
            ],
            "CloudFront-Viewer-Country": [
                "US"
            ],
            "Host": [
                "yef61g0li2.execute-api.ap-southeast-1.amazonaws.com"
            ],
            "Postman-Token": [
                "75f11306-6b82-4e32-87cb-abfd6fccf8d5"
            ],
            "User-Agent": [
                "PostmanRuntime/7.36.3"
            ],
            "Via": [
                "1.1 9584642257cbfecd967367758cd3e13c.cloudfront.net (CloudFront)"
            ],
            "X-Amz-Cf-Id": [
                "k08LUnbXbbvUcTT_zU9G-DwAFZTMoKHLhUF8pr-P8sWOaz6LBRKz0Q=="
            ],
            "X-Amzn-Trace-Id": [
                "Root=1-65e30551-4ee81a9e5995ec75636fec2d"
            ],
            "X-Forwarded-For": [
                "54.86.50.139, 15.158.50.237"
            ],
            "X-Forwarded-Port": [
                "443"
            ],
            "X-Forwarded-Proto": [
                "https"
            ]
        },
        "queryStringParameters": {
            "user": "foo"
        },
        "multiValueQueryStringParameters": {
            "user": [
                "foo"
            ]
        },
        "pathParameters": "None",
        "stageVariables": "None",
        "requestContext": {
            "resourceId": "w0slou",
            "resourcePath": "/get",
            "httpMethod": "GET",
            "extendedRequestId": "T_3EvE38yQ0EFQg=",
            "requestTime": "02/Mar/2024:10:54:09 +0000",
            "path": "/Prod/get",
            "accountId": "342076896000",
            "protocol": "HTTP/1.1",
            "stage": "Prod",
            "domainPrefix": "yef61g0li2",
            "requestTimeEpoch": 1709376849233,
            "requestId": "b538fef0-3488-474f-8782-8381ade99d8d",
            "identity": {
                "cognitoIdentityPoolId": "None",
                "accountId": "None",
                "cognitoIdentityId": "None",
                "caller": "None",
                "sourceIp": "54.86.50.139",
                "principalOrgId": "None",
                "accessKey": "None",
                "cognitoAuthenticationType": "None",
                "cognitoAuthenticationProvider": "None",
                "userArn": "None",
                "userAgent": "PostmanRuntime/7.36.3",
                "user": "None"
            },
            "domainName": "yef61g0li2.execute-api.ap-southeast-1.amazonaws.com",
            "apiId": "yef61g0li2"
        },
        "body": "None",
        "isBase64Encoded": False
    }
    lambda_handler(request, "")
