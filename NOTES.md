### head filter 14/01/20

- problem with head filter is that once you have defined a tag, the `git describe --tags` command returns that latest tag, regardles of what the current commit is
- (it doesn't get un- tagged by a commit)
- this renders filtering of /refs/heads useless as it never gets called once the first tag is defined
- so best just remove it, so you only get builds on tags
- this is in fact a benefit as it removes the number of code build calls, and also makes pareto simpler in that you can only deploy on a tag

### git tags 14/01/20

```
commands.append("APP_NAME=%s" % config["globals"]["app"])
commands.append("RAW_TAG=$(git describe --tags --abbrev=0)")
commands.append("MOD_TAG=$(echo \"$RAW_TAG\" | sed -e 's/\W/-/g')")
commands.append("if [ -n \"$RAW_TAG\" ]; then ARTIFACTS=$APP_NAME-$MOD_TAG.zip; else ARTIFACTS=$APP_NAME-$CODEBUILD_RESOLVED_SOURCE_VERSION.zip; fi")
```

### git tags 05/01/20

- https://ruddra.com/aws-codebuild-use-git-tags/
- https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codebuild-project-webhookfilter.html
- https://awscli.amazonaws.com/v2/documentation/api/latest/reference/codebuild/create-webhook.html
- https://stackoverflow.com/questions/63143638/aws-codebuild-webhook-cloudformation

### codebuild notifications 05/01/21

- https://stelligent.com/2017/10/24/get-notified-on-aws-codepipeline-errors/
- https://docs.aws.amazon.com/codebuild/latest/userguide/sample-build-notifications.html

### github PAT 04/01/21

- https://docs.github.com/en/free-pro-team@latest/github/authenticating-to-github/creating-a-personal-access-token
- Settings -> Developer Settings -> Personal Access Tokens
- add Repo scopes