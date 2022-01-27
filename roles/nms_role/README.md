NMS Licensing
=============

NGINX Managment Suite (NMS) Ansible role for roles


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

  - name: Setup role facts
    set_fact:
      nms_roles:
        - metadata:
            kind: role
            name: green
            displayName: The Green Team (Devs)
            tags:
              - dev
              - test
              - prod
          roleDef:
            permissions:
              - access: WRITE
                scope: INSTANCE-MANAGEMENT
                tags:
                  - env:dev
                  - env:test
              - access: READ
                scope: INSTANCE-MANAGEMENT
                tags:
                  - env:prod
              - access: WRITE
                scope: SETTINGS
        - metadata:
            kind: role
            name: red
            displayName: The Red Team (Ops)
            tags:
              - dev
              - test
              - prod
          roleDef:
            permissions:
              - access: READ
                scope: INSTANCE-MANAGEMENT
                tags:
                  - env:test
              - access: WRITE
                scope: INSTANCE-MANAGEMENT
                tags:
                  - env:prod
              - access: WRITE
                scope: SETTINGS


  - name: create NMS Roles
    include_role: 
      name: nginxinc.nginx_management_suite.nms_license
    loop: "{{ nms_roles }}"
    loop_control:
      label: "{{ nms_role.metadata.name }}"
      loop_var: nms_role

```

License
-------

[Apache License, Version 2.0](./LICENSE)

Author Information
------------------

[Mark Boddington](https://github.com/TuxInvader)

&copy; [NGINX, Inc.](https://www.nginx.com/) 2022

