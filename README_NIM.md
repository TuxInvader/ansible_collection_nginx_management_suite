# NGINX Management Suite - Instance Manager (NIM)

Documentation for NGINX Instance Manager roles.

## Roles

These are the roles for the NIM module. We can manage TLS certificates, upload/download staged configurations, and publish configurations (either staged or direct) to instances and instance groups.

* [nms_nim_certificate](#nim-certificate-management)
* [nms_nim_config_template](#nim-manage-staged-configurations)
* [nms_nim_get_config_template](#nim-manage-staged-configurations)
* [nms_nim_get_config_template_refs](#nim-manage-staged-configurations)
* [nms_nim_publish_config](#nms-nim-publish-config)

## NIM Certificate Management

> Role: nms_nim_certificate

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

## NIM Manage Staged Configurations

We have three roles for upserting, retrieving, and listing staged configurations. The roles treat the configuration name (`configName`) as a unique key, and so will not create a configuration with a duplicate name. However, NIM does not see the name as a unique key and so duplicates could exist if other tools/users also configure NIM.

If you want to create a configuration with a duplicate name (`configName`) then set the variable `nms_nim_create_new_config` to `true`. This configures the role to create a new config, even when one with the same name already exists.

If you want to suppress warnings about duplicate configNames then set `nms_nim_config_template_duplicate_warn` to `false`.

Once a configuration has been uploaded for the first time, you should record and store the generated UID within the configuration (returned in `nms_nim_config_template_uid`). The role will use the `uid` in preference to the `configName` if it is provided. 

> **NOTE**: You cannot provide a `uid` on creation of a role. NIM will generate one for you, which you can then use on subsequent upserts.

### Upsert Staged Config
> Role: nms_nim_config_template

Upserting configuration files to NIM requires them to be base64 encoded. The role can encode the files for you, if you set the optional role variable `nms_nim_encode_config_content` to `true`.

Upsert a configuration template (Staged Configuration) called base-config. The file contents are provided in plain text, so `nms_nim_encode_config_content` is enabled.

```yaml
  - name: Create NIM Config Template
    include_role:
      name: nginxinc.nginx_management_suite.nms_nim_config_template
    vars:

      nms_nim_encode_config_content: true
      nms_nim_config_template_duplicate_warn: false

      nms_nim_config_template:
        uid: <uid>
        configName: base-config
        auxFiles:
          rootDir: /
          files: []
        configFiles:
          rootDir: /etc/nginx
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
                ...
            - name: /etc/nginx/conf.d/default.conf
              ...
```

### Get Staged Config
> Role: nms_nim_get_config_template

This role can be used to download the contents of a Staged Configuration. You must supply exactly one of `nms_nim_config_template_name` or `nms_nim_config_template_uid`. If you supply a name then the role will get the list of staged configs from the server and download that configuration. It is best to use the uid (as returned from nms_nim_get_config_template_refs) if there is any possibility of duplicate names.

```yaml
  tasks:

  - name: Setup Authentication with NMS
    include_role:
      name: nginxinc.nginx_management_suite.nms_authenticate

  - name: Get our NIM Config Template
    include_role:
      name: nginxinc.nginx_management_suite.nms_nim_get_config_template
    vars:
      nms_nim_config_template_name: base-config
      #nms_nim_config_template_uid: <uid>
      nms_nim_decode_config_content: true

  - name: Display the config as returned by API
    debug:
      msg: "{{ nms_nim_encoded_config }}"

  - name: Display the Config decoded
    debug:
      msg: "{{ nms_nim_decoded_config }}"
```

The role returns the configuration with file contents base64 encoded in `nms_nim_encoded_config`. 

If you would like a decoded copy, then set `nms_nim_decode_config_content` to `true`. The role with then also return `nms_nim_decoded_config`.

### Get Staged Config list
> Role: nms_nim_get_config_template_refs

Retrieve a list of staged configs. This returns the list of staged configurations in a dictionary keyed by both name and uid.

```yaml
  tasks:

  - name: Setup Authentication with NMS
    include_role:
      name: nginxinc.nginx_management_suite.nms_authenticate

  - name: Get list of staged configs
    include_role:
      name: nginxinc.nginx_management_suite.nms_nim_get_config_template_refs

  - name: Display the list
    debug:
      msg: "{{ nms_nim_config_template_refs }}"
```

 The dictionary will contain the following keys: `configName`, `createTime`, `rel`, `uid`, `updateTime`, and also instance/group information if the configuration is deployed anywhere.

## NMS NIM Publish Config

