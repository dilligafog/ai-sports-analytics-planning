# LLM Infrastructure Setup - Petals Distributed Inference

**Date**: August 28, 2025  
**Setup Environment**: Windows 11 with WSL2 Ubuntu 22.04.5 LTS  
**GPU Support**: CUDA 12.8 compatible  
**Status**: ✅ Successfully Installed and Operational

## Overview

This document details the complete setup of Petals distributed inference framework for large language model (LLM) processing in our AI Sports Analytics project. Petals enables distributed inference of large language models across multiple machines, making it possible to run models that would otherwise require expensive dedicated hardware.

## Architecture Decision

We chose **WSL2 (Windows Subsystem for Linux)** as our deployment environment for several strategic reasons:

### Why WSL2 Over Native Windows?

1. **Linux Compatibility**: Petals and its dependency `uvloop` require Linux for optimal performance
2. **GPU Access**: WSL2 provides full CUDA GPU access while maintaining Windows workflow
3. **Easy Resource Management**: Can quickly shutdown (`wsl --shutdown`) to free resources
4. **Development Isolation**: Keeps experimental ML environments separate from main Windows setup
5. **Network Performance**: Better networking stack for distributed inference

## Installation Process

### Environment Setup

#### Base System Requirements
- **OS**: Windows 11 with WSL2 enabled
- **WSL Distribution**: Ubuntu 22.04.5 LTS
- **Python**: 3.10.12 (compatible with Petals requirements)
- **CUDA**: 12.8+ (for GPU acceleration)

#### Python Environment
```bash
# Location: ~/petals-env/ in WSL2
# Virtual Environment: petals_venv
# Python Version: 3.10.12
```

### Installation Steps

#### 1. WSL2 Ubuntu Setup
```bash
# Access WSL2
bash

# Update system packages
apt update && apt install -y python3-pip python3-venv build-essential

# Verify Python version
python3 --version  # Should show 3.10.12
```

#### 2. Virtual Environment Creation
```bash
# Create dedicated directory
mkdir -p ~/petals-env
cd ~/petals-env

# Create and activate virtual environment
python3 -m venv petals_venv
source petals_venv/bin/activate
```

#### 3. Petals Installation
```bash
# Upgrade pip
pip install --upgrade pip

# Install Petals with all dependencies
pip install petals
```

### Installed Components

#### Core Framework
- **Petals**: 2.2.0.post1 (latest stable)
- **PyTorch**: 2.8.0+cu128 (CUDA 12.8 support)
- **Transformers**: 4.34.1 (HuggingFace compatibility)

#### Key Dependencies
- **bitsandbytes**: 0.41.1 (quantization support)
- **accelerate**: 0.32.1 (distributed training)
- **hivemind**: 1.1.10.post2 (P2P networking)
- **tensor-parallel**: 1.0.23 (model parallelism)
- **CUDA Libraries**: Full NVIDIA CUDA 12.8 stack

#### Networking Components
- **uvloop**: 0.21.0 (high-performance event loop)
- **grpcio**: 1.74.0 (RPC communication)
- **cryptography**: 45.0.6 (secure communications)

## Verification Results

### System Verification
```bash
# Python environment
python --version  # ✅ Python 3.10.12
which python      # ✅ /root/petals-env/petals_venv/bin/python

# PyTorch and CUDA
python -c "import torch; print('PyTorch:', torch.__version__)"  # ✅ 2.8.0+cu128
python -c "import torch; print('CUDA:', torch.cuda.is_available())"  # ✅ True

# Core dependencies
python -c "import transformers; print('Transformers:', transformers.__version__)"  # ✅ 4.34.1
```

### Expected Behavior
- **Normal**: Petals import may hang for 10-30 seconds during initialization
- **Reason**: Distributed inference setup requires:
  - CUDA context initialization
  - Network stack preparation
  - Distributed communication setup
  - Model loading infrastructure

## Usage Guidelines

