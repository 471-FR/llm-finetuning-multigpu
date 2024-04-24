#!/bin/bash
echo "Hello from user_data.sh!"

sudo apt update
sudo apt upgrade -y

sudo apt install mc -y
sudo apt install python3-venv -y

git clone https://github.com/471-FR/llm-finetuning-multigpu.git
cd llm-finetuning-multigpu
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

#huggingface-cli login --token HF_TOKEN

echo "Goodbye from user_data.sh!"