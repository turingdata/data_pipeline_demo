## Overview
As part of our goals to Build a Better IT, we want to make documentation as essential and critical as features. The "why" can seem obvious, but most engineers and IT shops are terrible at actually doing it.

The ACM Queue article [Why Site Reliability Engineering (SRE) Documents Matter](https://queue.acm.org/detail.cfm?id=3283589), said it best:

> In the early stages of an SRE team's existence, the organization depends heavily on the performance of highly skilled individuals on the team. The team preserves important operational concepts and principles as nuggets of "tribal knowledge" that are passed on verbally to new team members. If these concepts and principles are not codified and documented, they will often need to be relearned—painfully—through trial and error. Sometimes team members perform operational procedures as a strict sequence of steps defined by their predecessors in the distant past, without understanding the reasons these steps were initially prescribed. If this is allowed to continue, processes eventually become fragmented and tend to degenerate as the team scales up to handle new challenges.

> SRE teams can prevent this process decay by creating high-quality documentation that lays the foundation for such teams to scale up and take a principled approach to managing new and unfamiliar services. These documents capture tribal knowledge in a form that is easily discoverable, searchable, and maintainable. New team members are trained through a systematic and well-planned induction and education program.

## Documentation Standard
This document serves as our initial rollout of a documentation standard, but far from the final version. 

If you have a suggestion, open a pull request on this repo.

### Format
All documents are written in [Markdown](https://daringfireball.net/projects/markdown/). Markdown is used widely because (to quote the author):

> Markdown allows you to write using an easy-to-read, easy-to-write plain text format, then convert it to structurally valid XHTML (or HTML).

> Thus, “Markdown” is two things: (1) a plain text formatting syntax; and (2) a software tool, written in Perl, that converts the plain text formatting to HTML.

Github will natively render Markdown making it easy to write, edit, display and search. Given its simple [formatting rules](https://guides.github.com/features/mastering-markdown/), it allows us to treat it like code and see the lineage of documentation changes.

If you are new to Markdown, see Github's [Mastering Markdown](https://guides.github.com/features/mastering-markdown/).

### Location
All documents will be stored in GitHub alongside the source code they support. All document changes will occur in pull requests; this is by design. It has the following outcomes:

 - We treat documentation with the same rigor and weight as we source code
 - Documentation will require code review, which will require others the team to read it and suggest corrections/additions

### Documents
Every repo in GitHub should contain the following documents in the root folder of the project:

 - `README.md` - Everything a new team member needs to know to be productive for a given application/system
 - `ARCHITECURE.md` - Describes the components, servers, and data flows for a given application/system
 - `SUPPORT.md` - A [runbook](https://www.blameless.com/blog/runbook-automation-best-practices) that initially be focused on L1 support

By default, GitHub will render a project's `README.md` on the root page of the repo just below the code listing.

If your application or system has documents static documents and would not be changed (user guides, vendor documentation), store these on the Confluence page for the given application or system.

There is no value in storing artifacts that we won't change in GitHub, but they should still be discoverable and centrally stored. Add a link from your `README.md` to these additional documents in Confluence.

#### README
A well-crafted README should spell out everything a new team member needs to know to from zero to productive. For example it should highlight:

 - How to contribute changes
 - Tech stack details
 - Development environment setup
 - Tooling instruction

When starting a new GitHub repo, copy the XYZ_Company [README Template](readme-template.md) to your project and make the appropriate changes to the template.

 The following are idiomatic examples of project `README.md` files:

  - [DMS API](https://github.com/XYZ_Company/dms_cloud_backend/blob/master/README.md)
  - [AWS Connect Backend](https://github.com/XYZ_Company/aws_connect_backend)
  - [Rulebook Data Lake](https://github.com/XYZ_Company/rulebook_data_platform/README.md)

#### ARCHITECURE
Architecture diagrams are critical for a shared understanding of complicated, distributed systems.

Examples of architecture diagrams:

 - [Data Lake Architecture](https://github.com/XYZ_Company/datalake/main/ARCHITECTURE.md)
 - [Data Lake Architecture](https://github.com/XYZ_Company/rulebook_demo_data_platform/data-pipeline/ARCHITECTURE.md)
 
#### SUPPORT
To enable AMS break/fix teams to support all of our systems, we must document operating what we've built. We'll accomplish L1 support by providing runbooks for every GitHub repo.

Runbooks provide adequately skilled team members unfamiliar with procedures or the workload, the instructions necessary to complete an activity. Capturing this information preserves the institutional knowledge of your organization. It eases the burden on key personnel by sharing their knowledge and enabling more team members to achieve the same outcomes.

When starting a new GitHub repo, copy the XYZ_Company [SUPPORT Template](support-template.md) to your project and make the appropriate changes to the template.
