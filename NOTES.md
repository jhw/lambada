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