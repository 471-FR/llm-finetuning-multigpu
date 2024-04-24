from datasets import load_dataset

# # Convert dataset to OAI messages
# system_message = """You are Llama, an AI assistant created by Philipp to be helpful and honest. 
#                     Your knowledge spans a wide range of top of topics, allowing you to engage 
#                     in substantive conversations and provide analysis on complex subjects."""

# def create_conversation(sample):
#     if sample["messages"][0]["role"] == "system":
#         return sample
#     else:
#       sample["messages"] = [{"role": "system", "content": system_message}] + sample["messages"]
#       return sample

# # Load dataset from the hub
# dataset = load_dataset("HuggingFaceH4/no_robots")

# # Add system message to each conversation
# columns_to_remove = list(dataset["train"].features)
# columns_to_remove.remove("messages")
# dataset = dataset.map(create_conversation, remove_columns=columns_to_remove,batched=False)

# # Filter out conversations which are corrupted with wrong turns, keep which have even number of turns after adding system message
# dataset["train"] = dataset["train"].filter(lambda x: len(x["messages"][1:]) % 2 == 0)
# dataset["test"] = dataset["test"].filter(lambda x: len(x["messages"][1:]) % 2 == 0)

# # save datasets to disk
# dataset["train"].to_json("dataset/train_dataset.json", orient="records", force_ascii=False)
# dataset["test"].to_json("dataset/test_dataset.json", orient="records", force_ascii=False)

from huggingface_hub import hf_hub_download
hf_hub_download(repo_id="sylvain471/episaveur", filename="config.json",repo_type="dataset",local_dir="dataset")

# load synthetic_invoices_reduced_2.json file
import json
with open("dataset/synth_data.json") as f:
    invoices = json.load(f)

system_message = """You are Llamanalist, an AI assistant to help analysing invoices. You extract information from user input and return a JSON object with the extracted information. You only use infomation provided in the conversation to generate the JSON object."""
dataset=[]
for invoice in invoices:
    conversation = {"messages": [{"role": "system", "content": system_message}]}
    conversation["messages"].append({"role": "user", "content": invoice['input']})
    conversation["messages"].append({"role": "assistant", "content": str(invoice['output'])})
    dataset.append(conversation)

ratio=0.9
train_set=dataset[:int(len(dataset)*ratio)]
test_set=dataset[int(len(dataset)*ratio):]

from datasets import Dataset
train_set = Dataset.from_list(train_set)
test_set = Dataset.from_list(test_set)

train_set.to_json("dataset/train_dataset.json", orient="records", force_ascii=False)
test_set.to_json("dataset/test_dataset.json", orient="records", force_ascii=False)