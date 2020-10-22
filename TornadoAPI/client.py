from tornado.httpclient import HTTPClient, HTTPResponse, HTTPRequest
import json


def client_start():
    offset = 12
    while offset != 0:
        client = HTTPClient()
        request = HTTPRequest(f'http://localhost:3000/read_log', method="POST")
        request.body = json.dumps({"offset": offset if offset != -1 else 0})
        response: HTTPResponse = client.fetch(request)
        body = json.loads(response.body)
        if body['ok']:
            offset = body['next_offset']
            print(response.body)
            client.close()
        else:
            client.close()
            break


if __name__ == '__main__':
    client_start()
