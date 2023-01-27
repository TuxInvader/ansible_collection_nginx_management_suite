# NMS NIM Configuration Templates
=============

NGINX Management Suite (NMS) Ansible role for retrieving staged configs

Requirements
------------

* [NGINX Instance Manager](https://www.nginx.com/products/nginx-instance-manager/)

Role Variables
--------------
`nms_fqdn`
`nms_api_version`
`nms_validate_certs`
`nms_nim_decode_config_content`

Dependencies
------------

None

Example Playbook
----------------

When calling the role, you must provided either a relative link to the staged config (as is returned by 
`nms_nim_get_config_template_refs`) in `nms_nim_config_template_rel` or the name of the staged config in
`nms_nim_config_template_name`.

The role will return the API response in `nms_nim_config_template_status` which includes the staged-config
under the `json` key. All of the staged files are base64 encoded. If you want a copy of the configuration
unencoded, then set the role variable `nms_nim_decode_config_content` to `true`. The role will then return
a copy of the configuration in plain text in `nms_nim_decoded_config`

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

  - name: Get our NIM Config Template
    include_role: 
      name: nginxinc.nginx_management_suite.nms_nim_get_config_template
    vars:
      nms_nim_config_template_name: default
      nms_nim_decode_config_content: true

  - name: Display the Config
    debug:
      msg: "{{ nms_nim_decoded_config }}"

```

License
-------

[Apache License, Version 2.0](./LICENSE)

Author Information
------------------

[Mark Boddington](https://github.com/TuxInvader)

&copy; [NGINX, Inc.](https://www.nginx.com/) 2022

