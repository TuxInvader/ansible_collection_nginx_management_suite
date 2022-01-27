NMS Licensing
=============

NGINX Managment Suite (NMS) Ansible role for Licensing


Requirements
------------

* [NGINX Instance Manager](https://www.nginx.com/products/nginx-instance-manager/)

Role Variables
--------------

`nms_user_name`

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

```

License
-------

[Apache License, Version 2.0](./LICENSE)

Author Information
------------------

[Mark Boddington](https://github.com/TuxInvader)

&copy; [NGINX, Inc.](https://www.nginx.com/) 2022

