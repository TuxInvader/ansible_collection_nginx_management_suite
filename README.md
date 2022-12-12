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
### NSM/NIM Management

* [Licensing](#licensing)
* [Agent Install / Configuration](#agent-install--configuration)
* [Tagging Systems](#tagging-systems-not-used-for-rbac)
* [Instance Groups](#instance-groups)

----
### NIM Configuration Management
* [Staged Configurations](#staged-configurations)
* [Certificates](#certificates)
* [Publish Staged Configuration](#publish-staged-configuration)
* [Publish Direct Configuration](#publish-direct-configuration)

----
### NMS API Connectivity Manager (ACM)
* [ACM Configuration](./README_ACM.md)

----
### NMS Security Module (SM)
* [NMS-SM Configuration](./README_SM.md)

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

## Staged Configurations

Upsert a configuration template (Staged Configuration) called base-config.

```yaml
  - name: Create NIM Config Template
    include_role:
      name: nginxinc.nginx_management_suite.nms_nim_config_template
    vars:
      nms_nim_config_template:
        configName: base-config
        auxFiles:
          rootDir: /
          files: []
        configFiles:
          rootDir: /etc/nginx
          files:
          - name: /etc/nginx/nginx.conf
            contents: |
              CnVzZXIgIG5naW54Owp3b3JrZXJfcHJvY2Vzc2VzICBhdXRvOwoKZXJyb3JfbG9nICAvdmFyL2xv
              Zy9uZ2lueC9lcnJvci5sb2cgbm90aWNlOwpwaWQgICAgICAgIC92YXIvcnVuL25naW54LnBpZDsK
              CgpldmVudHMgewogICAgd29ya2VyX2Nvbm5lY3Rpb25zICAxMDI0Owp9CgoKaHR0cCB7CiAgICBp
              bmNsdWRlICAgICAgIC9ldGMvbmdpbngvbWltZS50eXBlczsKICAgIGRlZmF1bHRfdHlwZSAgYXBw
              bGljYXRpb24vb2N0ZXQtc3RyZWFtOwoKICAgIGxvZ19mb3JtYXQgIG1haW4gICckcmVtb3RlX2Fk
              ZHIgLSAkcmVtb3RlX3VzZXIgWyR0aW1lX2xvY2FsXSAiJHJlcXVlc3QiICcKICAgICAgICAgICAg
              ICAgICAgICAgICckc3RhdHVzICRib2R5X2J5dGVzX3NlbnQgIiRodHRwX3JlZmVyZXIiICcKICAg
              ICAgICAgICAgICAgICAgICAgICciJGh0dHBfdXNlcl9hZ2VudCIgIiRodHRwX3hfZm9yd2FyZGVk
              X2ZvciInOwoKICAgIGFjY2Vzc19sb2cgIC92YXIvbG9nL25naW54L2FjY2Vzcy5sb2cgIG1haW47
              CgogICAgc2VuZGZpbGUgICAgICAgIG9uOwogICAgI3RjcF9ub3B1c2ggICAgIG9uOwoKICAgIGtl
              ZXBhbGl2ZV90aW1lb3V0ICA2NTsKCiAgICAjZ3ppcCAgb247CgogICAgaW5jbHVkZSAvZXRjL25n
              aW54L2NvbmYuZC8qLmNvbmY7Cn0KCgojIFRDUC9VRFAgcHJveHkgYW5kIGxvYWQgYmFsYW5jaW5n
              IGJsb2NrCiMKI3N0cmVhbSB7CiAgICAjIEV4YW1wbGUgY29uZmlndXJhdGlvbiBmb3IgVENQIGxv
              YWQgYmFsYW5jaW5nCgogICAgI3Vwc3RyZWFtIHN0cmVhbV9iYWNrZW5kIHsKICAgICMgICAgem9u
              ZSB0Y3Bfc2VydmVycyA2NGs7CiAgICAjICAgIHNlcnZlciBiYWNrZW5kMS5leGFtcGxlLmNvbTox
              MjM0NTsKICAgICMgICAgc2VydmVyIGJhY2tlbmQyLmV4YW1wbGUuY29tOjEyMzQ1OwogICAgI30K
              CiAgICAjc2VydmVyIHsKICAgICMgICAgbGlzdGVuIDEyMzQ1OwogICAgIyAgICBzdGF0dXNfem9u
              ZSB0Y3Bfc2VydmVyOwogICAgIyAgICBwcm94eV9wYXNzIHN0cmVhbV9iYWNrZW5kOwogICAgI30K
              I30K
```

## Certificates

This is example gets the instances list from NIM, and then uploads the certificate details
in PEM format, and deploys it to the `nginx1` and `nginx2` instances.

```yaml
  - name: Get Instances
    include_role:
      name: nginxinc.nginx_management_suite.nms_get_instance_refs

  - name: Upsert Certificate
    include_role:
      name: nginxinc.nginx_management_suite.nms_nim_certificate
    vars:
      nms_nim_certificate:
        name: NIM
        instanceRefs:
          - "{{ nms_instance_refs.nginx1.rel }}"
          - "{{ nms_instance_refs.nginx2.rel }}"
        certPEMDetails:
          type: PEM
          caCerts:
            - |
              -----BEGIN CERTIFICATE-----
              MIIFLTCCAxWgAwIBAgICECYwDQYJKoZIhvcNAQELBQAwejELMAkGA1UEBhMCR0Ix
              ................................................................
              5nUkQYke+VOm1JxhUWgsp7UNUNDhLgtgwPPIjEBo1U+P
              -----END CERTIFICATE-----
          publicCert: |
            -----BEGIN CERTIFICATE-----
            MIIFLTCCAxWgAwIBAgICECYwDQYJKoZIhvcNAQELBQAwejELMAkGA1UEBhMCR0Ix
            ................................................................
            5nUkQYke+VOm1JxhUWgsp7UNUNDhLgtgwPPIjEBo1U+P
            -----END CERTIFICATE-----
          privateKey: |
            -----BEGIN PRIVATE KEY-----
            MIIEvwIBADANBgkqhkiG9w0BAQEFAASCBKkwggSlAgEAAoIBAQCpxRW3kpHSaWqB
            ................................................................
            N7XmSBhJEUaEq1qkSRYIfFc+Sw==
            -----END PRIVATE KEY-----
```

## Publish Staged Configuration

This example retrieves the `Instance Groups` and `Configuration Templates`, and then
applies the `basic-config` template to the `production` instance group.

```yaml
  - name: Get Instances Groups
    include_role:
      name: nginxinc.nginx_management_suite.nms_get_instance_group_refs

  - name: Get Config Templates
    include_role:
      name: nginxinc.nginx_management_suite.nms_nim_get_config_template_refs

  - name: Publish Config Templates to Instance Group
    include_role:
      name: nginxinc.nginx_management_suite.nms_nim_publish_config
    vars:
      nms_nim_publish:
        config:
          configUid: "{{ nms_nim_config_template_refs['base-config'].uid }}"
        rel: "{{ nms_instance_group_refs.production.rel }}"

```

## Publish Direct Configuration

This example pushes a configuration directly to an instance not using a template

```yaml
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
            files:
            - name: /etc/nginx/nginx.conf
              contents: |
                CnVzZXIgIG5naW54Owp3b3JrZXJfcHJvY2Vzc2VzICBhdXRvOwoKZXJyb3JfbG9nICAvdmFyL2xv
                Zy9uZ2lueC9lcnJvci5sb2cgbm90aWNlOwpwaWQgICAgICAgIC92YXIvcnVuL25naW54LnBpZDsK
                CgpldmVudHMgewogICAgd29ya2VyX2Nvbm5lY3Rpb25zICAxMDI0Owp9CgoKaHR0cCB7CiAgICBp
                bmNsdWRlICAgICAgIC9ldGMvbmdpbngvbWltZS50eXBlczsKICAgIGRlZmF1bHRfdHlwZSAgYXBw
                bGljYXRpb24vb2N0ZXQtc3RyZWFtOwoKICAgIGxvZ19mb3JtYXQgIG1haW4gICckcmVtb3RlX2Fk
                ZHIgLSAkcmVtb3RlX3VzZXIgWyR0aW1lX2xvY2FsXSAiJHJlcXVlc3QiICcKICAgICAgICAgICAg
                ICAgICAgICAgICckc3RhdHVzICRib2R5X2J5dGVzX3NlbnQgIiRodHRwX3JlZmVyZXIiICcKICAg
                ICAgICAgICAgICAgICAgICAgICciJGh0dHBfdXNlcl9hZ2VudCIgIiRodHRwX3hfZm9yd2FyZGVk
                X2ZvciInOwoKICAgIGFjY2Vzc19sb2cgIC92YXIvbG9nL25naW54L2FjY2Vzcy5sb2cgIG1haW47
                CgogICAgc2VuZGZpbGUgICAgICAgIG9uOwogICAgI3RjcF9ub3B1c2ggICAgIG9uOwoKICAgIGtl
                ZXBhbGl2ZV90aW1lb3V0ICA2NTsKCiAgICAjZ3ppcCAgb247CgogICAgaW5jbHVkZSAvZXRjL25n
                aW54L2NvbmYuZC8qLmNvbmY7Cn0KCgojIFRDUC9VRFAgcHJveHkgYW5kIGxvYWQgYmFsYW5jaW5n
                IGJsb2NrCiMKI3N0cmVhbSB7CiAgICAjIEV4YW1wbGUgY29uZmlndXJhdGlvbiBmb3IgVENQIGxv
                YWQgYmFsYW5jaW5nCgogICAgI3Vwc3RyZWFtIHN0cmVhbV9iYWNrZW5kIHsKICAgICMgICAgem9u
                ZSB0Y3Bfc2VydmVycyA2NGs7CiAgICAjICAgIHNlcnZlciBiYWNrZW5kMS5leGFtcGxlLmNvbTox
                MjM0NTsKICAgICMgICAgc2VydmVyIGJhY2tlbmQyLmV4YW1wbGUuY29tOjEyMzQ1OwogICAgI30K
                CiAgICAjc2VydmVyIHsKICAgICMgICAgbGlzdGVuIDEyMzQ1OwogICAgIyAgICBzdGF0dXNfem9u
                ZSB0Y3Bfc2VydmVyOwogICAgIyAgICBwcm94eV9wYXNzIHN0cmVhbV9iYWNrZW5kOwogICAgI30K
                I30K
```

Another direct publishing example, but with a clear text configuration. The variable `nms_nim_publish_encode_content` enables
Base64 encoding of the file contents before upserting to the NMS API.

```yaml
  - name: Create NIM Config Template
    include_role:
      name: nginxinc.nginx_management_suite.nms_nim_publish_config
    vars:
      nms_nim_publish_decode_content: true
      nms_nim_publish_encode_content: true
      nms_nim_publish_ignore_conflict: true
      nms_nim_publish_validate_config: false
      nms_nim_publish:
        config:
          auxFiles:
            files:
            - name: /etc/app_protect/conf/log_default.json
              contents: |
                {
                  "filter": {
                      "request_type": "illegal"
                  },

                  "content": {
                      "format": "default",
                      "max_request_size": "any",
                      "max_message_size": "5k"
                  }
                }
            rootDir: /
          configFiles:
            files:
            - name: /etc/nginx/nginx.conf
              contents: |
                user  nginx;
                worker_processes  auto;

                error_log  /var/log/nginx/error.log notice;
                pid        /var/run/nginx.pid;

                load_module modules/ngx_http_js_module.so;
                load_module modules/ngx_http_app_protect_module.so;

                events {
                    worker_connections  1024;
                }


                http {
                    include       /etc/nginx/mime.types;
                    default_type  application/octet-stream;

                    log_format  main  '$remote_addr - $remote_user [$time_local] "$request" '
                                      '$status $body_bytes_sent "$http_referer" '
                                      '"$http_user_agent" "$http_x_forwarded_for"';

                    access_log  /var/log/nginx/access.log  main;

                    sendfile        on;
                    #tcp_nopush     on;

                    keepalive_timeout  65;

                    #gzip  on;

                    include /etc/nginx/conf.d/*.conf;
                }
            rootDir: /etc/nginx
        rel: "{{ nms_instance_refs[ item ].rel }}"
    loop:
      - nginx1
      - nginx2

```

