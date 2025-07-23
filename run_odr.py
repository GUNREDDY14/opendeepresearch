#!/usr/bin/env python3
"""
Simple ODR Runner
Quick access to the complete research system
"""

from odr_main import run_interactive_research, run_quick_research

def main():
    print("🚀 ODR System - Quick Start")
    print("=" * 40)
    
    mode = input("Choose mode:\n1. Interactive Research\n2. Quick Research\nChoice (1/2): ")
    
    if mode == "1":
        print("\n🔍 Starting Interactive Research...")
        run_interactive_research()
    elif mode == "2":
        topic = input("Enter research topic: ")
        print(f"\n⚡ Starting Quick Research on: {topic}")
        run_quick_research(topic)
    else:
        print("❌ Invalid choice")

if __name__ == "__main__":
    main()
