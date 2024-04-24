#!/bin/bash
echo "Hello from user_data.sh!"

sudo add-apt-repository ppa:deadsnakes/ppa -y

sudo apt update
sudo apt upgrade -y

sudo apt install mc -y
sudo apt install python3.10 python3.10-venv python3.10-dev -y


cd /home/ubuntu
git clone https://github.com/471-FR/llm-finetuning-multigpu.git
cd llm-finetuning-multigpu
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

pip cache purge

#huggingface-cli login --token HF_TOKEN

echo "Goodbye from user_data.sh!"