from dash import html, dcc, dash_table
import dash_bootstrap_components as dbc
import dash_uploader as du
from dash.dependencies import Input, Output, State
from app import app
import json
import uuid
from pathlib import Path
from datetime import datetime
from pymongo import MongoClient
import subprocess

# Text inputs
input_style = {
    'width': 'auto',
    'marginLeft': '50px',
    'marginRight': '50px',
    'marginTop': '10px',
    'marginBottom': '10px',
}
analysis_name_input = dbc.InputGroup(
    [
        dbc.InputGroupText("Analysis Name:"),
        dbc.Input(id='analysis_name_input', placeholder="Analysis Name", type="string")
    ],
    size='sm',
    style=input_style,
)

curator_name_input = dbc.InputGroup(
    [
        dbc.InputGroupText("Curator Name:"),
        dbc.Input(id='curator_name_input', placeholder="Curator Name", type="string")
    ],
    size='sm',
    style=input_style,
)

# Upload files
folder = '/DATA'
du.configure_upload(app, folder)
analysis_id = str(uuid.uuid1())

upload_style = {
    'width': 'auto',
    'marginLeft': '50px',
    'marginRight': '50px',
    'marginTop': '10px',
    'marginBottom': '10px',
}

vcf_upload = du.Upload(
    id='vcf_upload',
    upload_id=analysis_id,
    text='Upload VCF file',
    text_completed='VCF uploaded: ',
    cancel_button=True,
    pause_button=True,
    max_file_size=1024*20, # Max size == 20Gb
    chunk_size=1,
    default_style=upload_style,
)

fasta_upload = du.Upload(
    id='fasta_upload',
    upload_id=analysis_id,
    text='Upload Reference Genome FASTA',
    text_completed='Reference Genome FASTA uploaded: ',
    cancel_button=True,
    pause_button=True,
    max_file_size=1024*5, # Max size == 5Gb
    chunk_size=10,
    default_style=upload_style,
)

# Buttons

button_style = {
    'marginLeft': '50px',
}

run_analysis_button = dbc.Button(
    "Run Analysis",
    id='run_analysis_button',
    active=True,
    color='secondary',
    disabled=False,
    n_clicks=0,
    style=button_style,
)

panoptes_button = dbc.Button(
    "Analysis Monitoring",
    color="secondary",
    href="http://localhost:2000",
    target='_blank',
    style={'marginLeft': '10px'},
)


# Callbacks
@app.callback(
    Output('new_analysis_db_post', component_property='children'),
    [
        Input('analysis_name_input', component_property='value'),
        Input('curator_name_input', component_property='value'),
        Input('vcf_upload', component_property='isCompleted'),
        Input('fasta_upload', component_property='isCompleted'),
        State('vcf_upload', 'fileNames'),
        State('fasta_upload', 'fileNames'),
        Input('run_analysis_button', component_property='n_clicks'),
    ]
)

def new_analysis_db_post(analysis_name, curator_name, vcf_upload_completed, fasta_upload_completed, vcf_filename, fasta_filename, n_clicks):
    global folder
    global analysis_id

    # Get VCF filepath
    try:
        vcf_filepath = str(Path(folder)/analysis_id/vcf_filename[0])
    except IndexError: # While no file is uploaded yet
        vcf_filepath = None
    except TypeError: # While no file is uploaded yet
        vcf_filepath = None

    # Get FASTA filepath
    try:
        fasta_filepath = str(Path(folder)/analysis_id/fasta_filename[0])
    except IndexError: # While no file is uploaded yet
        fasta_filepath = None
    except TypeError: # While no file is uploaded yet
        fasta_filepath = None

    if analysis_name and curator_name and vcf_upload_completed and fasta_upload_completed and n_clicks > 0:
        # Create post document
        post = {
            'analysis_id': analysis_id,
            'analysis_name': analysis_name,
            'creation_date': datetime.now(),
            'last_accession_date': datetime.now(),
            'last_update_date': datetime.now(),
            'curator_name': curator_name,
            'analysis_progress': 0,
            'vcf_filepath': vcf_filepath,
            'fasta_filepath': fasta_filepath,
        }

        # Connect to MongoDB (somaticseeker::analysis_list)
        client = MongoClient()
        db = client['somaticseeker']
        collection = db['analysis_list']
        collection.insert_one(post)

@app.callback(
    Output('run_analysis_button', component_property='disabled'),
    [
        Input('analysis_name_input', component_property='value'),
        Input('curator_name_input', component_property='value'),
        Input('vcf_upload', component_property='isCompleted'),
        Input('fasta_upload', component_property='isCompleted'),
        Input('run_analysis_button', component_property='n_clicks'),
        Input('run_analysis_button', component_property='disabled'),
    ]
)

def run_analysis_button_disable(analysis_name_value, curator_name_value, vcf_upload_completed, fasta_upload_completed, n_clicks, disabled):
    if not analysis_name_value or not curator_name_value or not vcf_upload_completed or not fasta_upload_completed or n_clicks > 0:
        disabled = True
    else:
        disabled = False
    return disabled

@app.callback(
        Output('run_pipeline', component_property='chilren'),
        [
            Input('vcf_upload', component_property='isCompleted'),
            Input('fasta_upload', component_property='isCompleted'),
            State('vcf_upload', 'fileNames'),
            State('fasta_upload', 'fileNames'),
            Input('run_analysis_button', component_property='n_clicks'),
        ]
)

def run_pipeline(vcf_upload_completed, fasta_upload_completed, vcf_filename, fasta_filename, n_clicks):
    global folder
    global analysis_id

    if n_clicks > 0:
        # The following config variables must be loaed from an App config file
        snakefile = '/opt/msm_tfm/vcf_annotation_pipeline/Snakefile'
        configfile = '/opt/msm_tfm/vcf_annotation_pipeline/config.yaml'
        cores = 4
        workdir = str(Path(folder)/analysis_id/'pipeline_results')
        vcf_filepath = str(Path(folder)/analysis_id/vcf_filename[0])
        refgenome_filepath = str(Path(folder)/analysis_id/fasta_filename[0])
        cmd = ' '.join([
            "/usr/local/bin/snakemake",
            f"--snakefile {snakefile} --cores {cores} --configfile {configfile}",
            f"--config workdir={workdir} input_vcf={vcf_filepath} refgenome_filepath={refgenome_filepath} db_name={analysis_id}",
            "--wms-monitor http://127.0.0.1:5000",
        ])
        with subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True, shell=True) as p:
            for b in p.stdout:
                print(b, end='') # b is the byte rom stdout
            for b in p.stderr:
                print(b, end='') # b is the byte rom stdout
        if p.returncode != 0:
            raise subprocess.CalledProcessError(p.returncode, p.args)
        # Do something else

# Layout

h_style = {
    'text-align':'left',
    'marginLeft': '20px',
    'marginRight': '20px',
    'marginTop': '20px',
    'marginBottom': '20px',
    'fontWeight': 'bold',
}

layout = html.Div([
    html.H1('Somatic Seeker', style=h_style),
    html.Hr(),
    html.H2('New analysis', style=h_style),
    analysis_name_input,
    curator_name_input,
    vcf_upload,
    fasta_upload,
    run_analysis_button,
    panoptes_button,
    html.Div(id='new_analysis_db_post'),#, style={'display':'none'})
    html.Div(id='run_pipeline'),
])

