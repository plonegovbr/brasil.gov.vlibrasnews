# -*- coding: utf-8 -*-
from httmock import all_requests
from requests.exceptions import RequestException

import json


response_ok = {
    2: {
        'publish': {
            'POST': {
                'success': (
                    'Received request. The process will be performed in the '
                    'background.')
            }
        }
    },
    3: {
        'publish': {
            'PUT': {
                'success': (
                    'Received request. The process will be performed '
                    'in the background.')
            }

        },
        'videos': {
            'GET': {
                'url_youtube': 'https://www.youtube.com/embed/ds2gGAbPJz8'
            },
            'DELETE': {
                'success': 'Successfully deleted video.'
            }
        }
    }
}


@all_requests
def vlibras_ok(url, request):
    url_path = url.path.split('/')
    content = response_ok[len(url_path)][url_path[1]][request.method]
    return {'status_code': 200, 'reason': 'OK', 'content': json.dumps(content)}


@all_requests
def vlibras_error(url, request):
    content = {
        'unauthorized': 'The request requires user authentication.'
    }
    return {
        'status_code': 401, 'reason': 'UNAUTHORIZED', 'content': json.dumps(content)}


@all_requests
def vlibras_processing(url, request):
    content = {
        'stillProcessing': (
            'The video generation is still running. Try again after a '
            'few minutes.')
    }
    return {'status_code': 102, 'content': json.dumps(content)}


@all_requests
def request_exception(url, request):
    raise RequestException('Request ERROR on URL {0}'.format(url), request=request)
