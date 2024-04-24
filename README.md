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
!ACCELERATE_USE_FSDP=1 FSDP_CPU_RAM_EFFICIENT_LOADING=1 torchrun --nproc_per_node=4 ./scripts/run_fsdp_qlora.py --config llama_3_8B_fsdp_qlora.yaml
```

You may want to change the `--nproc_per_node` to the number of GPUs you have available. Here the script is set up to use 4 GPUs to use on g5.12xlarge instances on aws.
