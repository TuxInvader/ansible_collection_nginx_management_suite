# Ansible Collection - NGINX Management Suite

Documentation for the collection.

Drop this folder into ~/.ansible/collections/ansible_collections/nginxinc 

Then use in a playbook... Eg:
```yaml

- hosts: localhost
  gather_facts: no

  vars_files:
    - ~/src/ansible_nim_secrets.yaml

  vars:
    nms_user_name: "{{ secret_user_name }}"
    nms_user_passwd: "{{ secret_user_passwd }}"
    nms_fqdn: "{{ secret_fqdn }}"
    nms_auth_type: "basic"
    nms_api_version: "/api/platform/v1"
    nms_validate_certs: false
    nms_license_file: "/Users/boddington/NGINX/License/nginx-instance-manager-eval.lic"
    nms_license_force: false

  tasks:
  - name: Get License file
    set_fact:
      nms_license: "{{ lookup('file', nms_license_file) }}"

  - name: Setup Authentication with NMS
    include_role:
      name: nginxinc.nginx_management_suite.nms_authenticate

  - name: License NMS
    include_role:
      name: nginxinc.nginx_management_suite.nms_license

  - name: Setup role facts
    set_fact:
      nms_roles:
        - metadata:
            kind: role
            name: green
            displayName: The Green Team (Devs)
            tags:
              - dev
              - test
              - prod
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
        - metadata:
            kind: role
            name: red
            displayName: The Red Team (Ops)
            tags:
              - dev
              - test
              - prod
          roleDef:
            permissions:
              - access: READ
                scope: INSTANCE-MANAGEMENT
                tags:
                  - env:test
              - access: WRITE
                scope: INSTANCE-MANAGEMENT
                tags:
                  - env:prod
              - access: WRITE
                scope: SETTINGS

  - name: create NMS Roles
    include_role:
      name: nginxinc.nginx_management_suite.nms_role
    loop: "{{ nms_roles }}"
    loop_control:
      label: "{{ nms_role.metadata.name }}"
      loop_var: nms_role

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

  - name: Create System tags list
    set_fact:
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

  - name: Tag Systems
    include_role:
      name: nginxinc.nginx_management_suite.nms_system_tags
    loop: "{{ nms_systems }}"
    loop_control:
      label: "{{ nms_system.hostname }}"
      loop_var: nms_system

  - name: Setup Instance Group with NMS
    include_role:
      name: nginxinc.nginx_management_suite.nms_instance_group
    vars:
      nms_instance_group:
        name: production
        description: Production Instances
        displayName: AzureProd

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
