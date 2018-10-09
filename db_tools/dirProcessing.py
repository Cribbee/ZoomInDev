# -*- coding: utf-8 -*-
__author__ = 'Cribbee'
__create_at__ = 2018 / 6 / 15

import os


def mkdir(self, floder):
    os.mkdir(floder)
    os.mkdir(floder + "\Data")
    os.mkdir(floder + "\Publish")
    os.mkdir(floder + "\Log")