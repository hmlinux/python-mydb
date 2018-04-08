#/usr/bin/env python3
# -*- coding: utf-8 -*-
import os,sys

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(base_dir)

from core import main

if __name__ == '__main__':
    main.empInfoManageSystem()