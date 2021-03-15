#!/usr/bin/env bash

find . -name .DS_Store -print0 | xargs -0 git rm --ignore-unmatch
security delete-internet-password -s "git-codecommit.eu-west-1.amazonaws.com" ~/Library/Keychains/login.keychain-db
git add .
git commit -m "commit-"$(date +%s)
git push