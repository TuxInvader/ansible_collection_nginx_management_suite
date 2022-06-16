NMS Licensing
=============

NGINX Management Suite (NMS) Ansible role for getting the list of instance groups


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

  - name: Get Instances Groups
    include_role:
      name: nginxinc.nginx_management_suite.nms_get_instance_group_refs

```

This returns a fact `nms_instance_group_refs` containing the instance groups in the form

```
{
    "foobar": {
            "description": "Foo Servers",
            "displayName": "foobar",
            "instances": [
                "d825d962-4e57-5a46-b460-984ed82a321f"
            ],
            "name": "foobar",
            "rel": "/api/platform/v1/instance-groups/17f94130-e7c0-4cda-91b6-39b142bed1b8",
            "uid": "17f94130-e7c0-4cda-91b6-39b142bed1b8"
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

