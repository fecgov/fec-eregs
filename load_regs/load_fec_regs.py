import sys
from os import path

sys.path.insert(0, path.join(path.dirname(path.dirname(sys.executable)), 'src', 'regulations-parser'))
import manage
manage.main(['manage.py', 'migrate', '--fake-initial'])

with open('load_regs/fec_reg_parts.txt')as parts:
    if sys.argv[1] == 'local':
        url = 'http://localhost:8000/api'
    else:
        env, http_auth_user, http_auth_password = sys.argv[1:]
        url = "https://{0}:{1}@fec-{2}-eregs.app.cloud.gov/regulations/api" \
                 .format(http_auth_user.strip(), http_auth_password.strip(), env.strip())
        print(url)

    for part in parts:
        args = ['manage.py', 'eregs', 'pipeline', '11', part,
                url, '--only-latest']
        manage.main(args)
