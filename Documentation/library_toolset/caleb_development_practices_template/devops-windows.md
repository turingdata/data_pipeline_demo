### Install Git

Go to https://git-scm.com/downloads and download the windows version.
You can click next on most of the default settings but make sure to select the following:

![git_bash_default_branch_name](./assets/git_bash_default_branch_name.png)

![git_bash_symlink](./assets/git_bash_symlink.png)

### Configure Git

**Note:** For this next step you will need to open Git Bash application as an administrator.

![git_bash_admin](./assets/git_bash_admin.png)

Next we want to configure git to handle long paths.

```
$ git config --system core.longpaths true
```

### Configure SSH Keys

First generate a SSH Key and make sure you add a passphrase.

```
$ ssh-keygen -t rsa -b 4096 -C "your_email@example.com"
```

Configure ssh-agent to auto launch by copying the following lines into `~/.bash_profile`.

```
env=~/.ssh/agent.env

agent_load_env () { test -f "$env" && . "$env" >| /dev/null ; }

agent_start () {
    (umask 077; ssh-agent >| "$env")
    . "$env" >| /dev/null ; }

agent_load_env

# agent_run_state: 0=agent running w/ key; 1=agent w/o key; 2= agent not running
agent_run_state=$(ssh-add -l >| /dev/null 2>&1; echo $?)

if [ ! "$SSH_AUTH_SOCK" ] || [ $agent_run_state = 2 ]; then
    agent_start
    ssh-add
elif [ "$SSH_AUTH_SOCK" ] && [ $agent_run_state = 1 ]; then
    ssh-add
fi

unset env
```

To test that ssh-agent is working close and reopen git-bash.
It should prompt you for your passphares and running the following command will show that your ssh key is loaded.

```
$ ssh-add -l

4096 SHA256:... your_email@example.com (RSA)
```

### Add Your Public SSH Key to Github

Go to "SSH and GPG Keys" (https://github.com/settings/keys) inside of Github account settings.
Click on "New SSH Key", provide a title and paste in the output of `cat ~/.ssh/id_rsa.pub` into the key text area.

Test your connection to Github by running:

```
$ ssh -T git@github.com

Hi ...! You've successfully authenticated, but GitHub does not provide shell access.
```

### Install AWS CLI
Download the latest version of the AWS CLI installer here https://awscli.amazonaws.com/AWSCLIV2.msi.

### Install Terraform

- In git-bash create a directory to hold the executable files `mkdir ~/bin`.
- As of this writing version 0.12.9 is used in the majority of the project so download that version (terraform_0.12.9_windows_amd64.zip) from the releases page https://releases.hashicorp.com/terraform/
- Unzip and copy the executable into `~/bin` but make sure its called `terraform.exe`.

### Install Terragrunt
- Go to the releases page https://github.com/gruntwork-io/terragrunt/releases and download the latest version.
- Copy `terragrunt_windows_amd64.exe` into `~/bin` and make sure its called `terragrunt.exe`.

### Running Terragrunt Plan

- Git clone infrastructure_live repo
- Log into aw.okta.com and click on the AWS icon.
- Select your AWS Account and click on "Command line or programmatic acces".
- From the macOS and Linux tab copy the environment variables under "Option 1".
- Paste credentials and verify access by running `aws s3 ls`.
- Navigate to a module e.g. `dev/us-east-1/dev/utility-server` and run `terragrunt.exe plan`.
- Ignore the message "failed to get console mode..." and wait a bit and it will start printing the plan.

### Open Issues

Our repo has different versions of terraform that get automatically selected on macOS/Linux, thanks to `tfenv` and `tgenv`.
We currently don't have this feature on Windows and have to manually manage this by copying different version of `terraform.exe` into `~/bin`.
