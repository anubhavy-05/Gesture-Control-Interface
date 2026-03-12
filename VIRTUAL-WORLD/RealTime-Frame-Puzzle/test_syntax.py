#!/usr/bin/env python3
"""
Quick syntax check for main.py
"""
import py_compile
import sys

try:
    py_compile.compile('main.py', doraise=True)
    print("✅ SUCCESS: No syntax errors found!")
    print("✅ Code is syntactically correct")
    sys.exit(0)
except py_compile.PyCompileError as e:
    print("❌ SYNTAX ERROR FOUND:")
    print(f"   File: {e.file}")
    print(f"   Error: {e.msg}")
    print(f"   Details: {e.exc_value}")
    sys.exit(1)
except Exception as e:
    print(f"❌ ERROR: {e}")
    sys.exit(1)
