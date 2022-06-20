NMS Licensing
=============

NGINX Management Suite (NMS) Ansible role to help building ACM policies

This role takes in a list of policies, and sets a fact called `nms_acm_policy_bundle` which
contains the policies using the provided params and/or the same defaults as the ACM UI.

The `nms_acm_policy_bundle` can then be used with the `nms_acm_proxies` role to publish the
configuration and policies. See the example below.

Requirements
------------

* [NGINX Instance Manager](https://www.nginx.com/products/nginx-instance-manager/)

Role Variables
--------------


`nms_acm_policies`

The NMS ACM Policy will create/update the fact `nms_acm_policy_bundle` with the policies provided. `nms_acm_policies` has the following fields....

`new` - Set to true to start a fresh policy fact with this policy as the first entry
`policies` - A list of policies including `type` and `params`.

`type` - Set to one of the supported policy types
`params` - Set to the parameters for the policy

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

  - name: Create proxy policies
    include_role:
      name: nginxinc.nginx_management_suite.nms_acm_policy_factory
    vars:
      nsm_acm_policies:
        new: true
        policies:
        - type: proxy-request-headers
          params:
            proxy_custom_headers:
            - key: x-foo
              value: header.x_foo
        - type: cors

  - name: Create F1 API Proxies
    include_role:
      name: nginxinc.nginx_management_suite.nms_acm_proxies
    vars:
      nms_acm_workspace:
        name: formula1
      nms_acm_proxies:
        name: f1-api
        version: v1.0
        specRef: f1-results-api-1
        portalConfig:
          targetProxyHost: f1-api.foo.com
          hostname: devportal.foo.com
          category: ""
        proxyConfig:
          policies: "{{ nms_acm_policy_bundle }}"
          hostname: f1-api.foo.com
          backends:
          - serviceName: f1-svc
            serviceTargets:
            - hostname: f1-backend.internal.foo.com
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

