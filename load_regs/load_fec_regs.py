import sys
from os import path
from subprocess import run

with open('load_regs/fec_reg_parts.txt') as parts:
    env = sys.argv[1].strip()
    if env == 'local':
        url = 'http://localhost:8000/api'
    else:
        url = "https://fec-{0}-eregs.app.cloud.gov/regulations/api".format(env)

    for part in parts:
        run(['eregs', 'pipeline', '11', part, url, '--only-latest'])
