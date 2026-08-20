import time
from transformers import AutoModelForCausalLM, AutoTokenizer

MODEL = "HuggingFaceTB/SmolLM2-360M-Instruct"
PATH = "/generate"

tok = AutoTokenizer.from_pretrained(MODEL, local_files_only=True)
model = AutoModelForCausalLM.from_pretrained(MODEL, local_files_only=True)


def handle():
  prompt = "In one sentence, what is a data centre for?"

  # Encode prompt
  ids = tok(prompt, return_tensors="pt")
  prompt_len = ids["input_ids"].shape[1]  # Get input prompt token count

  t0 = time.perf_counter()

  # Generate text (min_new_tokens forces the model to generate actual text)
  out = model.generate(
      **ids, max_new_tokens=40, min_new_tokens=10, do_sample=False
  )

  dt = time.perf_counter() - t0

  # Get total tokens produced minus prompt length
  gen_tokens = out[0][prompt_len:]
  n = len(gen_tokens)

  # Decode only the generated response tokens
  sample_text = tok.decode(gen_tokens, skip_special_tokens=True).strip()

  return {
      "model": MODEL,
      "sample": sample_text,
      "seconds": round(dt, 2),
      "tokens_per_sec": round(n / dt, 1) if dt > 0 else 0,
  }