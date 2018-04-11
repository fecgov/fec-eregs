import sys
from os import path

sys.path.insert(0, path.join(path.dirname(path.dirname(sys.executable)), 'src', 'regulations-parser'))
import manage
manage.main(['manage.py', 'migrate', '--fake-initial'])

with open('load_regs/fec_reg_parts.txt')as parts:
    env = sys.argv[1].strip()
    if env == 'local':
        url = 'http://localhost:8000/api'
    else:
        url = "https://fec-{0}-eregs.app.cloud.gov/regulations/api".format(env)

    for part in parts:
        args = ['manage.py', 'eregs', 'pipeline', '11', part,
                url, '--only-latest']
        manage.main(args)
