#!/usr/bin/env python
# -*- coding: utf-8 -*-


import tornado.web
import tornado_mysql

from sphinx_client import *

from setting import *


sql_cmd = 'SELECT ' \
          'post.tid, post.title, post.fid, post.uid, post.user, post.post_time, post_content.content ' \
          'FROM post LEFT JOIN post_content ON post.tid = post_content.tid WHERE post.tid IN (%s)' \
          'ORDER BY FIND_IN_SET(post.tid, "%s")'


fid_str_nu = {'新作资源': '50', '游戏音乐': '4', '动画音乐': '5', '同人音乐': '42',
              '综合音乐': '8', '广播剧': '25', 'Hi-Res自购资源交流': '52', 'Hi-Res&Hi-Fi讨论': '53',
              'EX咖喱版': '49'}

fid_param_to_str = {'new': NEW_PRODUCTION, 'game': GAME_MUSIC, 'anime': ANIME_MUSIC, 'doujin': DOUJIN_MUSIC,
                    'comp': COMPOSITE_MUSIC, 'radio': RADIO, 'hi1': HI_RES_1, 'hi2': HI_RES_2,
                    'ex': EX}

excerpt_opts = {'before_match': '<em>', 'after_match': '</em>', 'limit_words': 300}


class ResultHandler(tornado.web.RequestHandler):

    """
    处理搜索请求,查询sphinx
    """

    def initialize(self):
        self.__re_html = re.compile(r'<[^>]+>', re.S)

    @tornado.gen.coroutine
    def get(self):
        key_word = self.get_argument('key', '').encode('utf-8')
        pn = self._check_argument_pn(self.get_argument('pn', 1))
        ex = self.get_argument('ex', '')
        fid = self.__check_fid(self.get_argument('fid', 'all').encode('utf-8'))

        if len(key_word) < 2:
            self.write('关键字长度必须大于两个字符!!!')
            return

        # sphinx client
        cl = AstostSphinxClient()
        cl.set_filter_fid(ALL_MUSIC)
        if ex != 'on':
            cl.open_ex(False)
        if fid != 'all':
            cl.set_filter_fid(fid_param_to_str.get(fid, 0x00))
        res = yield cl.search(key_word, (pn-1)*10)

        if not res:
            self.write('Something maybe wrong, Please wait some seconds!')
            return

        # result need
        result = {'key_word': key_word, 'pn': pn, 'fid': fid, 'count': res['total_found'], 'time': res['time']}

        result_items = None

        if 'matches' in res.keys() and res['total'] > 0:

            tids = [str(match['id']) for match in res['matches']] if 'matches' in res.keys() else None

            result_items = []

            if len(tids) > 0:
                tid_sql_str = ','.join(tids)
                conn = yield tornado_mysql.connect(host=SQL_HOST, port=SQL_PORT,
                                                   user=SQL_USER, passwd=SQL_PWD,
                                                   db=DB, charset='utf8')
                cur = conn.cursor()
                yield cur.execute(sql_cmd % (tid_sql_str, tid_sql_str))

                for row in cur:
                    row = [row_item.encode('utf-8') if isinstance(row_item, unicode) else row_item for row_item in row]
                    row_excerpts = [row[1], row[6]]
                    row_excerpts[1] = self.__re_html.sub('', row_excerpts[1])
                    row_excerpts = cl.build_excerpts(row_excerpts, 'astost', key_word, excerpt_opts)
                    result_item = {'tid': row[0], 'title': row_excerpts[0] + '_' + row[2],
                                   'time': row[5], 'abstract': row_excerpts[1],
                                   'fid_str': row[2], 'fid_num': fid_str_nu.get(row[2], ''),
                                   'uid': row[3], 'user': row[4]}
                    result_items.append(result_item)
                cur.close()
                conn.close()

        self.render('result.html', result=result, result_items=result_items)

    @staticmethod
    def _check_argument_pn(pn):
        try:
            pn_p = int(pn)
        except ValueError:
            pn_p = 1

        pn_p = pn_p if pn_p > 0 else 1
        pn_p = pn_p if pn_p <= 100 else 100
        return pn_p

    @staticmethod
    def __check_fid(fid):
        if fid not in fid_param_to_str.keys():
            return 'all'
        return fid



