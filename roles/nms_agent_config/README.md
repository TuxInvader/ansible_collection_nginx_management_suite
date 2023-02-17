NMS Agent Configuration
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

Agent Settings
* `nms_agent_state` (default = "present")
* `nms_agent_advanced_metrics` (default =  true)

NAP Settings
* `nms_agent_nap_enable` (default = false)
* `nms_agent_nap_syslog_port` (default = 514)
* `nms_agent_nap_collection_seconds` (default = 15)
* `nms_agent_nap_precompile` (default = true)

DevPortal Settings for ACM
* `nms_acm_devportal` (default = false)
* `nms_acm_devportal_db` (default = postgres)
* `nms_acm_devportal_db_init` (default = true)

The state of the agent is set with the `nms_agent_state` variable, which can be one of: `present`, `absent`, `removed`, `reset`.
Using present or absent will install/start or stop/uninstall the agent on the target host. If you use removed then the agent will
be stopped and uninstalled, and then the instance will be removed from the NMS inventory. Using reset will stop/uninstall,
remove from NMS, and then reinstall/start the agent.

If you use the states which require the playbook to interract with NMS API (`removed` and `reset`), then you need to setup API
authentication before calling this role (like you would with the other API interactive roles).

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

Example Removal
----------------

In this example we run `nms_get_instance_refs` on localhost before we execute the remove action on the nginx-cluster.
Th `nms_agent_config` role will stop/uninstall the agent and then check for the existence of `hostvars['localhost']['nms_instance_refs']`
and use this dictionary for deleting the instances from NMS. if it doesn't exist each ansible host will include the
`nms_get_instance_refs` role and build it's own dictionary of instances.

```
---
- hosts: localhost
  connection: local

  vars:
    nms_user_name: "{{ secret_user_name }}"
    nms_user_passwd: "{{ secret_user_passwd }}"
    nms_fqdn: "{{ secret_fqdn }}"
    nms_auth_type: "basic"
    nms_api_version: "/api/platform/v1"
    nms_validate_certs: false

  tasks:
  - name: Setup Authentication with NMS
    include_role:
      name: nginxinc.nginx_management_suite.nms_authenticate

  - name: Get NGINX instance refs
    include_role:
      name: nginxinc.nginx_management_suite.nms_get_instance_refs

- hosts: nginx-cluster
  gather_facts: yes

  vars:
    nms_user_name: "{{ secret_user_name }}"
    nms_user_passwd: "{{ secret_user_passwd }}"
    nms_fqdn: "{{ secret_fqdn }}"
    nms_auth_type: "basic"
    nms_api_version: "/api/platform/v1"
    nms_validate_certs: false
    nms_agent_state: "removed"

  tasks:
  - name: Setup Authentication with NMS
    include_role:
      name: nginxinc.nginx_management_suite.nms_authenticate

  - name: Setup Agent on API Gateways
    include_role:
      name: nginxinc.nginx_management_suite.nms_agent_config
```


License
-------

[Apache License, Version 2.0](./LICENSE)

Author Information
------------------

[Mark Boddington](https://github.com/TuxInvader)

&copy; [NGINX, Inc.](https://www.nginx.com/) 2022

