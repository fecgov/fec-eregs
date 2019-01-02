import sys
from os import path
from subprocess import call

"""
to run this script for eregs parsing and loading, you need:

1. install docker on your machine
2. make sure the eregs docker image is available on your machine:
   this is the command to pull the docker image from docker hub(https://hub.docker.com/r/eregs/parser/) - 
   you may need to register an account if you don't have one:
   >> docker pull eregs/parser

   or you can build the docker image from the Dockerfile in current directory:
   >> docker build -t "eregs/parser" .
3. make sure eregs.sh is available in same folder and executbile:
   >> chmod +x eregs.sh

refer this link for more details:
https://eregs-parser.readthedocs.io/en/latest/installation.html
"""

with open('load_regs/fec_reg_parts.txt') as parts:
    env = sys.argv[1].strip()
    if env == 'local':
        url = 'http://localhost:8000/api'
    else:
        url = "https://fec-{0}-eregs.app.cloud.gov/regulations/api".format(env)

    for part in parts:
        call(['./eregs.sh', 'pipeline', '11', part, url, '--only-latest'])