# -*- coding: utf-8 -*-
"""
    website.helpers
    ~~~~~~~~~~~~~~~

    top level helpers.
"""


from flask import request


def log_request(sender, **extra):
    sender.logger.info('[Request Message]: %s %s %s',
                       request.method,
                       request.url,
                       request.data)


def log_exception(sender, exception, **extra):
    sender.logger.error('[Exception Request]: %s', exception)
