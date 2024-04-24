import torch
from peft import AutoPeftModelForCausalLM
from transformers import AutoTokenizer

peft_model_id = "./llama3-8b-hf-ft"
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Load Model with PEFT adapter
model = AutoPeftModelForCausalLM.from_pretrained(
  peft_model_id,
  torch_dtype=torch.bfloat16,
  quantization_config= {"load_in_4bit": True},
  device_map=device
)
tokenizer = AutoTokenizer.from_pretrained(peft_model_id)


from datasets import load_dataset
from random import randint

# Load our test dataset
eval_dataset = load_dataset("json", data_files="dataset/test_dataset.json", split="train")
rand_idx = randint(0, len(eval_dataset))
messages = eval_dataset[rand_idx]["messages"][:2]

# Test on sample
input_ids = tokenizer.apply_chat_template(messages,add_generation_prompt=True,return_tensors="pt").to(model.device)
outputs = model.generate(
    input_ids,
    max_new_tokens=1096,
    eos_token_id= tokenizer.eos_token_id,
    do_sample=True,
    temperature=0.1,
    top_p=0.9,
)
response = outputs[0][input_ids.shape[-1]:]

print(f"**Query:**\n{eval_dataset[rand_idx]['messages'][1]['content']}\n")
print(f"**Original Answer:**\n{eval_dataset[rand_idx]['messages'][2]['content']}\n")
print(f"**Generated Answer:**\n{tokenizer.decode(response,skip_special_tokens=True)}")

