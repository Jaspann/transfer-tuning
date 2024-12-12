FROM ubuntu:20.04

ENV DEBIAN_FRONTEND=noninteractive

# Install basic dependencies
RUN apt-get update && apt-get install -y \
    wget \
    gnupg2 \
    software-properties-common \
    build-essential \
    cmake \
    git \
    llvm-dev \
    ninja-build \
    python3 \
    python3-pip \
    tmux \
    tree

# Install CUDA
RUN wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2004/x86_64/cuda-ubuntu2004.pin && \
    mv cuda-ubuntu2004.pin /etc/apt/preferences.d/cuda-repository-pin-600 && \
    wget https://developer.download.nvidia.com/compute/cuda/11.3.0/local_installers/cuda-repo-ubuntu2004-11-3-local_11.3.0-465.19.01-1_amd64.deb && \
    dpkg -i cuda-repo-ubuntu2004-11-3-local_11.3.0-465.19.01-1_amd64.deb && \
    apt-key add /var/cuda-repo-ubuntu2004-11-3-local/7fa2af80.pub && \
    apt-get update && \
    apt-get install -y cuda-11-3 cuda-compiler-11-3

# Set CUDA environment variables
ENV PATH=/usr/local/cuda-11.3/bin:${PATH}
ENV LD_LIBRARY_PATH=/usr/local/cuda-11.3/lib64:${LD_LIBRARY_PATH}
ENV CUDA_HOME=/usr/local/cuda-11.3
ENV CUDACXX=/usr/local/cuda-11.3/bin/nvcc

# Rest of your original Dockerfile...
COPY requirements.txt ./
RUN pip3 install -r requirements.txt
RUN jupyter contrib nbextension install --user; jupyter nbextensions_configurator enable --user
RUN pip3 install \
    torch==1.10.0 \
    torchvision==0.11.1 \
    torchaudio==0.10.0 \
    -f https://download.pytorch.org/whl/cu113/torch_stable.html

# CMake
RUN apt-get update \
    && apt-get -y install build-essential \
    && apt-get install -y wget \
    && rm -rf /var/lib/apt/lists/* \
    && wget https://github.com/Kitware/CMake/releases/download/v3.24.1/cmake-3.24.1-Linux-x86_64.sh \
        -q -O /tmp/cmake-install.sh \
        && chmod u+x /tmp/cmake-install.sh \
        && mkdir /opt/cmake-3.24.1 \
        && /tmp/cmake-install.sh --skip-license --prefix=/opt/cmake-3.24.1 \
        && rm /tmp/cmake-install.sh \
        && ln -s /opt/cmake-3.24.1/bin/* /usr/local/bin

# Install TVM
RUN cd / && \
    git clone --branch v0.16.0 https://github.com/apache/tvm && \
    cd tvm && \
    git fetch origin pull/16499/head:ansor-autotvm-pr && \
    git checkout ansor-autotvm-pr && \
    git submodule update --init --recursive && \
    mkdir build && \
    cp cmake/config.cmake build && \
    cd build && \
    printf "set(USE_LLVM ON)\n" >> config.cmake && \
    printf "set(USE_CUDA ON)\n" >> config.cmake && \
    # printf "set(USE_CUBLAS ON)\n" >> config.cmake && \
    # printf "set(USE_CUDNN ON)\n" >> config.cmake && \
    printf "set(CMAKE_CUDA_ARCHITECTURES 61)\n" >> config.cmake && \
    cmake .. -GNinja && \
    ninja

RUN echo "export TVM_HOME=/tvm; export PYTHONPATH=\$TVM_HOME/python:\${PYTHONPATH}" > /root/.bashrc

WORKDIR /workspace





































# FROM ubuntu:20.04


# # Add NVIDIA repository and install CUDA
# RUN apt-get update && apt-get install -y wget gnupg2
# RUN wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2004/x86_64/cuda-ubuntu2004.pin
# RUN mv cuda-ubuntu2004.pin /etc/apt/preferences.d/cuda-repository-pin-600
# RUN wget https://developer.download.nvidia.com/compute/cuda/11.3.0/local_installers/cuda-repo-ubuntu2004-11-3-local_11.3.0-465.19.01-1_amd64.deb
# RUN dpkg -i cuda-repo-ubuntu2004-11-3-local_11.3.0-465.19.01-1_amd64.deb
# RUN apt-key add /var/cuda-repo-ubuntu2004-11-3-local/7fa2af80.pub
# RUN apt-get update


# # ----------------------------------------------------------------------------------------------------------------------
# # Install libraries
# # ----------------------------------------------------------------------------------------------------------------------

# ENV DEBIAN_FRONTEND=noninteractive
# RUN apt-get update --fix-missing && \
#     apt-get -y install \
#     build-essential \
#     cmake \
#     git \
#     llvm-dev \
#     ninja-build \
#     python3 \
#     python3-pip \
#     tmux \
#     tree \
#     wget \
#     cuda


# # ----------------------------------------------------------------------------------------------------------------------
# # Setup Python deps
# # ----------------------------------------------------------------------------------------------------------------------

# COPY requirements.txt ./
# RUN pip3 install -r requirements.txt
# RUN jupyter contrib nbextension install --user; jupyter nbextensions_configurator enable --user
# RUN pip3 install \
#     torch==1.10.0 \
#     torchvision==0.11.1 \
#     torchaudio==0.10.0 \
#     -f https://download.pytorch.org/whl/cu113/torch_stable.html


# # CMake
# RUN apt-get update \
#     && apt-get -y install build-essential \
#     && apt-get install -y wget \
#     && rm -rf /var/lib/apt/lists/* \
#     && wget https://github.com/Kitware/CMake/releases/download/v3.24.1/cmake-3.24.1-Linux-x86_64.sh \
#         -q -O /tmp/cmake-install.sh \
#         && chmod u+x /tmp/cmake-install.sh \
#         && mkdir /opt/cmake-3.24.1 \
#         && /tmp/cmake-install.sh --skip-license --prefix=/opt/cmake-3.24.1 \
#         && rm /tmp/cmake-install.sh \
#         && ln -s /opt/cmake-3.24.1/bin/* /usr/local/bin

# # ----------------------------------------------------------------------------------------------------------------------
# # Install TVM
# # ----------------------------------------------------------------------------------------------------------------------
#     RUN cd / && \
#     git clone --branch v0.16.0 https://github.com/apache/tvm && \
#     cd tvm && \
#     git fetch origin pull/16499/head:ansor-autotvm-pr && \
#     git checkout ansor-autotvm-pr && \
#     git submodule update --init --recursive && \
#     mkdir build && \
#     cp cmake/config.cmake build && \
#     cd build && \
#     printf "set(USE_LLVM ON)\n" >> config.cmake && \
#     printf "set(USE_CUDA ON)\n" >> config.cmake && \
#     printf "set(USE_CUBLAS ON)\n" >> config.cmake && \
#     printf "set(USE_CUDNN ON)\n" >> config.cmake && \
#     printf "set(CMAKE_CUDA_ARCHITECTURES 61)\n" >> config.cmake && \
#     cmake .. -GNinja && \
#     ninja


# RUN echo "export TVM_HOME=/tvm; export PYTHONPATH=\$TVM_HOME/python:\${PYTHONPATH}" > /root/.bashrc

# WORKDIR /workspace
