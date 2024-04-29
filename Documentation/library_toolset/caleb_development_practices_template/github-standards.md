## Overview
The following outlines the standards and practices for git and github. The goal is to have a codebase that is maintainable and that starts with good git hygiene. Chris Beam's legendary 2014 post on [writing a good commit message](https://chris.beams.io/posts/git-commit/) said it best:  

 > Reviewing others’ commits and pull requests becomes something worth doing, and suddenly can be done independently. Understanding why something happened months or years ago becomes not only possible but efficient.

> A project’s long-term success rests (among other things) on its maintainability, and a maintainer has few tools more powerful than his project’s log. It’s worth taking the time to learn how to care for one properly. What may be a hassle at first soon becomes habit, and eventually a source of pride and productivity for all involved.

## Repo Naming
When creating a new repo:

 - Use snake case, for example, `aw_connect_backend` vs `AWConnect-Backend`
 - Don't use XYZ_Company in the name, that's already implied by the organization name
 - All repos **MUST** be private
 - Make the title as generic as possible without making it inscrutable
   - `cdog_core` is generic yet project specific, where as `core_libraries` is not
   - `broker_web_app` doesn't provide any specifics what so ever
 - Use the repo description field to describe the repo, a few examples:
   - `A template repo for a node.js serverless project`
   - `Frontend SPA for AW Connect`
 - Use the standard [README template](readme-template.md)

## Github Approach
 - All development must occur in feature branches
 - All code must be written test first
 - 2% drop in code coverage breaks the build
 - Run linters and test suite as pre-commit git hook where applicable
 - PRs are merged as using the squash merge strategy
 - `main` is locked down from direct pushes

## Branch Naming
A well-formed PR should start with a well-named feature branch. This can typically match the title of the story you are working on or a short title to explain the change. Use the following naming convention which starts with your initials:

```
<initials>-<feature>-<name>-<with>-<dashes>
```

For example `tq-earned-premium` or `jd-new-useremail-notifications`.

## Pull Requests
Developers are typically bad at documentation. As much as we'd like to write code that reveals its intention, things don't always work out that way. Pull requests are a stage-gate for code review. They are also an opportunity to communicate and document *why* the change was made.

This practice is essential to communicate with our current team members, but also those who join the project in a year (not to mention our future-selves who won't remember decisions made today).

Bearing this in mind, we use the following criteria to have a Pull Request reviewed and merged:

### The Branch

 - Must be merge-able
 - Must pass CI and CodeClimate
 - Created off of `main`, not another branch
 - Commit messages should use [sentence case](https://apastyle.apa.org/style-grammar-guidelines/capitalization/sentence-case) but no periods
 - Commit messages should be 70-75 characters or less
 - Commit messages should be written in present imperative tense
   - Imperative tense just means “spoken or written as if giving a command or instruction”
   - `Fix dashboard typo` vs `Fixed dashboard typo` or `Fixes dashboard typo`

### The Pull Request

 - The title should describe the change in a few words
 - The title should be in [title case](https://en.wikipedia.org/wiki/Letter_case#Title_case) with no periods
 - The title should *not* match the Jira issue/ticket name
 - The title should *not* match the first commit message
 - The description should use proper capitalization and punctuation
 - The description should describe the business reason for the change, written in a way a new team member or business sponsor could understand it
 - The description should *not* be blank

Example PRs:

 - https://gitlab.com/
