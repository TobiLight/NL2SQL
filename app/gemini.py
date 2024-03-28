#!/usr/bin/env python3
# File: gemini.py
# Author: Oluwatobiloba Light
"""Google Gemini AI"""


import google.generativeai as genai
from os import getenv

genai.configure(api_key=getenv("GOOGLE_API_KEY"), )

model = genai.GenerativeModel('gemini-pro')

chat = model.start_chat(history=[])
