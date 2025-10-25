# Setting Up Google Gemini (FREE!)

## Why Gemini?

✅ **FREE tier** with generous limits
✅ **No credit card** required
✅ **Fast performance** with Gemini 1.5 Flash
✅ **Great quality** for coding tasks

## Step-by-Step Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

This installs:
- `langchain` - Base framework
- `langchain-google-genai` - Google Gemini integration
- `pyyaml` - Configuration parsing

### 2. Get Your FREE API Key

1. **Visit**: https://aistudio.google.com/app/apikey
2. **Sign in** with your Google account
3. **Click** "Create API Key"
4. **Copy** the generated key (starts with `AI...`)

**Note**: No credit card required! The free tier is very generous.

### 3. Configure the System

Open `config.yaml` and add your key:

```yaml
api_keys:
  google: "AIza...your-key-here"  # Paste your key
```

### 4. Verify Models are Set

Ensure your `config.yaml` has Gemini models configured:

```yaml
models:
  tester_agent: "google:gemini-2.5-flash"
  brute_agent: "google:gemini-2.5-flash"
  optimal_agent: "google:gemini-2.5-flash"
```

### 5. Test It!

```bash
python main.py
```

You should see:
```
================================================================================
STEP 1: Generating test cases...
================================================================================
✓ Test cases saved to: ./workspace\small_inputs.txt
...
```

## Free Tier Limits

Gemini 2.5 Flash FREE tier (check https://ai.google.dev/gemini-api/docs/rate-limits for latest):
- **250 requests per day**
- Generous token limits

This is **more than enough** for solving programming problems!

## Model Options

### Gemini 2.5 Flash (Recommended - FREE)
```yaml
models:
  tester_agent: "google:gemini-2.5-flash"
  brute_agent: "google:gemini-2.5-flash"
  optimal_agent: "google:gemini-2.5-flash"
```

**Pros**:
- ✅ FREE tier
- ✅ Very fast
- ✅ Great quality for coding
- ✅ Low latency

### Gemini 2.5 Flash Lite (FREE - More requests)
```yaml
models:
  tester_agent: "google:gemini-2.5-flash-lite"
  brute_agent: "google:gemini-2.5-flash-lite"
  optimal_agent: "google:gemini-2.5-flash-lite"
```

**Pros**:
- ✅ FREE tier
- ✅ 1000 free requests/day
- ✅ Faster and cheaper

**Cons**:
- ⚠️ Slightly less capable than Flash

### Gemini 2.5 Pro (Most Capable)
```yaml
models:
  optimal_agent: "google:gemini-2.5-pro"  # Use Pro for hardest problems
```

**Pros**:
- ✅ Most capable model
- ✅ Better reasoning
- ✅ Higher quality
- ✅ Still has FREE tier (100 requests/day)

**Cons**:
- ⏱️ Slightly slower

## Environment Variables (Alternative)

Instead of `config.yaml`, you can use environment variables:

**Windows (PowerShell)**:
```powershell
$env:GOOGLE_API_KEY="AIza...your-key"
python main.py
```

**Windows (CMD)**:
```cmd
set GOOGLE_API_KEY=AIza...your-key
python main.py
```

**Linux/macOS**:
```bash
export GOOGLE_API_KEY="AIza...your-key"
python main.py
```

## Troubleshooting

### "API key not valid"
- Make sure you copied the full key (starts with `AIza`)
- Check there are no extra spaces
- Verify the key is active in Google AI Studio

### "Rate limit exceeded"
- You hit the free tier limit (15 req/min)
- Wait 60 seconds and try again
- Or upgrade to paid tier

### "Module not found: langchain_google_genai"
```bash
pip install langchain-google-genai
```

### "Invalid model name"
Valid names:
- `google:gemini-2.5-flash` ✅
- `google:gemini-2.5-pro` ✅
- `gemini-2.5-flash` ❌ (missing `google:` prefix)
- `google/gemini-2.5-flash` ❌ (use `:` not `/`)

## Cost Comparison

| Model | Free Tier | Requests/Day |
|-------|-----------|--------------|
| **Gemini 2.5 Flash** | **✅ Yes** | 250 |
| **Gemini 2.5 Flash Lite** | **✅ Yes** | 1000 |
| **Gemini 2.5 Pro** | **✅ Yes** | 100 |

**All models have generous FREE tiers!** 🎉

## Performance Tips

1. **Use Flash for all agents** - It's fast and FREE
2. **Use Flash Lite for testing** - More free requests available
3. **Use Pro for very difficult problems** - Better reasoning
4. **Monitor usage** at https://aistudio.google.com

## Getting Help

- **Google AI Studio**: https://aistudio.google.com
- **Gemini Docs**: https://ai.google.dev/docs
- **LangChain Docs**: https://python.langchain.com/docs/integrations/chat/google_generative_ai

## Ready to Go!

```bash
python main.py
```

Enjoy FREE, fast programming problem solving! 🚀
