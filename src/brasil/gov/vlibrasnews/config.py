# -*- coding: utf-8 -*-
PROJECTNAME = 'brasil.gov.vlibrasnews'

REQUEST_TIMEOUT = 5

POST_URL = 'http://150.165.204.81:3000/publish'
REPOST_URL = 'http://150.165.204.81:3000/publish/{0}'
VIDEO_URL = 'http://150.165.204.81:3000/videos/{0}'

# by default, all standard content types will be enabled
DEFAULT_ENABLED_CONTENT_TYPES = [
    'Document',
    'News Item'
]
