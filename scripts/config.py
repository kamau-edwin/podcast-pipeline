import os
import platform
import torch

def create_model_config():
    """
    Determines the optimal WhisperX model, device, and compute type
    based on platform and GPU availability.
    These are recommendation and testing can be done to get optimal
    settings
    
    Returns:
        dict: model configuration with keys: model_size, device, compute_type
        and batch_size
    """
    # Platform and device checks
    has_gpu = torch.cuda.is_available()
    os_name = platform.system()

    # Select model size
    if has_gpu:
        gpu_name = torch.cuda.get_device_name(0)
        print(f"Detected GPU: {gpu_name}")

        # For high-end GPUs like A100 or V100, use large models
        if any(x in gpu_name for x in ["A100", "V100", "H100"]):
            model_size = "large-v3"
            batch_size = 16 # use 16 - 32 memory > 16GB
        else:
            model_size = "medium" # increase memory with large model size
            batch_size = 4 # 4 - 8 memory > 10GB 
        device = "cuda"
        compute_type = "float16"
    else:
        # CPU case: use tiny or base
        model_size = "base"
        compute_type = "float32" # use int8 for Linux machines 
        device = "cpu"
        batch_size = 1

    return {
        "model_size": model_size,
        "device": device,
        "compute_type": compute_type,
        "batch_size" : batch_size
    }


RUN_CONFIG= create_model_config()

HF_TOKEN = "your hugging face token"

DB_CONFIG = {
  'user': 'your_username', # database admin username
  'password': 'your_password', # database admin password
  'host': 'cloud host path', # database instance address
  'port': '5432',
  'database': 'database name' # database name need to be created before hand
}

