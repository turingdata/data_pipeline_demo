## Overview
AWS allows us to assign metadata resources in the form of tags, a simple label consisting of a key and an optional value. Tags make it easier to manage, search for, and filter resources.

To understand why tags are essential, read https://www.datadoghq.com/blog/tagging-best-practices/.

**Detail**
For the resources in AWS that support tags, we require the following:

* application (Name - rise, edw, ebao, dragon, aw_connect)
* env (development, staging, production)
* owner (slack channel or group email)
* costcenter (GL Codes) (For example, `A1401` for an IT project)
* role (api, app, pipeline, web, worker)
* provider (aws, azure, nj_dc)
* service (typically a copy of `Name`, may not be relevant for infrastructure)

We can do clever things with `owner` in DataDog, but there is a specific syntax required: https://www.datadoghq.com/blog/tagging-best-practices/#assign-owners-to-services-with-tags.

This shows how DataDog uses `Unified Service Tagging` to tie telemetry together across services: https://docs.datadoghq.com/getting_started/tagging/unified_service_tagging/?tab=kubernetes

This will typically look like this in terraform nested inside of inputs block:

```
tags = {
    application = "name"
    env = "development"
    owner = "proj-name"
    costcenter = "A1401"
    role = "app"
    provider = "aws"
    service = "name"
  }
```

A recent refactor injects `$var.aws_environment_name` as a global variable, so this no longer needs to be set. This is an example of this as well as other defaults being set at the module level:



_Note:_ The tagging standard has evolved and these PRs :points_up: may not have all of the tags listed above depending on when they were created.
