# coding: utf-8
import xml.dom.minidom

"""
xml读取工具
author:CallMeE
date:2018-06-01
"""


class Mapper:
    _data = {}

    def sortTags(self, tree, name):
        tags = tree.getElementsByTagName(name)
        data = self._data
        for tag in tags:
            val = tag.childNodes[0].data
            attr = tag.getAttribute("id")
            data[attr] = val

    def openDom(self, file):
        # 使用minidom解析器打开 XML 文档
        DOMTree = xml.dom.minidom.parse(file)
        # tags=DOMTree.getElementsByTagName('')
        tags = DOMTree.documentElement
        # print(tags)
        # 取出标签(增删查改)
        self.sortTags(DOMTree, 'select')
        self.sortTags(DOMTree, 'delete')
        self.sortTags(DOMTree, 'insert')
        self.sortTags(DOMTree, 'update')
        # print(self._data)

    def getTree(self):
        return self._data



        # DOMTree = xml.dom.minidom.parse("movies.xml")
        # collection = DOMTree.documentElement
        # if collection.hasAttribute("shelf"):
        #     print("Root element : %s" % collection.getAttribute("shelf"))

        # # 在集合中获取所有电影
        # movies = collection.getElementsByTagName("movie")
        #
        # # 打印每部电影的详细信息
        # for movie in movies:
        #     print("*****Movie*****")
        #     if movie.hasAttribute("title"):
        #         print("Title: %s" % movie.getAttribute("title"))
        #
        #     type = movie.getElementsByTagName('type')[0]
        #     print("Type: %s" % type.childNodes[0].data)
        #     format = movie.getElementsByTagName('format')[0]
        #     print("Format: %s" % format.childNodes[0].data)
        #     rating = movie.getElementsByTagName('rating')[0]
        #     print("Rating: %s" % rating.childNodes[0].data)
        #     description = movie.getElementsByTagName('description')[0]
        #     print("Description: %s" % description.childNodes[0].data)

