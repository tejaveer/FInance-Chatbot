from transformers import AutoModelForCausalLM, AutoTokenizer

# Gemma 2B (general tasks)
gemma_model = "google/gemma-2b"
print("⬇️ Downloading Gemma 2B...")
AutoTokenizer.from_pretrained(gemma_model)
AutoModelForCausalLM.from_pretrained(gemma_model)
print("✅ Gemma 2B downloaded!")

# FinGPT small (finance-specific tasks)
fingpt_model = "FinGPT/fingpt-1.3b"   # Or use a 2B version if laptop can handle
print("⬇️ Downloading FinGPT...")
AutoTokenizer.from_pretrained(fingpt_model)
AutoModelForCausalLM.from_pretrained(fingpt_model)
print("✅ FinGPT downloaded!")
