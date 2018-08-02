import os
import yaml

# Set defaults
filter = dict(
    partitions = [],
)
system = dict(
    use_acct_db = False,
    use_cors = False,
    debug = False,
    host = '0.0.0.0',
    port = 5000,
    serve_index = False,
    archive_usage_load = False,
    archive_wait_time = 60,
    archive_path = 'db.json',
)

# Change to yaml values
ymlfile = None
if os.path.exists("config.yml"):
    ymlfile = open("config.yml", 'r')
elif os.path.exists(os.environ['SLURM_REST_API_CONFIG']):
    ymlfile = open(os.environ['SLURM_REST_API_CONFIG'], 'r')

if ymlfile is not None:
    try:
        cfg = yaml.load(ymlfile)
        if cfg is not None and 'filter' in cfg:
            for n in cfg['filter']:
                filter[n] = cfg['filter'][n]
        if cfg is not None and 'system' in cfg:
            for n in cfg['system']:
                system[n] = cfg['system'][n]

    finally:
        ymlfile.close()
