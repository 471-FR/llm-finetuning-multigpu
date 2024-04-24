from peft import AutoPeftModelForCausalLM
import torch

output_dir="llama-3-8b-hf-ft"

# Load PEFT model on CPU
model = AutoPeftModelForCausalLM.from_pretrained(
    output_dir,
    torch_dtype=torch.float16,
    low_cpu_mem_usage=True,
)
# Merge LoRA and base model and save
merged_model = model.merge_and_unload()
merged_model.save_pretrained(output_dir,safe_serialization=True, max_shard_size="4GB")

# # save to s3 bucket
# import os
# import boto3
# from botocore.exceptions import NoCredentialsError

# def upload_to_aws(local_file, bucket, s3_file):
#     s3 = boto3.client('s3', aws_access_key_id=os.environ['AWS_ACCESS_KEY_ID'],
#                       aws_secret_access_key=os.environ['AWS_SECRET'])
#     try:
#         s3.upload_file(local_file, bucket, s3_file)
#         print("Upload Successful")
#         return True
#     except FileNotFoundError:
#         print("The file was not found")
#         return False
#     except NoCredentialsError:
#         print("Credentials not available")
#         return False
    
# upload_to_aws(f"{output_dir}/pytorch_model.bin", "llama-llama", "llama_3_8b_hf_ft/pytorch_model.bin")
# upload_to_aws(f"{output_dir}/config.json", "llama-llama", "llama_3_8b_hf_ft/config.json")
# upload_to_aws(f"{output_dir}/merges.txt", "llama-llama", "llama_3_8b_hf_ft/merges.txt")
# upload_to_aws(f"{output_dir}/vocab.json", "llama-llama", "llama_3_8b_hf_ft/vocab.json")
# upload_to_aws(f"{output_dir}/special_tokens_map.json", "llama-llama", "llama_3_8b_hf_ft/special_tokens_map.json")
# upload_to_aws(f"{output_dir}/tokenizer_config.json", "llama-llama", "llama_3_8b_hf_ft/tokenizer_config.json")
# upload_to_aws(f"{output_dir}/training_args.bin", "llama-llama", "llama_3_8b_hf_ft/training_args.bin")
# upload_to_aws(f"{output_dir}/optimizer.pt", "llama-llama", "llama_3_8b_hf_ft/optimizer.pt")
# upload_to_aws(f"{output_dir}/scheduler.pt", "llama-llama", "llama_3_8b_hf_ft/scheduler.pt")
# upload_to_aws(f"{output_dir}/training_args.bin", "llama-llama", "llama_3_8b_hf_ft/training_args.bin")
# upload_to_aws(f"{output_dir}/config.json", "llama-llama", "llama_3_8b_hf_ft/config.json")

