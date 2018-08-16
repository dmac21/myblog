# -*- coding: utf-8 -*-
# @Author  : dmac

class Test(object):

    #nickname = ''

    @property
    def name(self):
        return self.name

    @name.setter
    def name(self,name):
        self.nickname=name

test = Test()
test.name = 'dmac'
print(test.nickname)