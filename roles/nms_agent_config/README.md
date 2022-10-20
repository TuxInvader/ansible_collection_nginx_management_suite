NMS Licensing
=============

NGINX Management Suite (NMS) Ansible role for configuring the Agent 

Requirements
------------

* [NGINX Instance Manager](https://www.nginx.com/products/nginx-instance-manager/)

Role Variables
--------------

`nms_fqdn`
`nms_validate_certs`
`nms_agent_instance_group`
`nms_agent_force_install`

Dependencies
------------

None

Example Playbook
----------------

```yaml
- hosts: prod_gateways
  gather_facts: no

  vars:
    nms_fqdn: "ngx-ctrl.mydomain.com"
    nms_validate_certs: false
    nms_agent_instance_group: prod_api_gateways
    nms_agent_force_install: true

  tasks:

  - name: Setup Agent on API Gateways
    include_role:
      name: nginxinc.nginx_management_suite.nms_agent_config

```

The above example will ensure that the NGINX Agent is installed/updated to the version available on NMS.
It will set the instance group to the name in `nms_agent_instance_group` and restart the agent if required.

License
-------

[Apache License, Version 2.0](./LICENSE)

Author Information
------------------

[Mark Boddington](https://github.com/TuxInvader)

&copy; [NGINX, Inc.](https://www.nginx.com/) 2022
