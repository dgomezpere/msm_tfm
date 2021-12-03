#!/usr/bin/env python3
#-*- coding: utf-8 -*-

rule vep_annot_vcf:
    input:
        vcf = rules.vt_normalize.output.vcf,
    output:
        vcf = '{vcf_dirpath}/{vcf_filename}'.format(
            vcf_dirpath = config['workdir_tree']['vcf_dirpath'],
            vcf_filename = Path(config['input_vcf'].replace(''.join(Path(config['input_vcf']).suffixes), ''.join(['.decomp.norm.annot'] + Path(config['input_vcf']).suffixes))).name,
        ),
        tbi = '{vcf_dirpath}/{vcf_filename}'.format(
            vcf_dirpath = config['workdir_tree']['vcf_dirpath'],
            vcf_filename = Path(config['input_vcf'].replace(''.join(Path(config['input_vcf']).suffixes), ''.join(['.decomp.norm.annot'] + Path(config['input_vcf']).suffixes))).name + '.tbi',
        ),
    params:
        vep_path = config['vep']['path'],
        tabix_path = config['tabix']['path'],
        buffer_size = config['vep']['opts']['buffer_size'],
        dir_cache = config['vep']['opts']['dir_cache'],
        exclude_predicted = config['vep']['opts']['exclude_predicted'],
        specie = config['vep']['opts']['specie'],
        assembly = config['vep']['opts']['assembly'],
        refgenome = config['references']['refgenome_filepath'],
    threads: workflow.cores,
    run:
        params_list = []

        params_list.append('--fork {}'.format(threads))
        params_list.append('--buffer_size {}'.format(params.buffer_size))
        params_list.append('--dir_cache {}'.format(params.dir_cache))
        if params.exclude_predicted:
            params_list.append('--exclude_predicted')
        params_list.append('--species {}'.format(params.specie))
        params_list.append('--assembly {}'.format(params.assembly))
        params_list.append('--fasta {}'.format(params.refgenome))

        params_str = ' '.join(params_list)

        cmd = ' '.join([
            "{params.vep_path}",
            "-i {input.vcf} --format vcf --vcf -o {output.vcf} --compress_output bgzip --force_overwrite --cache",
            "{params_str}",
            "--merged --hgvs --hgvsg --symbol --ccds --canonical --mane --biotype --protein --domains --check_existing --clin_sig_allele 1",
            "&& {params.tabix_path} -p vcf {output.vcf}",
        ])

        shell(cmd)

