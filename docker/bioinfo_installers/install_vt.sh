#!/usr/bin/env bash

# Installation reference: https://genome.sph.umich.edu/wiki/Vt#Installation
# Create /opt/bin for binaries symlinks
mkdir -p /opt/bin/

# Install VT
mkdir -p /opt/vt/vt
git clone https://github.com/atks/vt.git /opt/vt/vt
cd /opt/vt/vt
git submodule update --init --recursive
make && make test
VT_VERSION=vt_$(/opt/vt/vt/vt --version 2>&1 | grep "^vt" | egrep "[^ ]+$" -o)
mv /opt/vt/vt /opt/vt/$VT_VERSION

# Create symlinks
ln -s /opt/vt/$VT_VERSION /opt/vt_current
ln -s /opt/vt_current/vt /opt/bin/vt
