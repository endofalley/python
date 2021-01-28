FROM debian:buster-slim

LABEL MAINTAINER="Visionarytech, Inc"

ENV LANG=C.UTF-8 LC_ALL=C.UTF-8

RUN apt-get update -q && \
    apt-get install -q -y \
        bzip2 \
        ca-certificates \
        git \
        libglib2.0-0 \
        libsm6 \
        libxext6 \
        libxrender1 \
        mercurial \
        subversion \
        wget \
        unzip \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

ENV PATH /opt/conda/bin:$PATH

CMD [ "/bin/bash" ]

# Leave these args here to better use the Docker build cache
ARG CONDA_VERSION=py38_4.9.2
ARG CONDA_MD5=122c8c9beb51e124ab32a0fa6426c656

RUN wget --quiet https://repo.anaconda.com/miniconda/Miniconda3-${CONDA_VERSION}-Linux-x86_64.sh -O miniconda.sh && \
    echo "${CONDA_MD5}  miniconda.sh" > miniconda.md5 && \
    if ! md5sum --status -c miniconda.md5; then exit 1; fi && \
    mkdir -p /opt && \
    sh miniconda.sh -b -p /opt/conda && \
    rm miniconda.sh miniconda.md5 && \
    ln -s /opt/conda/etc/profile.d/conda.sh /etc/profile.d/conda.sh && \
    echo ". /opt/conda/etc/profile.d/conda.sh" >> ~/.bashrc && \
    echo "conda activate base" >> ~/.bashrc && \
    find /opt/conda/ -follow -type f -name '*.a' -delete && \
    find /opt/conda/ -follow -type f -name '*.js.map' -delete && \
    /opt/conda/bin/conda install -y python=3.6.8 flask h5py pandas keras tensorflow=1.13.1 matplotlib pywavelets gevent scikit-learn flask-cors pymongo && \
    /opt/conda/bin/conda clean -afy

RUN /opt/conda/bin/conda create -n tensorflow:2.3.1 --clone base && \
    source activate tensorflow:2.3.1 && \
    /opt/conda/bin/conda install -y tensorflow=2.3.1 && \
    source activate base

RUN mkdir /mcr-install && \
    mkdir /opt/mcr && \
    cd /mcr-install && \
    wget http://ssd.mathworks.com/supportfiles/downloads/R2018b/deployment_files/R2018b/installers/glnxa64/MCR_R2018b_glnxa64_installer.zip && \
    unzip -q MCR_R2018b_glnxa64_installer.zip && \
    ./install -destinationFolder /opt/mcr -agreeToLicense yes -mode silent && \
    cd / && \
    rm -rf mcr-install

ENV LD_LIBRARY_PATH=/opt/mcr/v95/runtime/glnxa64:/opt/mcr/v95/bin/glnxa64:/opt/mcr/v95/sys/os/glnxa64:/opt/mcr/v95/extern/bin/glnxa64
ENV MCR_CACHE_VERBOSE=true
ENV MCR_CACHE_ROOT=/tmp