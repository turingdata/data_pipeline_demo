_This page assumes you are familiar with [git](http://git-scm.com/) and github.com. If you need to get up to speed, see [Brad Frost's list of git resources](https://bradfrost.com/blog/post/gitgithub-resources/)._

## Overview

[Martin Fowler](http://martinfowler.com/)'s take on [feature branching](http://martinfowler.com/bliki/FeatureBranch.html):

> The basic idea of a feature branch is that when you start work on a feature (or UserStory if you prefer that term) you take a branch of the repository to work on that feature.

> The advantage of feature branching is that each developer can work on their own feature and be isolated from changes going on elsewhere. They can pull in changes from the mainline at their own pace, ensuring they don't break the flow of their feature

Our feature branching process will consist of the following:

* Anything in the `main` branch is **deployable**.
* To work on something new, create a branch off of `main`.
* Feature branches should not be long-lived, they should equate to 1-2 days worth of work.
* Commit to your branch locally and regularly push your work to GitHub using the same named branch.
* When your work is done, open a pull request.
* Your branch will undergo both an automated and manual code review.
* Once the code passes review, it will be merged into `main`, making it ready for deployment.

**IMPORTANT**: Every developer must push feature branches back to GitHub everyday, regardless if the work is completed or not. This not only provides a backup of your work, but it gives the team a view into which features are currently being worked on.

## Step-by-Step Feature Branching

### Step 1: Creating Your Feature Branch
When implementing a feature or a fix, a branch is created in the forked repository using the following naming convention:

``` bash
<initials>-<feature>-<name>-<with>-<dashes>
```

For example: ` jd-repo-cleanup ` or ` tq-earned-premium `. You can create the branch with the following command:

``` bash
git branch jd-repo-cleanup
```

### Step 2: Checkout Your Feature Branch
Checkout your new feature branch and start working:

``` bash
git checkout jd-repo-cleanup
```

You can view your branches with ` git branch `:

``` bash
git branch
* jd-repo-cleanup
  main
```

#### Shortcut for Branch Creation & Checkout
You can optionally _create_ and _checkout_ the branch _jd-repo-cleanup_ with just one command, rather than using the two above:

``` bash
git checkout -b jd-repo-cleanup
```

### Step 3: Implement Your Feature
Start implementing your feature, committing all of your changes to your branch. Once your branch is checked out, you will follow the standard ` git add ... ` ` git commit ` process you would normally use.

### Step 4: Push Your Feature Branch to GitHub
You should push your feature branch back to GitHub at least once a day (if not more). You can do this with:

``` bash
git push origin <branch_name>
```

For our example, we would type:

``` bash
git push origin jd-repo-cleanup
```

### Step 5: Create a Pull Request
When your branch is ready to undergo a code review, make a pull request from the source project's repo. Do this by navigating to the project's GitHub page, and click on _Pull Requests_ in the primary navigation:

![Pull Request](https://XYZ_Company-developer-practices.s3.amazonaws.com/images/pull-request-nav.png)

Enter a _title_ and a _succinct description_ of your changes, and click the "Create pull request" button:

![Submit your pull request.](https://s3.amazonaws.com/rejuvenan-wiki/images/create-pull-request.png)

Your Pull Request should adhere to our [git standards](github-standards.md). Once submitted, your Pull Request will be used to review the code and document any issues with the code quality or implementation.

__Important__: If the code review requires you to make changes, it is your responsibility to make the changes and notify the group that your PR is ready for review again.

Once your code passes the review, it will be merged into `main` , which closes the Pull Request. Your branch _will then be deleted_ on the server.

If you need feedback or help before your PR is ready, add `WIP` (for *work in progress*) anywhere in the PR title. This will block the PR from being merged:



### Step 6: Clean Up
Once your code is merged into `main`, your feature branch will be deleted on the server, you should do the same to your local environment.

First checkout the main branch:

``` bash
git checkout main
```

Delete your feature branch:

``` bash
git branch -D <branch_name>
```

In our example, we would type:

``` bash
git branch -D jd-repo-cleanup
```

Pull down new changes from the Github `main` branch (this will include your merged branch and possibly other work from teammates):

``` bash
git pull
```

You are now ready to start the process over again. For more details, see GitHub's [Using Pull Requests](https://help.GitHub.com/articles/using-pull-requests) page.
