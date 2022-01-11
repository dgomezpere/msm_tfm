# Snakemake VCF annotation pipeline

## Brief description

This pipeline has been designed to process and annotate the variants from a  VCf file (meeting the standard specifications of VCF v4.2).
Multiallelic variants from the input VCF are first decomposed and biallelic variants are normalized for a parsimonious representation of the variants.
Finally the variants are annotated for downstream intepretation using Ensembl's VEP annotator.

## Running the pipeline from CLI

```
snakemake --snakefile <Snakefile> --cores <cores> --config_file <config.yaml> \
    --config workdir=<workdir> input_vcf=<input_vcf> references.refgenome=<refgenome.fa> vep.opts.dir_cache=<dir_cache> \
    --until all --verbose -p
```

If [panoptes](https://github.com/panoptes-organization/panoptes) is installed, use `--wms-monitor http://127.0.0.1:5000` when running the pipeline.
`5000` is the default port for panoptes running service.
