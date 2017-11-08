# Contribution guidelines

This file sets out to establish common operating procedures when contributing to this project.

## Issues

All issues should be documented, tagged, and assigned.

## Branches

All branches should be named after the issue it resolves `1-contribution-guide` and created off of master.
**Commits cannot be made to master.**

```bash
$ git pull --rebase origin master // Update master
$ git checkout -b 1-contribution-guide
```

## Pull Requests

Must be reviewed by 1 team member. When branch resolves an issue it should be mentioned in the description `closes #ISSUE` to automatically close the issue on merge.
