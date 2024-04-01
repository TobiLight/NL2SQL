#!/usr/bin/env python3
# File: db.py
# Author: Oluwatobiloba Light
"""Database init"""
from prisma import Prisma


db = Prisma(auto_register=True)
