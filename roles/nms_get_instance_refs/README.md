NMS Licensing
=============

NGINX Management Suite (NMS) Ansible role for getting the list of instances


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

  - name: Get Instances
    include_role:
      name: nginxinc.nginx_management_suite.nms_get_instance_refs

```

This returns a fact `nms_instance_refs` containing the instances in the form

```
{
    "nginx1": {
            "displayName": "nginx1",
            "rel": "/api/platform/v1/systems/5bece5df-c189-8d4e-ab36-c1fd6c542aa1/instances/d825d962-4e57-5a46-b460-984ed82a321f",
            "systemUid": "5bece5df-c189-8d4e-ab36-c1fd6c542aa1",
            "uid": "d825d962-4e57-5a46-b460-984ed82a321f"
    },
    "nginx2": {
            "displayName": "nginx2",
            "rel": "/api/platform/v1/systems/615f9cfe-65ff-084c-8690-429a48304363/instances/5cbddfb9-0cca-5819-ab2f-40692f71054c",
            "systemUid": "615f9cfe-65ff-084c-8690-429a48304363",
            "uid": "5cbddfb9-0cca-5819-ab2f-40692f71054c"
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

