#!/usr/bin/env python
# -*- coding: utf-8 -*-


import tornado.web

import pymysql.cursors

from sphinx_client import *


class ResultHandler(tornado.web.RequestHandler):

    """
    处理搜索请求,查询sphinx
    """

    def __init__(self):

    def initialize(self):
        self.__cl = AstostSphinxClient()

    @tornado.gen.coroutine
    def get(self):
        key_word = self.get_argument('key').encode('utf-8')
        self.__cl.set_filter_fid(ALL_MUSIC)
        res = self.__cl.search(key_word, 0)

        if not res:
            self.write('Error')

        result = {'key_word': key_word, 'count': res['total_found'], 'time': res['time']}

        tids = [match['id'] for match in res['matches']] if res.has_key('matches') else None

        if tids is not None:
            sql_res =

        self.render('result.html', result=result, result_items=result_items)
