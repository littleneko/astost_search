#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tornado.web


class ItemModule(tornado.web.UIModule):
    def render(self, result_item):
        return self.render_string('modules/result_item.html', result_item=result_item)
