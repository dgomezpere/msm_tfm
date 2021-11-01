import re
import json

with open('vt_decompose_report.txt', 'r') as fh:

    report = []

    # regex section
    # .+ lazy regex -> avoid
    version_re = re.compile('decompose (?P<version>\S+$)')
    input_re = re.compile('input VCF file\s+(?P<ifile>\S+)')
    output_re = re.compile('.+output VCF file\s+(?P<ofile>\S+)')
    sdec_re = re.compile('smart decomposition\s+(?P<sdec>\S+ \S+)')
    nvar_re = re.compile('no. variants\s+: (?P<nvar>\d+)')
    nbia_re = re.compile('no. biallelic variants\s+: (?P<nbia>\d+)')
    nmul_re = re.compile('no. multiallelic variants\s+: (?P<nmul>\d+)')
    nadd_re = re.compile('no. additional biallelics\s+: (?P<nadd>\d+)')
    tbv_re = re.compile('total no. of biallelics\s+: (?P<tbv>\d+)')
    time_re = re.compile('Time elapsed: (?P<time>\d\S+)')

    for line in fh:
        line = line.lstrip(' ')
        if line.startswith('decompose'):
            reg_ex = version_re.search(line).groupdict()["version"]
            report.append({'version':f"vt_decompose_{reg_ex}"})

        elif line.startswith('options'):
            options = {}
            report.append(options)
            reg_ex = input_re.search(line).groupdict()['ifile']
            options['input_vcf'] = reg_ex

        elif line.startswith('[o] output VCF'):
            reg_ex = output_re.search(line).groupdict()['ofile']
            options['output_vcf'] = reg_ex

        elif line.startswith('[s] smart decomposition'):
            reg_ex = sdec_re.search(line).groupdict()['sdec']
            options['smart decomposition'] = reg_ex

        elif line.startswith('stats'):
            stats = {}
            report.append(stats)
            reg_ex = nvar_re.search(line).groupdict()['nvar']
            stats['n_variants'] = reg_ex

        elif line.startswith('no. biallelic variants'):
            reg_ex = nbia_re.search(line).groupdict()['nbia']
            stats['n_biallelic_variants'] = reg_ex

        elif line.startswith('no. multiallelic variants'):
            reg_ex = nmul_re.search(line).groupdict()['nmul']
            stats['n_multiallelic_variants'] = reg_ex

        elif line.startswith('no. additional biallelics'):
            reg_ex = nadd_re.search(line).groupdict()['nadd']
            stats['n_additional_biallelic_variants'] = reg_ex

        elif line.startswith('total no. of biallelics'):
            reg_ex = tbv_re.search(line).groupdict()['tbv']
            stats['total_biallelic_variants'] = reg_ex

        elif line.startswith('Time elapsed'):
            reg_ex = time_re.search(line).groupdict()['time']
            report.append({'Time elapsed':reg_ex})

g = open("vt_decompose_report.json", "w")
g.write(json.dumps(report, indent=4))
g.close()

print(report)
