#!/usr/bin/env bash

# Installation reference: http://www.htslib.org/download/
# Create opt/bin for binaries symlinks
mkdir -p /opt/bin

# Install BCFtools
mkdir /opt/bcftools
wget -O /opt/bcftools/bcftools-1.13.tar.bz2 https://github.com/samtools/bcftools/releases/download/1.13/bcftools-1.13.tar.bz2
tar -xvf /opt/bcftools/bcftools-1.13.tar.bz2 -C /opt/bcftools
rm /opt/bcftools/bcftools-1.13.tar.bz2
mv /opt/bcftools/bcftools-1.13 /opt/bcftools/bcftools_v1.13
cd /opt/bcftools/bcftools_v1.13 && make

# Create symlinks
ln -s /opt/bcftools/bcftools_v1.13 /opt/bcftools_current
ln -s /opt/bcftools_current/bcftools /opt/bin/bcftools

