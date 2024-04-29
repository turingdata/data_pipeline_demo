#!/bin/bash

set -euo pipefail
IFS=$'\n\t'

# Required Environment Variables
# AWS_ACCESS_KEY_ID
# AWS_SECRET_ACCESS_KEY
# AWS_MFA_SERIAL_NUMBER=arn:aws:iam::[account_id]:mfa/[username]

# Get an MFA token from the user
readMfaCode() {
  printf "Enter an MFA code: "
  read MFA_CODE
}

1password_mfa(){
  printf "Reading MFA token from 1Password"
  MFA_CODE=`op get totp --vault "Allied World" aws`
}
# Get a session token from AWS and save it to a file
getSessionToken() {
  realGetSessionToken
  # Sometimes this fails, I don't know why, re-running it makes it work
  if [ -z "$AWS_CLI_RESPONSE" ]
  then
    echo "\$AWS_CLI_RESPONSE is empty"
    realGetSessionToken
  fi
}
realGetSessionToken() {
  AWS_CLI_RESPONSE=`aws sts get-session-token \
    --serial-number $AWS_MFA_SERIAL_NUMBER \
    --token-code $MFA_CODE \
    --duration-seconds 43200`
}
exportAwsKeys() {
  export AWS_ACCESS_KEY_ID=$(echo $AWS_CLI_RESPONSE | jq -r .Credentials.AccessKeyId)
  export AWS_SECRET_ACCESS_KEY=$(echo $AWS_CLI_RESPONSE | jq -r .Credentials.SecretAccessKey)
  export AWS_SESSION_TOKEN=$(echo $AWS_CLI_RESPONSE | jq -r .Credentials.SessionToken)
}
assumeRole() {
  AWS_CLI_RESPONSE=`aws sts assume-role \
    --role-arn arn:aws:iam::${AWS_ACCOUNT_ID}:role/allow-full-access-from-other-accounts \
    --role-session-name aw-aws \
    --duration-seconds 3600`
}
# including this to prove to the caller that it worked
proveIt() {
  aws sts get-caller-identity
}
# Save the original credentials so we can reset later
export ORIGINAL_AWS_ACCESS_KEY_ID=${ORIGINAL_AWS_ACCESS_KEY_ID:-$AWS_ACCESS_KEY_ID}
export ORIGINAL_AWS_SECRET_ACCESS_KEY=${ORIGINAL_AWS_SECRET_ACCESS_KEY:-$AWS_SECRET_ACCESS_KEY}
export AWS_ACCESS_KEY_ID=${ORIGINAL_AWS_ACCESS_KEY_ID}
export AWS_SECRET_ACCESS_KEY=${ORIGINAL_AWS_SECRET_ACCESS_KEY}
echo "Accounts and Auth: https://github.com/alliedworld/infrastructure-live/blob/master/_docs/08-accounts-and-auth.md"
PS3="Choose an environment: "
options=("dev: 805321607950" "stage: 645769240473" "prod: 608056288583" "security: 296216577101" "shared-services: 451511469926" "Quit")
select opt in "${options[@]}"
do
  case $opt in
    "dev: 805321607950")
      AWS_ACCOUNT_ID=805321607950
      ;;
    "stage: 645769240473")
      AWS_ACCOUNT_ID=645769240473
      ;;
    "prod: 608056288583")
      AWS_ACCOUNT_ID=608056288583
      ;;
    "security: 296216577101")
      AWS_ACCOUNT_ID=296216577101
      ;;
    "shared-services: 451511469926")
      AWS_ACCOUNT_ID=451511469926
      ;;
    "Quit")
      break
      ;;
    *) echo "invalid option $REPLY";;
  esac
  echo "Loading Account: ${AWS_ACCOUNT_ID}"
  1password_mfa
  getSessionToken
  exportAwsKeys

  if [ "$AWS_ACCOUNT_ID" != "296216577101" ]
  then
    assumeRole
    exportAwsKeys
  fi

  proveIt
  break
done

$SHELL
