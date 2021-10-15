#!/usr/bin/env bash

# Installation reference: https://m.ensembl.org/info/docs/tools/vep/script/vep_download.html 
# Create /opt/bin for binaries symlinks
mkdir -p /opt/bin/

# Install VEP 
VEP_VERSION=104
mkdir -p /opt/ensembl-vep/ensembl-vep_v$VEP_VERSION
git clone https://github.com/Ensembl/ensembl-vep.git /opt/ensembl-vep/ensembl-vep_v$VEP_VERSION
cd /opt/ensembl-vep/ensembl-vep_v$VEP_VERSION
git pull
git checkout release/$VEP_VERSION
## Install dependencies
apt install -y gcc g++ make
cpan Archive::Zip
cpan DBD::mysql
cpan DBI
cd /opt/ensembl-vep/ensembl-vep_v$VEP_VERSION
perl INSTALL.pl --AUTO a

# Create symlinks
ln -s /opt/ensembl-vep/ensembl-vep_v$VEP_VERSION /opt/ensembl-vep_current
ln -s /opt/ensembl-vep_current/vep /opt/bin/vep
