# Quick Start Guide

## 🔑 Get FREE API Key (Google Gemini)

1. Visit: https://aistudio.google.com/app/apikey
2. Click "Create API Key"
3. Copy your key
4. Paste in `config.yaml` under `api_keys.google`

**No credit card required!** Gemini Flash has a generous free tier.

## 📝 Set Your Problem

Edit `PROBLEM.txt` with your problem statement:

```
Given an array of integers, find the maximum sum...

Input Format:
...

Output Format:
...

Constraints:
...
```

## 🚀 Run the Solver

```bash
python main.py
```

This will:
1. Load problem from `PROBLEM.txt`
2. Generate test cases
3. Create brute force solution
4. Iteratively generate optimal solutions (up to 5 attempts)
5. Save all attempts with verdicts
6. Generate `workspace/results.json`

## 🎨 View Results

### Option 1: Direct Open (Recommended for local files)
```bash
# Windows
start viewer.html

# macOS
open viewer.html

# Linux
xdg-open viewer.html
```

### Option 2: HTTP Server (Required for CORS if loading from file://)
```bash
python -m http.server 8000
```
Then visit: http://localhost:8000/viewer.html

## 📊 What You'll See

### Dashboard Stats
- ✓/✗ Success status
- Total attempts made
- Success rate percentage
- Accepted solutions count

### Problem Statement
- Formatted with LaTeX support
- Use `$formula$` or `$$formula$$` for math

### Test Data
- Input test cases
- Expected output (from brute force)

### Brute Force Solution
- Reference correct solution
- Syntax highlighted Python code

### Optimal Attempts (Reverse Order)
Each card shows:
- **Attempt Number**
- **Verdict Badge**:
  - 🟢 Accepted (Green)
  - 🔴 Wrong Answer (Red)
  - 🟠 Runtime Error (Orange)
  - ⚫ Generation Failed (Gray)
- **Code** (syntax highlighted)
- **Error Message** (if any)
- **"Show Output Diff"** button (for wrong answers)

### Diff Modal
Click "Show Output Diff" to see:
- Column 1: Input
- Column 2: Expected Output
- Column 3: Actual Output

## 🔧 Customize Your Problem

Edit `main.py` and change the `problem_statement` variable:

```python
problem_statement = """
Your problem here...

Input Format:
...

Output Format:
...

Constraints:
- Use $n \leq 10^5$ for LaTeX math
...
"""
```

Then run `python main.py` again and refresh the viewer!

## 📁 Generated Files

All in `workspace/`:
- `small_inputs.txt` - Test cases
- `brute.py` - Brute force solution
- `small_outputs.txt` - Expected outputs
- `optimal_attempt_1.py` - First attempt
- `optimal_attempt_1_output.txt` - First attempt output
- `optimal_attempt_2.py` - Second attempt
- ... (up to 10 attempts)
- `results.json` - **Viewer data**

## ⚙️ Configuration

Edit `config.yaml`:

```yaml
# Google Gemini (FREE!)
models:
  tester_agent: "google:gemini-2.5-flash"
  brute_agent: "google:gemini-2.5-flash"
  optimal_agent: "google:gemini-2.5-flash"

execution:
  max_optimal_attempts: 5                # Max retry count
  timeout_seconds: 30                    # Execution timeout
```

**Available Google Gemini Models (FREE Tier):**
- `google:gemini-2.5-flash` - Fast, efficient (250 free requests/day) ⭐
- `google:gemini-2.5-flash-lite` - Faster, cheaper (1000 free requests/day)
- `google:gemini-2.5-pro` - Most capable (100 free requests/day)

## 🐛 Troubleshooting

### "Loading results..." stuck
- Run `python main.py` first
- Check `workspace/results.json` exists
- Use HTTP server instead of file://

### Unicode errors on Windows
- Already fixed with UTF-8 encoding
- If still issues, use: `chcp 65001` before running

### Viewer not loading files
- Use HTTP server: `python -m http.server 8000`
- Files must be in `workspace/` directory

### API key errors
**For Google Gemini (FREE):**
- Get key at: https://aistudio.google.com/app/apikey
- Set in `config.yaml`: `api_keys.google: "your-key"`
- Or env var: `export GOOGLE_API_KEY="your-key"`

## 🎯 Example Workflow

```bash
# 1. Get FREE Gemini API key
# Visit: https://aistudio.google.com/app/apikey
# Add to config.yaml under api_keys.google

# 2. Run solver
python main.py

# 3. Check console output
# See attempts, verdicts, and success/failure

# 4. Open viewer
start viewer.html  # Windows
# or
python -m http.server 8000  # Then visit localhost:8000/viewer.html

# 5. Explore results
# - View all attempts in reverse order
# - Click "Show Output Diff" to debug
# - Check syntax-highlighted code
```

## 🌟 Tips

1. **LaTeX Math**: Use `$...$` for inline math, `$$...$$` for display math
2. **Small Test Cases**: TesterAgent generates 3-5 small cases for speed
3. **Feedback Loop**: Each failed attempt gets detailed feedback for next try
4. **All Saved**: Every attempt preserved - nothing is lost!
5. **Reverse Order**: Latest attempts shown first for easy access

Enjoy! 🎉
