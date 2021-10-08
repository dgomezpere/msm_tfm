#!/usr/bin/env bash

# Installation reference: https://github.com/EBIvariation/vcf-validator
# Create opt/bin for binaries symlinks
mkdir -p /opt/bin

# Install vcf_validator
mkdir -p /opt/vcf_validator/vcf_validator_v0.9.4
wget -O /opt/vcf_validator/vcf_validator_v0.9.4/vcf_validator https://github.com/EBIvariation/vcf-validator/releases/download/v0.9.4/vcf_validator_linux
chmod +x /opt/vcf_validator/vcf_validator_v0.9.4/vcf_validator

# Create symlinks
ln -s /opt/vcf_validator/vcf_validator_v0.9.4 /opt/vcf_validator_current
ln -s /opt/vcf_validator_current/vcf_validator /opt/bin/vcf_validator

