#!/usr/bin/python

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

from ansible.plugins.action import ActionBase
from ansible.errors import AnsibleError, AnsibleFileNotFound

class ActionModule(ActionBase):
    def run(self, tmp=None, task_vars=None):

        if task_vars is None:
            task_vars = dict()

        result = super(ActionModule, self).run(tmp, task_vars)

        module_args = self._task.args.copy()
        source = self._task.args.get('source', None)
        filename = self._task.args.get('filename', None)
        fdata = None

        result = dict(
            changed = False,
            status = 500
        )

        if source == 'local':
            try:
                #fdata = self._loader.get_real_file(filename, False)
                fdata = self._find_needle('', filename)
            except AnsibleError:
                result['failed'] = True
                result['msg'] = to_native(get_exception())
                return result
        else:
            result['failed'] = True
            result['msg'] = "Unimplemented"
            return result

        task_vars.update( dict(
            filename = fdata,
            ), 
        )
        mod_result = self._execute_module(module_name='nginxinc.nginx_management_suite.nms_sm_uploader',
                            module_args=module_args, task_vars=task_vars)
        result.update( mod_result )
        return result
