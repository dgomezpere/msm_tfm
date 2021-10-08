#!/usr/bin/env bash

# Installation reference: http://www.htslib.org/download/
# Create opt/bin for binaries symlinks
mkdir -p /opt/bin

# Install HTSlib
mkdir /opt/htslib
wget -O /opt/htslib/htslib-1.13.tar.bz2 https://github.com/samtools/htslib/releases/download/1.13/htslib-1.13.tar.bz2
tar -xvf /opt/htslib/htslib-1.13.tar.bz2 -C /opt/htslib
rm /opt/htslib/htslib-1.13.tar.bz2
mv /opt/htslib/htslib-1.13 /opt/htslib/htslib_v1.13
cd /opt/htslib/htslib_v1.13 && make

# Create symlinks
ln -s /opt/htslib/htslib_v1.13 /opt/htslib_current
ln -s /opt/htslib_current/tabix /opt/bin/tabix
ln -s /opt/htslib_current/bgzip /opt/bin/bgzip
