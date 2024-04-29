
# Project Title
Short, 1 sentence description of project.

_Status badges here (if available for your project)_

# Getting Started

This is a sample outline of a README.md file, you _should_ edit it and make changes as you see fit.  The information here can be used as a guideline to help you.

## Contributing
Please observe the following rules when contributing to this project:

1. All code in the `main` branch is deployable, deploys are from `main`
2. All development must occur in feature branches
3. All code must be written test first using _your testing tool_
4. The following tools will be run as pre-commit git hook:
 - _add tools such as linters_
 - _add tools such as code quality_
5. PRs are merged as using the `squash` merge strategy

### Acceptance Criteria
In effort to have this repository serve as documentation for our future selves and future team members, the following criteria must be met in order to have a Pull Request reviewed and merged:

 - The branch must be merge-able
 - The branch must pass CI
 - The branch was created off of `main`, not another branch
 - The branch's commit messages should be written imperatively describing the change in 70-75 characters or less
 - The pull request title should describe the change in a few words
 - The pull request description should describe the business reason for the change, written in a way a new team member or business sponsor could understand it. While you can use bullet points, there should be a summary before this.
 - The pull request should use proper capitalization and punctation

# Technology Stack

Please update the sample list below to indicate the technologies that are used within this project.

1. [TypeScript](https://www.typescriptlang.org/)
2. [JavaScript](https://www.javascript.com/)
3. [NodeJS](https://nodejs.org/)
4. [npm](https://www.npmjs.com/)

# Setup Instructions

This section should outlines what is required to setup this project within a new environment.

## Local Development

Here, you should provide some brief instructions about setting up the tooling (packages, testing frameworks, etc.) that is required to build and deploy this project.  For example:

Homebrew is a package manager for OSX. To install it, run the following from the command line:

```
ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
```

### Ruby
You can install and manage your rubies using any tool you want. The following describes how to manage it with [rbenv](https://github.com/rbenv/rbenv).

First install [rbenv](https://github.com/rbenv/rbenv) with the following:

```
brew install rbenv
```

Setup [rbenv](https://github.com/rbenv/rbenv) in your shell:

```
rbenv init
```

Make sure you have the following where ever you setup your path (`.bashrc` or `.bash_profile`):

```
export PATH=~/.rbenv/shims:$PATH
```

Close your Terminal window and open a new one so your changes take effect. Now install ruby 2.6.2 with the following:

```
rbenv install ruby-2.6.2
```

## Development Tools

## Environment Setup
Run the setup script to install dependencies and setup the database (you only have to do this once):

```
bin/setup
```

### Local Server
To start the rails server, run:

```
bin/rails server
```

Access this project in a web browser at [http://localhost:3000](http://localhost:3000).

### Tests
In this section please provide brief instruction for running tests. For example:

To run Jest tests via yarn, execute:

```
yarn test
```

This will start a test loop that is trigger anytime a change is saved.

# Deployment
In this section please provide brief instruction for running/deploying this project as well as how to run any tests that are in the project.  For example:


## Deploy
Deployments can be executed via yarn as well:

```
yarn deploy
```

# Project Structure
In this section you should outline what the structure of your project is like and highlight any specific files that need special attention.  For example:

## Models
Data Models representing data transferred in and out of the API.

### models/user.ts
Model representing users, used as the base for all role specific uses.

## models/product.ts
Model representing products.

## Controllers

### controllers/homeController.ts
Default index controller that handles routing user actions to the appropriate handlers.

# Misc Information
In this section you should include anything that would help a new developer come up to speed. For example:

## Signing In
### Employee (`app/models/employee.rb`)
Employee access is controlled by Okta and you would use your network/AD credentials to log in. This Rails development environment will properly authenticate with Okta as long as you set the key and secret in your `.env.development` file.

### Policy Holder (`app/models/user.rb`)
When you run `bin/setup`, this will load all the records in `db/seeds.rb` including the following policy:

- Policy Number: `123456`
- Effective: `Nov 1st of the current year`
- Expiry: `Nov 1st of next year`

Use can use these values to create an account as a policy holder
