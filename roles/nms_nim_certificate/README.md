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

    - name: Upsert Certificate
    include_role:
      name: nginxinc.nginx_management_suite.nms_nim_certificate
    vars:
      #nms_instances:
      #  - nginx1
      #  - nginx2
      nms_nim_certificate:
        name: NIM
        #instanceRefs:
        #  - /api/platform/v1/systems/<sysuid>/instances/<uid>
        #  - /api/platform/v1/systems/<sysuid>/instances/<uid>
        certPEMDetails:
          type: PEM
          caCerts:
            - |
              -----BEGIN CERTIFICATE-----

              -----END CERTIFICATE-----
          publicCert: |
            -----BEGIN CERTIFICATE-----
            -----END CERTIFICATE-----
          privateKey: |
            -----BEGIN PRIVATE KEY-----
            -----END PRIVATE KEY-----

```

To publish the certificate to an NGINX instance, you need to provide the instanceRefs paramater as part of
the `nms_nim_certificate` dictionary. Alternatively you can provide an optional `nms_instances` list which
includes the displayNames of the instances.

License
-------

[Apache License, Version 2.0](./LICENSE)

Author Information
------------------

[Mark Boddington](https://github.com/TuxInvader)

&copy; [NGINX, Inc.](https://www.nginx.com/) 2022

