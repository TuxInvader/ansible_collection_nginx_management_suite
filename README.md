# Ansible Collection - NGINX Management Suite

Documentation for the collection.

Drop this folder into ~/.ansible/collections/ansible_collections/nginxinc

Then use in a playbook...

```yaml

- hosts: localhost
  gather_facts: no
  connection: local

  vars_files:
    - ~/src/ansible_nim_secrets.yaml

  vars:
    nms_user_name: "{{ secret_user_name }}"
    nms_user_passwd: "{{ secret_user_passwd }}"
    nms_fqdn: "{{ secret_fqdn }}"

  tasks:
  - name: Setup Authentication with NMS
    include_role:
      name: nginxinc.nginx_management_suite.nms_authenticate

```

You will always need to provide the above variables, and call the `nms_authenticate` role before you
attempt to use any other of the roles in the collection. The examples below show the roles required
to perform specific tasks, and assume that you have performed the `nms_authenticate` prior to using
them.

## Variables

To use the roles you must provide authentication details in the `nms_user_name` and `nms_user_passwd`,
and also provide the FQDN of the NMS system in `nms_fqdn`.

```yaml
  vars:
    nms_user_name: "{{ secret_user_name }}"
    nms_user_passwd: "{{ secret_user_passwd }}"
    nms_fqdn: "{{ secret_fqdn }}"
```

There are some additional variables which control the behaviour, but they have defaults assigned.

```yaml
    nms_auth_type:           "basic"
    nms_api_version:         "/api/platform/v1"
    nms_validate_certs:      false
    nms_license_force:       false
    nms_nim_publish_wait:    true
```

## Example tasks

----

### RBAC

The NMS RBAC system is made up of three components (roles, users, and groups).

* [RBAC Roles](#rbac-roles)
* [RBAC Users](#rbac-users)
* [RBAC Groups](#rbac-groups)

**Roles**: A collection of permissions for one or more features. The definition also includes the list of actions (CRUD) that can be performed for that feature.

**Users**: A username and set of credentials, these can be created in NMS itself or added come from an external identity provider (idP)

**Groups**: A collection of users. Groups are only used with an external idP to confer role permissions to members.

----

### NMS/NIM Management

* [Licensing](#licensing)
* [Agent Install / Configuration](#agent-install--configuration)
* [Tagging Systems](#tagging-systems-not-used-for-rbac)
* [Instance Groups](#instance-groups)

----

### NIM Configuration Management

* [NIM Configuration](./docs/README_NIM.md)

----

### NMS API Connectivity Manager (ACM)

* [ACM Configuration](./docs/README_ACM.md)

----

### NMS Security Module (SM)

* [NMS-SM Configuration](./docs/README_SM.md)

----

## Licensing

```yaml
  - name: License NMS
    include_role:
      name: nginxinc.nginx_management_suite.nms_license
    vars:
      nms_license: "{{ lookup('file', /home/mark/nms_license.txt') }}"
```

## Agent Install / Configuration

NMS uses an agent to manage deployed nginx instances. Unlike most of the other roles in this collection (which interact with the NMS API), this role cannot be run on `localhost` and should instead target the NGINX systems directly.

```yaml
- hosts: nginx
  gather_facts: yes

  vars:
    nms_fqdn: "nim1.mydomain.com"
    nms_validate_certs: false
    nms_agent_nap_enable: true
    nms_agent_nap_collection_seconds: 15
    nms_agent_nap_syslog_port: 5514

  tasks:

  - name: Setup Agent on API Gateways
    include_role:
      name: nginxinc.nginx_management_suite.nms_agent_config
```

There are additional variables which can be defined to enable NAP management, and for use with the ACM module to create proxies, and enable developer portal configuration.

See the [nms_agent_config Documentation](/roles/nms_agent_config/README.md) for more information.

## Tagging Systems (Not Used for RBAC)

In early versions of NMS we used system tags as a way to apply RBAC rules. This is no longer the case, but you can still tag systems if you wish.

```yaml
  - name: Tag Systems
    include_role:
      name: nginxinc.nginx_management_suite.nms_system_tags
    vars:
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
    loop: "{{ nms_systems }}"
    loop_control:
      label: "{{ nms_system.hostname }}"
      loop_var: nms_system
```

## RBAC Roles

```yaml
  - name: Create NMS Role
    include_role:
      name: nginxinc.nginx_management_suite.nms_role
    vars:
      nms_role:
        metadata:
          kind: role
          name: green
          displayName: The Green Team (Devs)
          tags:
            - dev
            - test
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
                  - All
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
```

## RBAC Users

```yaml
  - name: Create the user for Developer Debbie
    include_role:
      name: nginxinc.nginx_management_suite.nms_user
    vars:
      nms_user:
        metadata:
          description: Developer Deborah
          displayName: Deborah Debuggington
          name: devdebs
        userDef:
          email: devdebss@nginx.com
          firstName: Deborah
          lastName: Debuggington
          groups:
            - ref: /api/platform/v1/groups/green
          roles:
            - ref: /api/platform/v1/roles/green
```

## RBAC Groups

TODO

```yaml
```

## Instance Groups

```yaml
  - name: Setup Instance Group with NMS
    include_role:
      name: nginxinc.nginx_management_suite.nms_instance_group
    vars:
      nms_instance_group:
        name: production
        description: Production Instances
        displayName: AzureProd
```
