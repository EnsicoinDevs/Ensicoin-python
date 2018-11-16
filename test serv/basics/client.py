# -*- coding: utf-8 -*-
"""
Created on Wed Nov 14 19:37:16 2018

@author: Admin
"""
import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((socket.gethostname(), 4224))