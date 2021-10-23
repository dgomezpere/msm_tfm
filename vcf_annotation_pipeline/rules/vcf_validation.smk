#!/usr/bin/env python3
#-*- coding: utf-8 -*-

# Run vcf_validatort rule
rule vcf_validator:
    input:
        vcf = config['input_vcf'],
    output:
        report = '{report_dirpath}/{report_filename}'.format(
            report_dirpath = config['workdir_tree']['qc_data_dirpath'], 
            report_filename = str(Path(config['input_vcf']).name)+'.errors_summary.txt'
        ),
    params:
        vcf_validator_path = config['vcf_validator']['path'],
        validation_level = config['vcf_validator']['opts']['validation_level'],
        report_type = config['vcf_validator']['opts']['report_type'],
    run:

        outdir = config['workdir_tree']['qc_data_dirpath']
        vcf_filename = str(Path(config['input_vcf']).name)

        cmd = ' '.join([
            "{params.vcf_validator_path}",
            "--input {input.vcf}",
            "--level {params.validation_level}",
            "--report {params.report_type}",
            "--outdir {outdir}",
            "&& mv {outdir}/{vcf_filename}.* {outdir}/{vcf_filename}.errors_summary.txt"
        ])

        shell(cmd)


