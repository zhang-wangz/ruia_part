from ruia import AttrField, TextField, Item, HtmlField

#定义爬取的地方
'''
Param	Rule	Description
target_item	tr.athing	表示每条资讯
title	a.storylink	表示每条资讯里的标题
url	a.storylink->href	表示每条资讯里标题的链接
'''
class HackerNewsItem(Item):
    target_item = TextField(css_select='tr.athing')
    title = TextField(css_select='a.storylink')
    url = AttrField(css_select='a.storylink', attr='href')
    content = HtmlField(css_select='a.storylink')