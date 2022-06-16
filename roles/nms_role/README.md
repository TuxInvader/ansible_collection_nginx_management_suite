NMS Licensing
=============

NGINX Management Suite (NMS) Ansible role for roles


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
            displayName: The Green Team
            description: Dev/Test Full
            tags:
              - dev
              - test
              - prod
          roleDef:
            permissions:
              - accessTypes:
                - CREATE
                - READ
                - UPDATE
                - DELETE
                feature: INSTANCE-MANAGEMENT
                objects:
                  - resource: Systems
                    values:
                    - nginx1
              - accessTypes:
                - CREATE
                - UPDATE
                - DELETE
                - READ
                feature: INSTANCE-GROUPS
                objects:
                  - resource: "Instance Groups"
                    values:
                    - AzureDev
                    - AzureTest

        - metadata:
            kind: role
            name: red
            displayName: The Red Team
            description: Production SRE
            tags:
              - dev
              - test
              - prod
          roleDef:
            permissions:
              - accessTypes:
                - CREATE
                - READ
                - UPDATE
                - DELETE
                feature: INSTANCE-MANAGEMENT
                objects:
                  - resource: Systems
                    values:
                    - nginx2
              - accessTypes:
                - CREATE
                - UPDATE
                - DELETE
                - READ
                feature: INSTANCE-GROUPS
                objects:
                  - resource: "Instance Groups"
                    values:
                    - AzureProd

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

