#!/bin/bash

# Find and delete all __pycache__ directories
find . -type d -name "__pycache__" -exec rm -r {} +
