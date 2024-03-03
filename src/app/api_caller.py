import json
import logging
import psycopg2

# TODO: these should be used SSM - Parameter Store instead
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
        cur.execute(""" select username as user, project,  cast(hours as varchar), to_char(timestamp, 'YYYY-mm-dd HH:SS')
                            from daily_checkins where username = '{}' ;""".format(username))
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
    for row in rows:
        tmp.append(dict(zip(cols, row)))
    return tmp
