# Ansible Collection - NGINX Management Suite

Documentation for the collection.

Drop this folder into ~/.ansible/collections/ansible_collections/nginxinc 

Then use in a playbook... 

```yaml

- hosts: localhost
  gather_facts: no

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

NSM/NIM Management

* [Licensing](#licensing)
* [RBAC Tag Systems](#rbac-tag-systems)
* [RBAC User Roles](#rbac-user-roles)
* [RBAC Users](#rbac-users)
* [Instance Groups](#instance-groups)

NIM Configuration Management
* [Configuration Templates](#configuration-templates)
* [Certificates](#certificates)
* [Publish Configuration](#publish-configuration)

### Licensing

```yaml
  - name: License NMS
    include_role:
      name: nginxinc.nginx_management_suite.nms_license
    vars:
      nms_license: "{{ lookup('file', /home/mark/nms_license.txt') }}"
```

### RBAC Tag Systems

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

### RBAC User Roles

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
            - access: WRITE
              scope: INSTANCE-MANAGEMENT
              tags:
                - env:dev
                - env:test
            - access: READ
              scope: INSTANCE-MANAGEMENT
              tags:
                - env:prod
            - access: WRITE
              scope: SETTINGS
```

### RBAC Users

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

### Instance Groups

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

### Configuration Templates

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

### Certificates

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
          - "{{ nms_instance_refs.nginx1.rel }}"
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

### Publish Configuration

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


