#!/usr/bin/env python
"""
Wrapper script to run the TBATS fertility rate prediction.
This script makes it easier to run the application from the command line.
"""

import sys
from predict_data.main import main

if __name__ == '__main__':
    # Pass any command line arguments to the main function
    result = main()
    sys.exit(0 if result else 1)