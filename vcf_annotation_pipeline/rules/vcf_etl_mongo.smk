#!/usr/bin/env python3
#-*- coding: utf-8 -*-

rule vcf_etl_mongo:
    input:
        vcf = rules.vep_annot_vcf.output.vcf,
    output:
        db_status = '{vcf_dirpath}/{filename}'.format(
            vcf_dirpath = config['workdir_tree']['vcf_dirpath'],
            filename = Path(config['input_vcf'].replace(''.join(Path(config['input_vcf']).suffixes), '.decomp.norm.annot.mongodb.DONE')).name
        ),
    params:
        mongo_builder_path = config['mongo_builder']['path'],
        annotation_field = config['mongo_builder']['opts']['annotation_field'],
        annotation_sep = config['mongo_builder']['opts']['annotation_sep'],
        buffersize_records = config['mongo_builder']['opts']['buffersize_records'],
        db_name = config['db_name'],
    run:
        params_list = []

        params_list.append('--annotation_field {}'.format(params.annotation_field))
        params_list.append("--annotation_sep '{}'".format(params.annotation_sep))
        params_list.append('--buffersize_records {}'.format(params.buffersize_records))
        params_list.append('--db_name {}'.format(params.db_name))

        params_str = ' '.join(params_list)
        cmd = ' '.join([
            "{params.mongo_builder_path}",
            "--vcf {input.vcf}",
            "{params_str}",
            "&& touch {output.db_status}",
        ])

        shell(cmd)



