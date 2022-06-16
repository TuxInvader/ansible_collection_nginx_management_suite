NMS Licensing
=============

NGINX Management Suite (NMS) Ansible role for getting the list of stored config templates


Requirements
------------

* [NGINX Instance Manager](https://www.nginx.com/products/nginx-instance-manager/)

Role Variables
--------------

`nms_auth_header`
`nms_fqdn`
`nms_api_version`
`nms_validate_certs`

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

  - name: Get Config Templates
    include_role:
      name: nginxinc.nginx_management_suite.nms_nim_config_template_refs

```

This returns a fact `nms_nim_config_template_refs` containing the instances in the form

```
{
    "base-config": {
        "configName": "base-config",
        "createTime": "2022-02-02T15:08:01.524Z",
        "rel": "/api/platform/v1/configs/724cfcbb-c94c-4d37-800d-96bcf7e6f63e",
        "uid": "724cfcbb-c94c-4d37-800d-96bcf7e6f63e",
        "updateTime": "2022-02-02T15:11:02Z"
    }
}
```

License
-------

[Apache License, Version 2.0](./LICENSE)

Author Information
------------------

[Mark Boddington](https://github.com/TuxInvader)

&copy; [NGINX, Inc.](https://www.nginx.com/) 2022

