#!/usr/bin/env python3
"""
Setup script for Meta HackerCup AI StarterKit.
"""
import os
import shutil
import sys


def setup_project():
    """Set up the project for first-time use."""
    print("Setting up Meta HackerCup AI StarterKit...")
    
    # Check if config.yaml exists
    if not os.path.exists('config.yaml'):
        if os.path.exists('config.template.yaml'):
            print("Creating config.yaml from template...")
            shutil.copy('config.template.yaml', 'config.yaml')
            print("✓ config.yaml created")
            print("⚠️  Please edit config.yaml and add your Google Gemini API key")
        else:
            print("❌ config.template.yaml not found")
            return False
    else:
        print("✓ config.yaml already exists")
    
    # Create workspace directory if it doesn't exist
    if not os.path.exists('workspace'):
        os.makedirs('workspace')
        print("✓ workspace directory created")
    else:
        print("✓ workspace directory already exists")
    
    # Check if PROBLEM.txt exists
    if not os.path.exists('PROBLEM.txt'):
        print("⚠️  PROBLEM.txt not found - you'll need to create this file with your problem statement")
    else:
        print("✓ PROBLEM.txt exists")
    
    print("\nSetup complete! Next steps:")
    print("1. Edit config.yaml and add your Google Gemini API key")
    print("2. Create or edit PROBLEM.txt with your problem statement")
    print("3. Run: python main.py")
    print("4. View results: python -m http.server 8000, then open http://localhost:8000/viewer.html")
    
    return True


if __name__ == '__main__':
    success = setup_project()
    sys.exit(0 if success else 1)
