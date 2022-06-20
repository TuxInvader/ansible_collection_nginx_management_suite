NMS Authentication
==================

NGINX Management Suite (NMS) Ansible role for configuring the API Authentication


Requirements
------------

* [NGINX Instance Manager](https://www.nginx.com/products/nginx-instance-manager/)

Role Variables
--------------

`nms_fqdn` - The FQDN of the NMS/NIM host.
`nms_user_name` - The username to connect to NMS/NIM.
`nms_user_passwd` - The password for the above user.
`nms_auth_type` - The Authentication type to use. Currently this is just `basic` for basic auth.

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
      nginxinc.nginx_management_suite.nms_authenticate


```

License
-------

[Apache License, Version 2.0](./LICENSE)

Author Information
------------------

[Mark Boddington](https://github.com/TuxInvader)

&copy; [NGINX, Inc.](https://www.nginx.com/) 2022

