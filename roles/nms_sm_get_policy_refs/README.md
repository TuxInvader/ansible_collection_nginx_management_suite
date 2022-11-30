NMS Licensing
=============

NGINX Management Suite - Security Module (NMS-SM) Ansible role for Getting a dictionary of NAP Policies


Requirements
------------

* [NGINX Instance Manager](https://www.nginx.com/products/nginx-instance-manager/)

Role Variables
--------------
`nms_fqdn`
`nms_api_version`
`nms_validate_certs`
`nms_sm_policy`

Dependencies
------------

None

Example Playbook
----------------

```yaml
- hosts: localhost
  gather_facts: no

  vars:
    nms_user_name: "admin"
    nms_user_passwd: "myPassword"
    nms_fqdn: "ngx-ctrl.mydomain.com"
    nms_auth_type: "basic"
    nms_api_version: "/api/platform/v1"
    nms_validate_certs: false

  tasks:

  - name: Setup Authentication with NMS
    include_role: 
      name: nginxinc.nginx_management_suite.nms_authenticate

  - name: Upsert NSM-SM Policy
    include_role: 
      name: nginxinc.nginx_management_suite.nms_sm_policy
    vars:
      nms_sm_policy_state: present
      nms_sm_policy:
        metadata:
          name: default-policy
          displayName: Default Policy
          description: Base policy
        content:
          policy:
            name: app_protect_default_policy
            template:
              name: POLICY_TEMPLATE_NGINX_BASE

```

After running the list of current configurations will be available in `nms_nim_config_template_refs`

License
-------

[Apache License, Version 2.0](./LICENSE)

Author Information
------------------

[Mark Boddington](https://github.com/TuxInvader)

&copy; [NGINX, Inc.](https://www.nginx.com/) 2022

