#!/usr/bin/env python3
"""
Test runner script for Coffee Shop API.
Provides different test execution options.
"""

import subprocess
import sys
import argparse
from pathlib import Path


def run_command(cmd, description):
    """Run a command and handle errors."""
    print(f"\n{'='*50}")
    print(f"Running: {description}")
    print(f"Command: {' '.join(cmd)}")
    print(f"{'='*50}")
    
    try:
        result = subprocess.run(cmd, check=True, capture_output=False)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed with exit code {e.returncode}")
        return False


def main():
    parser = argparse.ArgumentParser(description="Run Coffee Shop API tests")
    parser.add_argument(
        "--type", 
        choices=["unit", "integration", "all", "coverage"],
        default="all",
        help="Type of tests to run"
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Run tests in verbose mode"
    )
    parser.add_argument(
        "--fast",
        action="store_true",
        help="Skip slow tests"
    )
    
    args = parser.parse_args()
    
    # Base pytest command
    base_cmd = ["uv", "run", "pytest"]
    
    if args.verbose:
        base_cmd.append("-v")
    
    if args.fast:
        base_cmd.extend(["-m", "not slow"])
    
    # Test type specific commands
    if args.type == "unit":
        cmd = base_cmd + ["tests/unit/"]
        description = "Unit Tests"
    elif args.type == "integration":
        cmd = base_cmd + ["tests/integration/"]
        description = "Integration Tests"
    elif args.type == "coverage":
        cmd = base_cmd + ["--cov=main", "--cov=models", "--cov-report=html", "--cov-report=term"]
        description = "Tests with Coverage"
    else:  # all
        cmd = base_cmd + ["tests/"]
        description = "All Tests"
    
    # Run the tests
    success = run_command(cmd, description)
    
    if args.type == "coverage" and success:
        print(f"\n📊 Coverage report generated in htmlcov/index.html")
    
    if not success:
        sys.exit(1)
    
    print(f"\n🎉 All tests completed successfully!")


if __name__ == "__main__":
    main()
