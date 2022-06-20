NMS Licensing
=============

NGINX Management Suite (NMS) Ansible role for creating NGINX configs


Requirements
------------

* [NGINX Instance Manager](https://www.nginx.com/products/nginx-instance-manager/)

Role Variables
--------------
`nms_fqdn`
`nms_api_version`
`nms_validate_certs`
`nms_nim_config_template`

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

          - name: /etc/nginx/mime.types
            contents: |
                CnR5cGVzIHsKICAgIHRleHQvaHRtbCAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAg
                ICAgICBodG1sIGh0bSBzaHRtbDsKICAgIHRleHQvY3NzICAgICAgICAgICAgICAgICAgICAgICAg
                ICAgICAgICAgICAgICAgICBjc3M7CiAgICB0ZXh0L3htbCAgICAgICAgICAgICAgICAgICAgICAg
                ---SNIP--- ---SNIP--- ---SNIP--- ---SNIP--- ---SNIP--- ---SNIP--- ---SNIP---
                dmlkZW8gICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgYXZpOwp9Cg==

          - name: /etc/nginx/conf.d/default.conf
            contents: |
              c2VydmVyIHsKICAgIGxpc3RlbiAgICAgICA4MCBkZWZhdWx0X3NlcnZlcjsKICAgIHNlcnZlcl9u
              YW1lICBsb2NhbGhvc3Q7CgogICAgI2FjY2Vzc19sb2cgIC92YXIvbG9nL25naW54L2hvc3QuYWNj
              ZXNzLmxvZyAgbWFpbjsKCiAgICBsb2NhdGlvbiAvIHsKICAgICAgICByb290ICAgL3Vzci9zaGFy
              ZS9uZ2lueC9odG1sOwogICAgICAgIGluZGV4ICBpbmRleC5odG1sIGluZGV4Lmh0bTsKICAgIH0K
              CiAgICAjZXJyb3JfcGFnZSAgNDA0ICAgICAgICAgICAgICAvNDA0Lmh0bWw7CgogICAgIyByZWRp
              cmVjdCBzZXJ2ZXIgZXJyb3IgcGFnZXMgdG8gdGhlIHN0YXRpYyBwYWdlIC81MHguaHRtbAogICAg
              IwogICAgZXJyb3JfcGFnZSAgIDUwMCA1MDIgNTAzIDUwNCAgLzUweC5odG1sOwogICAgbG9jYXRp
              b24gPSAvNTB4Lmh0bWwgewogICAgICAgIHJvb3QgICAvdXNyL3NoYXJlL25naW54L2h0bWw7CiAg
              ICB9CgogICAgIyBwcm94eSB0aGUgUEhQIHNjcmlwdHMgdG8gQXBhY2hlIGxpc3RlbmluZyBvbiAx
              MjcuMC4wLjE6ODAKICAgICMKICAgICNsb2NhdGlvbiB+IFwucGhwJCB7CiAgICAjICAgIHByb3h5
              X3Bhc3MgICBodHRwOi8vMTI3LjAuMC4xOwogICAgI30KCiAgICAjIHBhc3MgdGhlIFBIUCBzY3Jp
              cHRzIHRvIEZhc3RDR0kgc2VydmVyIGxpc3RlbmluZyBvbiAxMjcuMC4wLjE6OTAwMAogICAgIwog
              ICAgI2xvY2F0aW9uIH4gXC5waHAkIHsKICAgICMgICAgcm9vdCAgICAgICAgICAgaHRtbDsKICAg
              ICMgICAgZmFzdGNnaV9wYXNzICAgMTI3LjAuMC4xOjkwMDA7CiAgICAjICAgIGZhc3RjZ2lfaW5k
              ZXggIGluZGV4LnBocDsKICAgICMgICAgZmFzdGNnaV9wYXJhbSAgU0NSSVBUX0ZJTEVOQU1FICAv
              c2NyaXB0cyRmYXN0Y2dpX3NjcmlwdF9uYW1lOwogICAgIyAgICBpbmNsdWRlICAgICAgICBmYXN0
              Y2dpX3BhcmFtczsKICAgICN9CgogICAgIyBkZW55IGFjY2VzcyB0byAuaHRhY2Nlc3MgZmlsZXMs
              IGlmIEFwYWNoZSdzIGRvY3VtZW50IHJvb3QKICAgICMgY29uY3VycyB3aXRoIG5naW54J3Mgb25l
              CiAgICAjCiAgICAjbG9jYXRpb24gfiAvXC5odCB7CiAgICAjICAgIGRlbnkgIGFsbDsKICAgICN9
              CgogICAgIyBlbmFibGUgL2FwaS8gbG9jYXRpb24gd2l0aCBhcHByb3ByaWF0ZSBhY2Nlc3MgY29u
              dHJvbCBpbiBvcmRlcgogICAgIyB0byBtYWtlIHVzZSBvZiBOR0lOWCBQbHVzIEFQSQogICAgIwog
              ICAgI2xvY2F0aW9uIC9hcGkvIHsKICAgICMgICAgYXBpIHdyaXRlPW9uOwogICAgIyAgICBhbGxv
              dyAxMjcuMC4wLjE7CiAgICAjICAgIGRlbnkgYWxsOwogICAgI30KCiAgICAjIGVuYWJsZSBOR0lO
              WCBQbHVzIERhc2hib2FyZDsgcmVxdWlyZXMgL2FwaS8gbG9jYXRpb24gdG8gYmUKICAgICMgZW5h
              YmxlZCBhbmQgYXBwcm9wcmlhdGUgYWNjZXNzIGNvbnRyb2wgZm9yIHJlbW90ZSBhY2Nlc3MKICAg
              ICMKICAgICNsb2NhdGlvbiA9IC9kYXNoYm9hcmQuaHRtbCB7CiAgICAjICAgIHJvb3QgL3Vzci9z
              aGFyZS9uZ2lueC9odG1sOwogICAgI30KfQpzZXJ2ZXIgewogIGxpc3RlbiA4MDgwIGRlZmF1bHQ7
              CiAgbG9jYXRpb24gLyB7IHJldHVybiA0MDQ7IH0KICBsb2NhdGlvbiAvYXBpLyB7IGFwaSB3cml0
              ZT1vbjsgYWxsb3cgMTI3LjAuMC4xOyBkZW55IGFsbDsgfQp9Cg==

```

After running the list of current configurations will be available in `nms_nim_config_template_refs`

License
-------

[Apache License, Version 2.0](./LICENSE)

Author Information
------------------

[Mark Boddington](https://github.com/TuxInvader)

&copy; [NGINX, Inc.](https://www.nginx.com/) 2022

