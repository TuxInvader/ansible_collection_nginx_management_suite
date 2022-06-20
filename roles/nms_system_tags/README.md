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

  - name: Create System tags list
    set_fact:
      nms_systems:
        - hostname: mbngx1
          tags:
            - env:prod
            - dc:azure
        - hostname: mbngx2
          tags:
            - env:test
            - dc:azure
        - hostname: mbngx3
          tags:
            - env:dev
            - dc:azure

  - name: Tag Systems
    include_role: 
      name: nginxinc.nginx_management_suite.nms_system_tags
    loop: "{{ nms_systems }}"
    loop_control:
      label: "{{ nms_system.hostname }}"
      loop_var: nms_system


```

License
-------

[Apache License, Version 2.0](./LICENSE)

Author Information
------------------

[Mark Boddington](https://github.com/TuxInvader)

&copy; [NGINX, Inc.](https://www.nginx.com/) 2022

