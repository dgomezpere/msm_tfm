#!/usr/bin/env python3
#-*- coding: utf-8 -*-

rule vt_decompose:
    input:
        vcf = config['input_vcf'],
    output:
        vcf = temp('{vcf_dirpath}/{vcf_filename}'.format(
            vcf_dirpath = config['workdir_tree']['vcf_dirpath'],
            vcf_filename = Path(config['input_vcf'].replace(''.join(Path(config['input_vcf']).suffixes), ''.join(['.decomp'] + Path(config['input_vcf']).suffixes))).name,
        )),
        tbi = temp('{vcf_dirpath}/{vcf_filename}'.format(
            vcf_dirpath = config['workdir_tree']['vcf_dirpath'],
            vcf_filename = Path(config['input_vcf'].replace(''.join(Path(config['input_vcf']).suffixes), ''.join(['.decomp'] + Path(config['input_vcf']).suffixes))).name + '.tbi',
        )),
        report = '{report_dirpath}/{report_filename}'.format(
            report_dirpath = config['workdir_tree']['qc_data_dirpath'],
            report_filename = Path(config['input_vcf'].replace(''.join(Path(config['input_vcf']).suffixes), '.vt_decompose_report')).name,
        ),
    params:
        vt_path = config['vt']['path'],
        bcftools_path = config['bcftools']['path'],
        tabix_path = config['tabix']['path'],
        smart_decomposition = config['vt']['opts']['smart_decomposition'],
    run:
        params_list = []

        if params.smart_decomposition:
            params_list.append('-s')

        params_str = ' '.join(params_list)

        cmd = ' '.join([
            "{params.vt_path} decompose {params_str} {input.vcf} 2> {output.report} | {params.bcftools_path} view -O z -o {output.vcf}",
            "&& {params.tabix_path} -p vcf {output.vcf}"
        ])
        shell(cmd)

# Run vt_normalize rule
rule vt_normalize:
    input:
        vcf = rules.vt_decompose.output.vcf,
        tbi = rules.vt_decompose.output.tbi,
    output:
        vcf = temp('{vcf_dirpath}/{vcf_filename}'.format(
            vcf_dirpath = config['workdir_tree']['vcf_dirpath'],
            vcf_filename = Path(config['input_vcf'].replace(''.join(Path(config['input_vcf']).suffixes), ''.join(['.decomp.norm'] + Path(config['input_vcf']).suffixes))).name,
        )),
        tbi = temp('{vcf_dirpath}/{vcf_filename}'.format(
            vcf_dirpath = config['workdir_tree']['vcf_dirpath'],
            vcf_filename = Path(config['input_vcf'].replace(''.join(Path(config['input_vcf']).suffixes), ''.join(['.decomp.norm'] + Path(config['input_vcf']).suffixes))).name + '.tbi',
        )),
        report = '{report_dirpath}/{report_filename}'.format(
            report_dirpath = config['workdir_tree']['qc_data_dirpath'],
            report_filename = Path(config['input_vcf'].replace(''.join(Path(config['input_vcf']).suffixes), '.vt_normalize_report')).name,
        ),
    params:
        vt_path = config['vt']['path'],
        bcftools_path = config['bcftools']['path'],
        tabix_path = config['tabix']['path'],
        refgenome = config['refgenome_filepath'],
        window_size = config['vt']['opts']['window_size']
    run:
        params_list = []

        if params.window_size:
            params_list.append("-w {}".format(params.window_size))

        params_str = ' '.join(params_list)

        cmd = ' '.join([
            "{params.vt_path} normalize -n {params_str} -r {params.refgenome} {input.vcf} 2> {output.report} | {params.bcftools_path} view -O z -o {output.vcf}",
            "&& {params.tabix_path} -p vcf {output.vcf}"
        ])
        shell(cmd)

