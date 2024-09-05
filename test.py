import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from transformers.generation.utils import GenerationConfig
tokenizer = AutoTokenizer.from_pretrained("FreedomIntelligence/HuatuoGPT2-34B", use_fast=True, trust_remote_code=True)
model = AutoModelForCausalLM.from_pretrained("FreedomIntelligence/HuatuoGPT2-34B", device_map="auto", torch_dtype="auto", trust_remote_code=True)
model.generation_config = GenerationConfig.from_pretrained("FreedomIntelligence/HuatuoGPT2-34B")
messages = []
messages.append({"role": "user", "content": "肚子疼怎么办？"})
response = model.HuatuoChat(tokenizer, messages)
print(response)

#test