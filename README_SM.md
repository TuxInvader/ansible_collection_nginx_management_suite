# NGINX Management Suite - Security Module (SM)

Documentation for the Security Module.

## Roles

* [nms_sm_policy](#nms-sm-policy)
* [nms_sm_get_policy_refs](#nms-sm-get-policy-refs)
* [nms_sm_get_logprofiles](#nms-sm-get-log-profiles)
* [nms_sm_signature](#nms-sm-signature-upload)
* [nms_sm_publish](#nms-sm-publish)

## NMS Security Module

The NMS-SM module can be used to configure and monitor security events from NGINX Plus / NGINX App Protect.

NMS-SM ships with two policies by default: `NginxDefaultPolicy` and `NginxStrictPolicy`. You can see the list of available policies by running the [nms_sm_get_policy_refs](#nms-sm-get-policy-refs) role. You can upload or updated existing policies by using the [nms_sm_policy](#nms-sm-policy) role.

NSM-SM also ships with a number of log-profiles: `log_all`, `log_blocked`, `log_illegal`, and `secops_dashboard`. You can download the list of available profiles by running the [nms_sm_get_logprofiles](#nms-sm-get-log-profiles) role.

## Deploying a NAP Policy

> **Agent Configuration:**
The NMS-SM module requires that the NGINX Agent be deployed with several additional options for collecting NAP metrics, and also to provide
a syslog service for the `app_protect_security_log`. Please ensure that you have set the appropriate settings in the agent configuration,
either manually or bu using the [nms_agent_config](roles/nms_agent_config/README.md) role and setting `nms_agent_nap_enable` and `nms_agent_nap_syslog_port`.

To deploy a NAP policy, you simply need to deploy a configuration which references one of the available policies and log_profiles.
Eg:

```yaml
 - name: Create NIM Config Template
    include_role:
      name: nginxinc.nginx_management_suite.nms_nim_publish_config
    vars:
      nms_nim_publish_encode_content: true
      nms_nim_publish_ignore_conflict: true
      nms_nim_publish_validate_config: false
      nms_nim_publish:
        config:
          auxFiles: 
            files: []
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
                    default_type  application/octet-stream;
    
                    log_format  main  '$remote_addr - $remote_user [$time_local] "$request" '
                                      '$status $body_bytes_sent "$http_referer" '
                                      '"$http_user_agent" "$http_x_forwarded_for"';

                    access_log  /var/log/nginx/access.log  main;
                    sendfile        on;
                    keepalive_timeout  65;

                    include /etc/nginx/conf.d/*.conf;
                }
            - name: /etc/nginx/conf.d/default.conf
              contents: |
                server {
                  listen       80 default_server;
                  server_name  localhost;

                  app_protect_enable on;
                  app_protect_policy_file "/etc/app_protect/conf/NginxStrictPolicy.tgz";
                  app_protect_security_log_enable on;
                  app_protect_security_log "/etc/app_protect/conf/secops_dashboard.tgz" syslog:server=127.0.0.1:5514;

                  access_log  /var/log/nginx/host.access.log  main;

                  location / {
                    proxy_pass http://127.0.0.1:8081;

                  }
            rootDir: /etc/nginx

```

The above is a directly configured NGINX deployment, but you can also use `Staged Configuration`.

The Policies and Log Profiles are precompiled by NMS, and so you should reference them by name and with a `tgz` extension.
Also make sure that your syslog port matches the one used in the agent configuration.

Once you have a deployed policy, you might want to deploy Attack Signatures and enable Threat Campaigns. This is achieved by publishing signatures to the
`instance` or `instancegroup` and targetting a specific policy version with the desired AS/TC bundles. Attack Signatures and Threat Campaignes can be uploaded
to NMS using the [nms_sm_signature](#nms-sm-signature-upload) role, and then published with [nms_sm_publish](#nms-sm-publish).


## NMS-SM Get Policy Refs

Get the available policies from NMS. The policy content itself is only retrieved when `nms_sm_policy_include_content` is true, and it is base64 encoded, but you pass `nms_sm_policy_decode_content` if you would it returned to you in clear text.

```yaml
  - name: Get existing NSM-SM Policies
    include_role:
      name: nginxinc.nginx_management_suite.nms_sm_get_policy_refs
    vars:
      nms_sm_policy_include_content: true
      nms_sm_policy_decode_content: true
```

If you include `nms_sm_policy -> metadata -> uid` then the role will return only the matching policy. 

```yaml
  - name: Get existing NSM-SM Policies
    include_role:
      name: nginxinc.nginx_management_suite.nms_sm_get_policy_refs
    vars:
      nms_sm_policy_include_content: true
      nms_sm_policy_decode_content: true
      nms_sm_policy:
        metadata:
          uid: "74d4579f-03c7-4943-98fc-93076b68ce08"
```

## NMS-SM Get Log Profiles

To get the available Log Profiles:

```yaml
  - name: Get existing NSM-SM Log Profiles
    include_role:
      name: nginxinc.nginx_management_suite.nms_sm_get_logprofiles
    vars:
      nms_sm_logprofile_include_content: false
      nms_sm_logprofile_decode_content: false
```

## NMS-SM Policy

To upload your own policy, you can make a request like the one below:

```yaml
  - name: Upsert NSM-SM Policy
    include_role:
      name: nginxinc.nginx_management_suite.nms_sm_policy
    vars:
      nms_sm_policy_state: present
      nms_sm_policy_new_revision: false
      nms_sm_policy:
        metadata:
          name: marks-policy
          displayName: Default Policy
          description: Base policy
        content:
          policy:
            name: app_protect_default_policy
            template:
              name: POLICY_TEMPLATE_NGINX_BASE

```

## NMS-SM Signature Upload

Both Attack Signatures and Threat Campaigns can be uploaded to NMS by extracting the data from a deployed package, and creating a tarball
containing the files from either:

Attack Signatures
  * version
  * signature_update.yaml
  * signatures.bin.tgz
  
Threat Campaigns
  * version
  * threat_campaign_update.yaml
  * threat_campaigns.bin.tgz

### Attack Signatures

```yaml
  - name: Upsert NSM-SM Attack Signature
    include_role:
      name: nginxinc.nginx_management_suite.nms_sm_signature
    vars:
      nms_sm_signature_state: present
      nms_sm_signature_source: local
      nms_sm_signature_type: sig 
      nms_sm_signature:
        filename: /home/mark/Downloads/sigs.tgz
        revisionTimestamp: 2022.11.16

```
### Threat Campaigns

```yaml
  - name: Upsert NSM-SM Threat Campaign
    include_role:
      name: nginxinc.nginx_management_suite.nms_sm_signature
    vars:
      nms_sm_signature_state: present
      nms_sm_signature_source: local
      nms_sm_signature_type: threat
      nms_sm_signature:
        filename: /home/mark/Downloads/tcs.tgz
        revisionTimestamp: 2022.11.15

```

## NMS-SM Publish

Once the signautures are available on NMS, they can be published to the instances/instance group, and linked to a NAP policy.

```yaml
  - name: Publish NSM-SM Policy
    include_role:
      name: nginxinc.nginx_management_suite.nms_sm_publish
    vars:
      nms_sm_publish_instances:
      - nginx1
      - nginx2
      nms_sm_publish:
        attackSignatureLibrary:
          versionDateTime: 2022.11.16
        threatCampaign:
          versionDateTime: 2022.11.15
        policyContent:
          name: NginxStrictPolicy
          uid: 74d4579f-03c7-4943-98fc-93076b68ce08

```
