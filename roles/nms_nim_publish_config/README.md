NMS Licensing
=============

NGINX Management Suite (NMS) Ansible role for publishing configuration through NIM


Requirements
------------

* [NGINX Instance Manager](https://www.nginx.com/products/nginx-instance-manager/)

Role Variables
--------------

`nms_fqdn`
`nms_api_version`
`nms_validate_certs`
`nms_nim_publish`

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

  - name: Get Instances
    include_role:
      name: nginxinc.nginx_management_suite.nms_get_instance_refs

  - name: Get Config Templates
    include_role:
      name: nginxinc.nginx_management_suite.nms_nim_get_config_template_refs

  - name: Publish Config Template 'base-config' to instance 'nginx1'
    include_role:
      name: nginxinc.nginx_management_suite.nms_nim_publish_config
    vars:
      nms_nim_publish:
        config:
          configUid: "{{ nms_nim_config_template_refs['base-config'].uid }}"
        rel: "{{ nms_instance_refs.nginx1.rel }}"

```

The above example publishes a configuration template to a specific NGINX instance by providing the
`uid` of the template and the instance relative link in the `rel` key.

You can also put a configuration directly in the `config` element using the same structure as a config
template. See the `nms_nim_config_template` role for a complete example. Basic formatting is:

```
  - name: Publish a config ddirectly to an instance
    include_role:
      name: nginxinc.nginx_management_suite.nms_nim_publish_config
    vars:
      nms_nim_publish:
        rel: /api/platform/v1/systems/74e598eb-0d27-0247-a7f3-6e39dbb91d09/instances/2ca64bea-1fa4-5325-9f5a-1989ef5dfafa
        config:
          auxFiles:
            rootDir: /
            files: []
          configFiles:
            rootDir: /etc/nginx
            files: []
```



License
-------

[Apache License, Version 2.0](./LICENSE)

Author Information
------------------

[Mark Boddington](https://github.com/TuxInvader)

&copy; [NGINX, Inc.](https://www.nginx.com/) 2022

