NMS Licensing
=============

NGINX Management Suite (NMS) Ansible role for creating ACM workspace


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
    nms_acm_team: services

  tasks:

  - name: Setup Authentication with NMS
    include_role: 
      name: nginxinc.nginx_management_suite.nms_authenticate

  - name: Create F1 API workspace
    include_role:
      name: nginxinc.nginx_management_suite.nms_acm_workspace
    vars:
      nms_acm_workspace:
        name: formula1
        contactDetails:
          adminEmail: admin@nginx.com
          adminName: Alfred the API Developer
        metadata:
          description: Formula 1 API workspace

  - name: Create F1 API Proxies
    include_role:
      name: nginxinc.nginx_management_suite.nms_acm_proxies
    vars:
      nms_acm_workspace:
        name: formula
      nms_acm_proxies:
        name: f1-api
        version: 1.0
        portalConfig:
          targetProxyHost: f1docs.foo.com
          hostname: f1docs.foo.com
          category: ""
        proxyConfig:
          hostname: f1dev.foo.com
          backends:
          - serviceName: f1-svc
            serviceTargets:
            - hostname: f1.foo.com
          ingress:
            basePath: /api/f1

```

License
-------

[Apache License, Version 2.0](./LICENSE)

Author Information
------------------

[Mark Boddington](https://github.com/TuxInvader)

&copy; [NGINX, Inc.](https://www.nginx.com/) 2022

