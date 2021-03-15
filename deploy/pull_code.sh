#!/usr/bin/env bash

security delete-internet-password -s "git-codecommit.eu-west-1.amazonaws.com" ~/Library/Keychains/login.keychain-db
git pull