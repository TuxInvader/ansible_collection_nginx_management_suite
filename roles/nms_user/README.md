NMS Licensing
=============

NGINX Management Suite (NMS) Ansible role for Licensing


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

  - name: Create the user for Developer Debbie
    include_role: 
      name: nginxinc.nginx_management_suite.nms_user
    vars:
      nms_user:
        metadata:
          description: Developer Deborah
          displayName: Deborah Debuggington
          name: devdebs
        userDef:
          email: devdebss@nginx.com
          firstName: Deborah
          lastName: Debuggington
          groups:
            - ref: /api/platform/v1/groups/green
          roles:
            - ref: /api/platform/v1/roles/green

```

License
-------

[Apache License, Version 2.0](./LICENSE)

Author Information
------------------

[Mark Boddington](https://github.com/TuxInvader)

&copy; [NGINX, Inc.](https://www.nginx.com/) 2022

