#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Multi-Agent Programming Problem Solver

This system uses three specialized agents to solve programming problems:
1. TesterAgent: Generates small test cases
2. BruteAgent: Creates a correct but potentially inefficient solution
3. OptimalAgent: Iteratively develops an efficient solution
"""

import sys
import io
from orchestrator import ProblemSolverOrchestrator

# Ensure UTF-8 encoding for Windows console
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')


def main():
    # Read problem statement from file
    problem_file = "PROBLEM.txt"

    try:
        with open(problem_file, 'r', encoding='utf-8') as f:
            problem_statement = f.read().strip()
    except FileNotFoundError:
        print(f"Error: {problem_file} not found!")
        print(f"Please create a {problem_file} file with your problem statement.")
        return 1

    print("Multi-Agent Programming Problem Solver")
    print("=" * 80)
    print(f"\nProblem loaded from: {problem_file}")
    print("\n" + problem_statement)
    print("\n")

    # Initialize orchestrator
    orchestrator = ProblemSolverOrchestrator()

    # Solve the problem
    success, optimal_code, metadata = orchestrator.solve(problem_statement)

    # Print results
    print("\n" + "=" * 80)
    print("FINAL RESULTS")
    print("=" * 80)
    print(f"Success: {success}")
    print(f"Attempts used: {metadata['attempts']}/{orchestrator.max_attempts}")
    print(f"Test cases generated: {metadata['test_cases_generated']}")
    print(f"Brute force generated: {metadata['brute_force_generated']}")
    print(f"Brute force executed: {metadata['brute_force_executed']}")
    print(f"Optimal solution found: {metadata['optimal_solution_found']}")

    if metadata['errors']:
        print(f"\nErrors encountered: {len(metadata['errors'])}")
        for i, error in enumerate(metadata['errors'], 1):
            print(f"  {i}. {error}")

    if success and optimal_code:
        print("\n" + "=" * 80)
        print("OPTIMAL SOLUTION CODE:")
        print("=" * 80)
        print(optimal_code)
        print("\n")
        print(f"Solution saved to: {orchestrator.files['optimal_solution']}")
    else:
        print("\nFailed to find a working solution.")
        if orchestrator.files['brute_solution']:
            print(f"Brute force solution available at: {orchestrator.files['brute_solution']}")

    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())
