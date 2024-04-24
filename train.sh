ACCELERATE_USE_FSDP=1 FSDP_CPU_RAM_EFFICIENT_LOADING=1 torchrun --nproc_per_node=4 ./run_fsdp_qlora.py --config ./llama_3_8B_fsdp_qlora.yaml

# shutdown ec2 instance to avoid extra charges
sudo shutdown -h now