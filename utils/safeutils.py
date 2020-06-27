# -*- coding: UTF-8 -*-

from urllib.parse import urlparse, urljoin
from flask import request, url_for


def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    print(request.host_url)
    print(ref_url)
    print(test_url)
    print(ref_url.netloc)
    return test_url.scheme in ('http', 'https') and ref_url.netloc == test_url.netloc
