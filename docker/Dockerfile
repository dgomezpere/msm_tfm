FROM ubuntu:20.04

# Image metadata
LABEL maintainer="David Gomez Peregrina" \
      email="dgomezperegrina@vhio.net" \
      organization="Sarcoma Translational Lab (VHIO)" \
      version="0.0.1" \
      description="Bioinformatics Docker for develoment and production"

# Update and fix missing repo links
RUN apt update && apt update --fix-missing && apt upgrade -y

# Non-interactive tzdata configuration and installation
COPY debconf_preseed.conf /etc/debconf_preseed.conf
RUN export DEBIAN_FRONTEND=noninteractive DEBCONF_NONINTERACTIVE_SEEN=true \
    && debconf-set-selections /etc/debconf_preseed.conf \
    && apt install tzdata

# Installing mandatory and basic software and libs
RUN apt install -y \
    build-essential \
    software-properties-common \
    g++ \
    gcc \
    make \
    cmake \
    zlib1g-dev \
    libbz2-dev \
    liblzma-dev \
    libncurses5-dev \
    libcurl4-openssl-dev \
    libssl-dev \
    cpanminus \
    locales \
    zip \
    unzip \
    tree \
    tmux \
    htop \
    rsync \
    wget \
    curl \
    git \
    parallel \
    task-spooler

# COPY cpan configuration
COPY cpan.MyConfig.pm /root/.cpan/CPAN/MyConfig.pm

# Set up locales
RUN sed -i -e 's/# en_US.UTF-8 UTF-8/en_US.UTF-8 UTF-8/' /etc/locale.gen && \
    locale-gen
ENV LANG en_US.UTF-8
ENV LANGUAGE en_US:en
ENV LC_ALL en_US.UTF-8

# Set up vim
RUN apt install -y vim

#[TODO] Install Vundle and add .vimrc from https://gist.github.com/dgomezpere/203469d2e7ddbec67aaf69702b14d8f9

# Install Java OpenJDK
RUN apt install -y \
    openjdk-8-jdk \
    openjdk-11-jdk

# Install NodeJS >= v12.0
RUN curl -fsSL https://deb.nodesource.com/setup_lts.x | bash - \
    && apt update && apt install nodejs

# Install python3 and jupyterlab
RUN apt install -y \
    python3 \
    python3-pip \
    && pip3 install --upgrade pip \
    && ln -s /usr/bin/python3 /usr/bin/python

RUN pip3 install jupyterlab

# Install python3 package requirements
COPY py_requirements.txt /py_requirements.txt
RUN pip3 install -r /py_requirements.txt --upgrade \
    && rm /py_requirements.txt

# Install R in ubuntu:20.04 (requires tzdata installation)
RUN apt install -y dirmngr gnupg apt-transport-https ca-certificates \
    && apt-key adv --keyserver keyserver.ubuntu.com --recv-keys E298A3A825C0D65DFD57CBB651716619E084DAB9 \
    && add-apt-repository 'deb https://cloud.r-project.org/bin/linux/ubuntu focal-cran40/' \
    && apt update && apt install -y r-base r-base-core r-recommended r-base-dev

#[TODO] Install R packages of interest

# Install Bioconductor
COPY install_bioconductor.R /install_bioconductor.R
RUN chmod +x /install_bioconductor.R \
    && /install_bioconductor.R \
    && rm /install_bioconductor.R

# [TODO] Install bioconductor packages

# Install IRkernel for jupyterlab
COPY install_IRkernel.R /install_IRkernel.R
RUN chmod +x /install_IRkernel.R \
    && /install_IRkernel.R \
    && jupyter labextension install @techrah/text-shortcuts
    && rm /install_IRkernel.R

# Install MongoDB Community Edition (specs for ubuntu:20.04)
RUN wget -qO - https://www.mongodb.org/static/pgp/server-5.0.asc | apt-key add - \
    && touch /etc/apt/sources.list.d/mongodb-org-5.0.list \
    && echo 'deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu focal/mongodb-org/5.0 multiverse' | tee /etc/apt/sources.list.d/mongodb-org-5.0.list \
    && apt update && apt install -y mongodb-org

# COPY and install bioinfo_installers
COPY bioinfo_installers /bioinfo_installers
RUN chmod +x /bioinfo_installers/*.sh \
    && for installer in $(ls /bioinfo_installers); do echo '#[INFO] Installing:' /bioninfo_installers/$installer; /bioinfo_installers/$installer; done \
    && rm -rf /bioinfo_installers
# bioinfo_installers will install binaries in /opt/bin
ENV PATH="/opt/bin:$PATH"

# Expose ports:
# - Jupyterlab: 8888
EXPOSE \
    8888
