import os
import sys

from agent_orchestrator import agent_loop
from config import Config

def test_notepad():
    print("=== Testing Notepad ===")
    try:
        agent_loop("open notepad and type Hello ForgeAI", max_steps=5)
    except SystemExit:
        pass

def test_browser():
    print("=== Testing Browser ===")
    try:
        agent_loop("open browser and go to example.com", max_steps=5)
    except SystemExit:
        pass

if __name__ == "__main__":
    Config.HEADLESS = True # Ensure headless if supported
    test_notepad()
    test_browser()
