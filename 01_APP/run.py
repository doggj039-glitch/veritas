# Copyright (c) contributors. Licensed under the Apache License, Version 2.0.
#!/usr/bin/env python3
"""
VERITAS — Startup Script
Constitutional analysis using dictionary-backed checks.
"""

import sys
import os

# Add project directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

if __name__ == "__main__":
    print("═" * 60)
    print("  VERITAS")
    print("  Report checks • dictionary definitions • plain-language output")
    print("═" * 60)
    print()
    print("Starting GUI...")
    
    from main import main
    main()
