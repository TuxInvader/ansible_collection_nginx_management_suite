#!/usr/bin/python

from __future__ import (absolute_import, division, print_function)
from ansible.module_utils.basic import AnsibleModule
__metaclass__ = type

import requests
import json

DOCUMENTATION = r'''

'''

EXAMPLES = r'''

'''

RETURN = r'''

'''

def run_module():

    module_args = dict(
        revisionTimestamp=dict(type='str', required=True),
        url=dict(type='str', required=True),
        filename=dict(type='str', required=True),
        source=dict(type='str', required=True),
        headers=dict(type='str', required=True),
        validate_certs=dict(type='bool', required=True)
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    result = dict(
        changed=False,
        status=419,
        response={},
    )

    if module.check_mode:
        module.exit_json(**result)

    data = [ ('revisionTimestamp', module.params['revisionTimestamp']) ]
    multipart = [
        ('filename', (module.params['filename'], open(module.params['filename'],'rb'), 'application/octet-stream'))
    ]
    headers = json.loads(module.params['headers'])

    response = requests.post(module.params['url'], files=multipart, data=data,
                   verify=module.params['validate_certs'], headers=headers)

    result['status'] = response.status_code
    result['response'] = response.json()

    if result['status'] in [400,401,403] or result['status'] > 500:
        module.fail_json(msg='Upload Failed', **result)
    module.exit_json(**result)

def main():
    run_module()

if __name__ == '__main__':
    main()

