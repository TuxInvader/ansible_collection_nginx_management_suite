NMS Licensing
=============

NGINX Management Suite (NMS) Ansible role for configuring the Agent 

Requirements
------------

* [NGINX Instance Manager](https://www.nginx.com/products/nginx-instance-manager/)

Role Variables
--------------

* `nms_fqdn`
* `nms_validate_certs`
* `nms_agent_instance_group`

NAP Settings
* `nms_agent_nap_enable` (default - false)
* `nms_agent_nap_syslog_port` (default = 514)
* `nms_agent_nap_collection_seconds` (default = 15)

DevPortal Settings for ACM
* `nms_acm_devportal` (default = false)
* `nms_acm_devportal_db` (default = postgres)
* `nms_acm_devportal_db_init` (default = true)

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

