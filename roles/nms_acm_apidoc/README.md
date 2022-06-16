NMS Licensing
=============

NGINX Management Suite (NMS) Ansible role for creating ACM API-Docs


Requirements
------------

* [NGINX Instance Manager](https://www.nginx.com/products/nginx-instance-manager/)

Role Variables
--------------

Certificate validation `nms_validate_certs` defaults to true, and `nms_api_version` to '/api/v1'

`nms_fqdn`
`nms_api_version`
`nms_validate_certs`
`nms_acm_workspace`
`nms_acm_apidoc`


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
    nms_validate_certs: false
    f1_oas3_file: "/tmp/ergastf1.oas3.yaml"

  tasks:

  - name: Setup Authentication with NMS
    include_role: 
      name: nginxinc.nginx_management_suite.nms_authenticate

  - name: Uplaod F1 API specification
    include_role:
      name: nginxinc.nginx_management_suite.nms_acm_apidoc
    vars:
      nms_acm_workspace:
        name: formula1
      nms_acm_apidoc:
        name: f1-results-api-1
        spec: "{{ lookup('file', f1_oas3_file) | from_yaml }}"

```

License
-------

[Apache License, Version 2.0](./LICENSE)

Author Information
------------------

[Mark Boddington](https://github.com/TuxInvader)

&copy; [NGINX, Inc.](https://www.nginx.com/) 2022

