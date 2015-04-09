#!/bin/bash
if [ ! -n "`git status -s`" ]; then
    echo "Repository clean."
    git checkout master
    echo "Pulling master:master..."
    git pull origin master
    git branch ignore-migrations
    git checkout ignore-migrations
    echo "Removing git indices of migrations..."
    git rm -rf --cached accounts/migrations/
    git rm -rf --cached blogs/migrations/
    git rm -rf --cached index/migrations/
    git rm -rf --cached products/migrations/
    git rm -rf --cached smartcontract/migrations/
    echo "Committing..."
    git add --all
    git commit -m "by ignore-migrations.sh"
    echo "Testing..."
    touch blogs/migrations/t.test
    if [ ! -n "`git status -s`" ]; then
        echo "PASS"
        rm blogs/migrations/t.test
        git checkout master
        git merge ignore-migrations
        git branch -d ignore-migrations
        echo "Everything fine. Better git-push ASAP!"
    else
        echo "ERROR"
        echo "Action aborted. Crime scene remained in branch ignore-migrations"
        git add --all
        git commit -m "by ignore-migrations.sh"
        git checkout master
    fi
    git status
else
    echo "Commit all changes and try this again."
fi

