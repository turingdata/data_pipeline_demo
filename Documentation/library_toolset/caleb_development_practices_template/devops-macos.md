### Requirements

Install Command Line Tools

```bash
xcode-select --install
```


Install Homebrew (https://brew.sh)

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install.sh)"
```

Install other dependencies

```bash
brew install awscli jq tfenv packer
```

### Setting up tfenv and tgenv

`tfenv` should already be installed from the homebrew steps above.
For `tgenv` we have to install it manually:

```bash
$ git clone https://github.com/cunymatthieu/tgenv.git ~/.tgenv

# If using Zsh shell replace .bash_profile with .zshrc
$ echo 'export PATH="$HOME/.tgenv/bin:$PATH"' >> ~/.bash_profile
```

Next we will install terragrunt and terraform

```bash
# Note starting with 0.25.0 terragrunt will be tested against terraform 0.13.x we will use the previous version until we are ready to upgrade.
tgenv install 0.24.4

tfenv install 0.12.9
tfenv install 0.12.29
```

### Auto Switching Between Versions

To use the auto switch feature we just have to add `.terraform-version` and `.terragrunt-version` files to the root of a folder, see this blog post for more [details](https://blog.gruntwork.io/how-to-manage-multiple-versions-of-terragrunt-and-terraform-as-a-team-in-your-iac-project-da5b59209f2d).

### AWS Authentication

We are following the Gruntwork recommended setup in this [guide](https://gruntwork.io/guides/foundations/how-to-configure-production-grade-aws-account-structure/#iam-roles).

![aws_login_flow](./assets/aws_login_flow.png)


### Shell setup with plaintext environment variables (less secure)

Copy [mfa.sh](./bin/macos/mfa.sh) to your home directory and make sure its executable `chmod +x mfa.sh` add the alias to your `.bash_profile` or `.zshrc` file.

```bash
# Make sure that this path matches your mfa.sh location
alias aw-mfa="/Users/$USER/mfa.sh"
```

Add the following to the end of `.bash_profile` or `.zshrc` file.

```bash
AWS_ACCESS_KEY_ID=[your-access-key]
AWS_SECRET_ACCESS_KEY=[your-secret-key]
AWS_MFA_SERIAL_NUMBER=arn:aws:iam::[account_id]:mfa/[username]
```


Apply shell changes by running `exec $SHELL` and when you use the alias `aw-mfa`, you should see the following output when it's successful. After you're done running terragrunt or any other command under the assumed role, typing exit will take you back to your regular shell.

![mfa_login](./assets/mfa_login.png)

### AWS Single-Sign-On(SSO) Authentication

Use below instructions to setup AWS CLI with SSO authentication.

Prerequisites:

- AWS CLI Installed
- Access to AWS account

Terminal(zsh) configuration: 
```bash
# Login to SSO site 
aws configure sso
SSO start URL [None]: https://XYZ_Company.awsapps.com/start         # This is the site which will authenticate your credentials
SSO Region [None]: us-east-1                                        # Choose default region to use
Attempting to automatically open the SSO authorization page in your default browser.
If the browser does not open or you wish to use a different device to authorize this request, open the following URL:

https://device.sso.us-east-1.amazonaws.com/

Then enter the code:

JZVK-QPMK
The only AWS account available to you is: 012345123
Using the account ID 012345123
The only role available to you is: PowerUserAccess
Using the role name "PowerUserAccess"                                # At this point you should be signed in.
CLI default client Region [None]: us-east-1                          # Setup region
CLI default output format [None]: json                               # Setup output format. 
CLI profile name [PowerUserAccess-012345123]: dev-profile         # Name this profile. This is helpful if using multiple accounts

To use this profile, specify the profile name using --profile, as shown:

aws s3 ls --profile dev-profile
```

Above will create a custom profile named "dev-profile". If this was the first time configuring aws cli, then most likely there is no default profile created and everytime awscli will ask for default setting.

Making the above as default profile-

Terminal(zsh) configuration:
```bash
# Edit aws cli configuration file
vi ~/.aws/config

# Sample content from above configuration
# [profile dev-profile]
# sso_start_url = https://XYZ_Company.awsapps.com/start
# sso_region = us-east-1
# sso_account_id = 012345123
# sso_role_name = PowerUserAccess
# region = us-east-1
# output = json

# Copy/Update the above lines and set it as default. Sample: 
# [default]
# sso_start_url = https://XYZ_Company.awsapps.com/start
# sso_region = us-east-1
# sso_account_id = 012345123
# sso_role_name = PowerUserAccess
# region = us-east-1
# output = json

# You can keep the initial profile and also the default configurations.
```

Test Configuration:
- To test if everything is setup correctly, run some test aws cli commands:

Example:
```bash
aws sts get-caller-identity
```
For Terragrunt/terraform it doesn't accept the --profile flag we need to set the environment variable AWS_PROFILE=dev-profile
More details on AWS SSO can be found [here](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-sso.html).

### Shell setup with 1Password

A better approach than saving credentials in plaintext is to fetch them from a password manager. Here we will use [1Password](https://1password.com) and [1Password cli](https://1password.com/downloads/command-line/). The first time you use the 1Password command-line tool, you will need to enter your sign-in address and email address, go [here](https://support.1password.com/command-line-getting-started/) for further details. After the initial setup, you should be able to sign in using your account shorthand.

```bash
# First-time sign in
op signin example.1password.com wendy_appleseed@example.com

# Account shorthand examples
eval $(op signin example)
eval $(op signin)
```

**Note:** for the rest of the setup create a 1Password vault called `XYZ_Company` and create a entry called `aws` with the fields `aws-access-key` and `aws-secret-key` with their values filled in. Copy [mfa-1password.sh](./bin/macos/mfa-1password.sh) to your home directory and make sure its executable `chmod +x mfa-1password.sh` add the alias to your `.bash_profile` or `.zshrc` file.

```bash
# Make sure that this path matches your mfa-1password.sh location
alias aw-mfa="/Users/$USER/mfa-1password.sh"
```

 Add the following to the end of `.bash_profile` or `.zshrc` file.

```bash
# Log into 1password and set AWS credentials
alias oplogin='eval $(op signin) && exec $SHELL'

export AWS_ACCESS_KEY_ID=`op get item --vault "XYZ_Company" aws --fields aws-access-key`
export AWS_SECRET_ACCESS_KEY=`op get item --vault "XYZ_Company" aws --fields aws-secret-key`
export AWS_MFA_SERIAL_NUMBER=arn:aws:iam::[account_id]:mfa/[username]
```

Apply shell changes by running `exec $SHELL`, then use alias `oplogin` to log into 1password and initialize your session then run alias `aw-mfa`. You should see the following output when its successful. After you're done running terragrunt or any other command under the assumed role, typing exit will take you back to your regular shell.

![mfa_1password_login](./assets/mfa_1password_login.png)

The nice thing about using 1Password when you need to set additional secrets, you can look them up from the vault.

```bash
export TF_VAR_database_password=`op get item --vault "XYZ_Company" aw-connect --fields staging-app-password`
```

### Shell setup with kms (coming soon)
