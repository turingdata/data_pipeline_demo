## TL;DR

 - Take a card with your face from "Next Up", move it to "Work in Progress"
 - Create a [feature branch](feature-branch.md) for your card
 - Write your code test first
 - Submit the branch for a code review as a PR, move card to "Ready for Staging"
 - If the code review requires changes, move back, to "Work in Progress"
 - If the code review passes, the PR can be merged.
 - Once merged, it will be deployed to staging
 - After successful deploy, card is moved to "Ready for Testing"
 - Once QA has tested it, he’ll move it to “Ready for Production"
 - Production deploys will occur on a normal basis (unless downtime is required for the deploy)

## Overview
XYZ_Company's development process is focused on delivering business value as quickly as possible via [continuous delivery](http://martinfowler.com/bliki/ContinuousDelivery.html). This means building software in such a way that it can be released to production at any time. [Martin Fowler](http://martinfowler.com) describes [continuous delivery](http://martinfowler.com/bliki/ContinuousDelivery.html) as:

> - Your software is deployable throughout its lifecycle.
> - Your team prioritizes keeping the software deployable over working on new features.
> - Anybody can get fast, automated feedback on the production readiness of their systems any time somebody makes a change to them.
> - You can perform push-button deployments of any version of the software to any environment on demand.

The key benefits of continuous delivery are:

> - __Reduced Deployment Risk__: since you are deploying smaller changes, there's less that can go wrong, and it's easier to fix should a problem appear.
> - __Believable Progress__: many folks track progress by tracking work done. If "done" means "developers declare it to be done" that's much less believable than if it's deployed into a production (or production-like) environment.
> - __User Feedback__: the biggest risk to any software effort is that you end up building something that isn't useful. The earlier and more frequently you get working software in front of real users, the quicker you get feedback to find out how valuable it really is.

## Development Process
Development follows an iterative, agile approach, in a continuous cycle:

* Plan
* Develop
* Review
* Deploy
* Observe

#### Plan
The team-lead will work with the product owner to manage the Jira backlog and plan sprints. Sprints will either be 1 or 2 weeks depending on what needs to be accomplished and how quickly we need to deliver features to a user.

Stories and issues will be assigned to a specific sprint and developer. Retrospectives and sprint reviews will be held every 2 to 3 weeks depending on sprint duration.

Standups occur every day over Microsoft Teams. If you are committing code, you must be on the standup. The meetings are kept to 15 minutes and each team member quickly answers the following 3 questions:

 1) What did you do yesterday?
 2) What are you doing today?
 3) Blockers?

Once the sprint starts, we move to __Develop__.

#### Develop
This phase lives entirely on a developer's local machine and includes testing. The developer starts with the highest priority story/issue and creates a [feature branch](feature-branch.md) for it. All development is [test-driven](#), following the standard red-green-refactor workflow:

![red-green-refactor](http://blog.andolasoft.com/wp-content/uploads/2015/05/TDD-vs-BDD.jpg)

Once the code satisfies all tests, the developer can run a set of tools locally to identify any code-quality issues that could cause an issue during the code review.

The developer then submits a [pull request](github-standards.md), which brings us to the __Review__ phase.

#### Review
The review process is throughly documented in code review. Once the review is completed and the [feature branch](feature-branch.md) is closed, we move to the __Deploy__ phase.

#### Deploy
All deployments happen from the `main` branch and code is uploaded directly from [github](https://github.com).

Deployment methods will vary based on technology, but should be done through a pipeline with no human intervention.

#### Observe
Notification of deployments will be sent to the application's  channel and to [datadog](http://www.datadoghq.com) events console. We can then monitor any deviations in performance and be notified if a larger number of exceptions or errors occur.

If you aren't observing that your code is in production and reading logs, how do you know the code deployed and is actually working?