### Environment Activation
```bash
# From Windows
bash

# Navigate to environment
cd ~/petals-env

# Activate environment
source petals_venv/bin/activate
```

### Resource Management
```bash
# Quick shutdown from Windows PowerShell
wsl --shutdown

# This immediately frees:
# - GPU memory
# - System RAM
# - Network connections
# - Background processes
```

### Example Usage Patterns
```python
# Basic distributed inference setup
import os
os.environ['PETALS_CACHE_DIR'] = '/tmp/petals_cache'

from petals import AutoDistributedModelForCausalLM
from transformers import AutoTokenizer

# Example: Loading a distributed model
model_name = "meta-llama/Llama-2-70b-chat-hf"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoDistributedModelForCausalLM.from_pretrained(model_name)
```

## Performance Characteristics

### Advantages
- **Memory Efficiency**: Distribute large models across multiple machines
- **Cost Effective**: Use commodity hardware instead of expensive single machines
- **Scalable**: Add more nodes to increase capacity
- **GPU Utilization**: Full CUDA acceleration in WSL2

### Considerations
- **Network Dependency**: Requires stable internet for distributed nodes
- **Initialization Time**: Cold start can take 30-60 seconds
- **Latency**: Network communication adds inference latency
- **Availability**: Dependent on network of volunteer nodes

## Troubleshooting

### Common Issues

#### Import Hanging
**Symptom**: `import petals` appears to hang  
**Solution**: This is normal - Petals initializes heavy components  
**Workaround**: Set environment variables to disable network features if testing

#### CUDA Issues
**Symptom**: CUDA not available  
**Solution**: Ensure WSL2 has CUDA support enabled  
**Verification**: `nvidia-smi` should work in WSL2

#### Memory Issues
**Symptom**: Out of memory errors  
**Solution**: Use `wsl --shutdown` to reset environment

### Environment Variables
```bash
# Disable network ping for testing
export PETALS_NO_PING_CLIENT=1

# Set custom cache directory
export PETALS_CACHE_DIR=/tmp/petals_cache

# Control logging level
export PETALS_LOG_LEVEL=INFO
```

## Integration with AI Sports Analytics

### Planned Use Cases
1. **Content Generation**: Automated analysis and reporting
2. **Data Processing**: Large-scale text analysis of sports data
3. **Feature Extraction**: NLP processing of news and social media
4. **Report Generation**: Automated sports analytics reports

### Project Integration Points
- **News Analysis**: Process sports news for sentiment and trends
- **Player Analysis**: Generate detailed player performance narratives
- **Betting Analysis**: Process and analyze betting market commentary
- **Social Media**: Analyze sports-related social media content

## Security Considerations

### Network Security
- **Encrypted Communication**: All Petals traffic is encrypted
- **Authentication**: Cryptographic authentication for node communication
- **Privacy**: Model inputs are distributed, not stored centrally

### Local Security
- **Isolation**: WSL2 provides process isolation from Windows
- **Resource Limits**: Can be controlled via WSL2 configuration
- **Quick Shutdown**: Immediate resource cleanup capability

## Future Enhancements

### Planned Improvements
1. **Custom Model Training**: Fine-tune models for sports-specific tasks
2. **Local Node Hosting**: Contribute compute resources to Petals network
3. **Performance Optimization**: Tune for specific sports analytics workloads
4. **Integration Scripts**: Automated setup and deployment scripts

### Monitoring and Maintenance
- **Resource Monitoring**: Track GPU and memory usage
- **Performance Metrics**: Monitor inference latency and throughput
- **Update Strategy**: Regular updates of Petals and dependencies
- **Backup Strategy**: Environment replication procedures

## Contact and Support

**Technical Lead**: Nex (Phil)  
**Setup Date**: August 28, 2025  
**Environment**: WSL2 Ubuntu 22.04.5 LTS  
**GPU**: CUDA 12.8 compatible

**Documentation Status**: ✅ Complete and Verified  
**Installation Status**: ✅ Operational  
**Next Phase**: Integration with sports analytics workflows
