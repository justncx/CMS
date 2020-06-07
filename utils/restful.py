# -*- coding: UTF-8 -*-
from flask import jsonify


class HttpCode(object):
    ok = 200
    unautherror = 401
    paramserror = 400
    servererror = 500


def restfule_result(code=None, message=None, data=None):
    return jsonify({'code': code, 'message': message, 'data': data or {}})

def success(message="", data=None):
    return restfule_result(code=HttpCode.ok, message=message, data=data)

def unautherror(message=""):
    return restfule_result(code=HttpCode.unautherror, message=message, data=None)

def servererror(message=""):
    return restfule_result(code=HttpCode.servererror, message=message, data=None)

def paramerror(message=""):
    return restfule_result(code=HttpCode.paramserror, message=message, data=None)
