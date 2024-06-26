# LLM finetuning on multiple GPUs

reference https://www.philschmid.de/fsdp-qlora-llama3

## Setup

```bash
git clone git@github.com:471-FR/llm-finetuning-multigpu.git
cd llm-finetuning-multigpu
pip install -r requirements.txt
```

## Finetuning

```bash
ACCELERATE_USE_FSDP=1 FSDP_CPU_RAM_EFFICIENT_LOADING=1 torchrun --nproc_per_node=4 ./run_fsdp_qlora.py --config ./llama_3_8B_fsdp_qlora.yaml
```

You may want to change the `--nproc_per_node` to the number of GPUs you have available. Here the script is set up to use 4 GPUs to use on g5.12xlarge instances on aws.


# Terraform

The terraform script sets up:

- a `g5.12xlarge` instance with ubuntu and nvidia drivers on aws. You can change the instance type in the `main.tf` file. 

- a security group that allows all traffic on all ports. You may want to change this to only allow traffic on the ports you need.

- a key pair that you can use to ssh into the instance.

First `cp user_data.sh.example user_data.sh` and fill in the variables, then


```bash
terraform init
terraform plan
terraform apply
```
the address of the instance will be printed at the end of the `terraform apply` command. Alternatively you can run:

```bash
PUBLIC_IP=$(terraform show -json | jq .values.outputs.public_ip.value | tr -d '"')
```
to obtain the address of the instance.

You can ssh into the instance with the following command:

```bash
chmod 400 myKey.pem
ssh -i myKey.pem ubuntu@$PUBLIC_IP
```

To destroy the instance run:

```bash
terraform destroy
```

also remember to delete the key pair 
    
```bash 
rm -f myKey.pem
```

# monitoring
tensorboard can be accessed on the instance, first redirect the port with the following command:
```bash
ssh -i myKey.pem -L 6006:localhost:6006 ubuntu@$PUBLIC_IP
```
then run tensorboard on the instance with the following command:
```bash
tensorboard --logdir llama3-8b-hf-ft 
```