#!/usr/bin/env python
# -*- coding: utf-8 -*-


from sphinxapi import *

from setting import *

NEW_PRODUCTION = 0x01
GAME_MUSIC = 0x02
ANIME_MUSIC = 0x04
DOUJIN_MUSIC = 0x08
COMPOSITE_MUSIC = 0x10
RADIO = 0x20
HI_RES_1 = 0x40
HI_RES_2 = 0x80
EX = 0x100
ALL_MUSIC = 0x00


class AstostSphinxClient(object):

    # for sphinx
    mode = SPH_MATCH_EXTENDED
    limit = 10
    index = '*'

    def __init__(self):
        self.__cl = SphinxClient()
        self.__cus_init()

    def __cus_init(self):
        self.__cl.SetServer(SPHINX_HOST, SPHINX_PORT)
        self.__cl.SetMatchMode(AstostSphinxClient.mode)
        self.__cl.SetSortMode(SPH_SORT_EXTENDED, '@weight DESC, post_time DESC')
        # self.__cl.SetGroupBy(groupby, SPH_GROUPBY_ATTR, groupsort)

    def set_filter_fid(self, fid):
        self.__cl.ResetFilters()
        if fid & NEW_PRODUCTION:
            self.__cl.SetFilterString('fid', '新作资源')
        if fid & GAME_MUSIC:
            self.__cl.SetFilterString('fid', '游戏音乐')
        if fid & ANIME_MUSIC:
            self.__cl.SetFilterString('fid', '动画音乐')
        if fid & DOUJIN_MUSIC:
            self.__cl.SetFilterString('fid', '同人音乐')
        if fid & COMPOSITE_MUSIC:
            self.__cl.SetFilterString('fid', '综合音乐')
        if fid & RADIO:
            self.__cl.SetFilterString('fid', '广播剧')
        if fid & HI_RES_1:
            self.__cl.SetFilterString('fid', 'Hi-Res&Hi-Fi讨论')
        if fid & HI_RES_2:
            self.__cl.SetFilterString('fid', 'Hi-Res自购资源交流')
        if fid & EX:
            self.__cl.SetFilterString('fid', 'EX咖喱版')

    def open_ex(self, ex):
        if ex is False:
            # 排除EX版
            self.__cl.SetFilterString('fid', 'EX咖喱版', True)

    def search(self, key, start):
        self.__cl.SetLimits(start, AstostSphinxClient.limit, max(AstostSphinxClient.limit, 1000))
        res = self.__cl.Query('"' + key + '"/0.75', AstostSphinxClient.index)
        return res

    def build_excerpts(self, docs, index, words, opts=None):
        return self.__cl.BuildExcerpts(docs, index, words, opts)



