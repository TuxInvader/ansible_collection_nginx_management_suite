# Ansible Collection - NGINX Management Suite - ACM Module

Documentation for the using ACM with this collection.

## Roles

* [nms_acm_workspace](#nms-acm-workspace)
* [nms_acm_environment](#nms-acm-environment)
* [nms_acm_apidoc](#nms-acm-apidoc)
* [nms_acm_proxies](#nms-acm-proxies)
* [nms_acm_policy_factory](#nms-acm-policy-factory)

### NMS ACM Workspace

Create an Infrastructure or Service workspace.

```yaml
  - name: Create Dev workspace
    include_role:
      name: nginxinc.nginx_management_suite.nms_acm_workspace
    vars:
      nms_acm_workspace:
        name: partners
        contactDetails:
          adminEmail: admin@nginx.com
          adminName: Albert the Admin
        metadata:
          description: Partner API workspace
          slackHandle: ""
```

By default the role creates an infra workspace,
to create a services workspace, provide the variable `nms_acm_team: services`

```yaml
  - name: Create F1 workspace
    include_role:
      name: nginxinc.nginx_management_suite.nms_acm_workspace
    vars:
      nms_acm_team: services
      nms_acm_workspace:
        name: formula1
        contactDetails:
          adminEmail: api-dev@nginx.com
          adminName: Alfred the API Developer
        metadata:
          description: Formula 1 APIs
          slackHandle: ""
```


### NMS ACM Environment

```yaml
  - name: Create Partner Dev environment
    include_role:
      name: nginxinc.nginx_management_suite.nms_acm_environment
    vars:
      nms_acm_workspace:
        name: partners
      nms_acm_environment:
        name: dev
        type: NON-PROD
        metadata:
          description: Partner Dev
        functions:
        - DEVPORTAL
        - API-GATEWAY
        proxies:
        - runtime: GATEWAY-PROXY
          proxyClusterName: partner-dev-cluster
          hostnames:
          - devapi.foo.com
        - runtime: PORTAL-PROXY
          proxyClusterName: partner-dev-portal
          hostnames:
          - devportal.foo.com
```

### NMS ACM APIDoc

```yaml
  - name: Upload F1 API OAS Spec
    include_role:
      name: nginxinc.nginx_management_suite.nms_acm_apidoc
    vars:
      nms_acm_workspace:
        name: formula1
      nms_acm_apidoc:
        name: f1-results-api-1
        spec: "{{ lookup('file', 'specs/ergast.yaml') | from_yaml }}"
```

### NMS ACM Proxies

The below example includes the `proxyConfig -> Policies` directly, but there is also
a helper function to build policies using defaults, see [nms_acm_policy_factory](#nms-acm-policy-factory)
```yaml
  - name: Create F1 API Proxies
    include_role:
      name: nginxinc.nginx_management_suite.nms_acm_proxies
    vars:
      nms_acm_workspace:
        name: formula1
      nms_acm_proxies:
        name: f1-api
        version: v1.0
        specRef: f1-results-api-1
        portalConfig:
          targetProxyHost: devapi.foo.com
          hostname: devportal.foo.com
          category: ""
        proxyConfig:
          policies:
            proxy-request-headers:
            - action:
                proxyHeaders:
                  proxyCustomHeadersToBackend:
                  - key: x-foo
                    value: header.x_foo
                  proxyDefaultHeadersToBackend: true
              metadata:
                appliedOn: backend
                labels:
                - default
          hostname: devapi.foo.com
          backends:
          - serviceName: f1-svc
            serviceTargets:
            - hostname: f1api.internal.foo.com
          ingress:
            basePath: /api/f1
```

### NMS ACM Policy Factory

The factory builds a fact called `nms_acm_policy_bundle`, which can then be provided to
the `nms_acm_proxies` role when publishing an API. It tries to set the same defaults as
the ACM UI.

```yaml
  - name: Create proxy policies
    include_role:
      name: nginxinc.nginx_management_suite.nms_acm_policy_factory
    vars:
      nms_acm_policies:
        new: True
        policies:
        - type: proxy-request-headers
          params:
            proxy_custom_headers:
            - key: x-foo
              value: header.x_foo
        - type: apikey-authn
          params:
            no_match_return_code: 404
            api_key_name: x-api-key
            api_keys:
            - clientID: devkey
              apiKey: foobarbaz
        - type: cors
```

Example use of the bundle 
```yaml
  - name: Create F1 API Proxies
    include_role:
      name: nginxinc.nginx_management_suite.nms_acm_proxies
    vars:
      nms_acm_workspace:
        name: formula1
      nms_acm_proxies:
        name: f1-api
        version: v1.0
        specRef: f1-results-api-1
        portalConfig:
          targetProxyHost: devapi.foo.com
          hostname: devportal.foo.com
          category: ""
        proxyConfig:
          policies: "{{ nms_acm_policy_bundle }}"
          hostname: devapi.foo.com
          backends:
          - serviceName: f1-svc
            serviceTargets:
            - hostname: f1api.internal.foo.com
          ingress:
            basePath: /api/f1
```



