### SNS and eventbridge 30/04/21

- importance of SNS is that it wraps the raw message in an [SNS] envelope for nicer handling at the Lambda level; otherwise you just get a very raw template
- is possible there are other benefits also
- so sometimes it might feel like you are over- using AWS components but it's really just to enable a nicer flow
- and eventbridge is really just a pattern matcher
- which is useful when connected with dynamodb as allows you to route different messages coming from the DDB stream
- sometime it feels like each AWS service is really just a single programming language feature

### codebuild source credential 28/04/21

- https://docs.aws.amazon.com/codebuild/latest/userguide/access-tokens.html
- https://stackoverflow.com/questions/57066101/how-do-you-specify-github-access-token-with-codebuild-from-cloudformation

### stack creation failure 28/04/21

```
 2021-04-28T12:05:43.910Z|  CodeBuildProject                  |  AWS::CodeBuild::Project          |  CREATE_FAILED        |  Failed to call CreateWebhook, reason: Unable to create webhook at this time. Please try again later. (Service: AWSCodeBuild; Status Code: 400; Error Code: OAuthProviderException; Request ID: 756134a2-711c-4474-b64a-d57aa51abdad; Proxy: null)
 ```

- resolved by adding a new PAT

### local staging bucket 26/02/21

- note that bucket is used for two things
  - download of git assets
  - final build
- not sure what format source will be saved in, but likely under /src
- so want artifacts to be saved under /lambda/#{tag}.zip
- add bucket to stack.yaml
- remove StagingBucket parameter and replace with local bucket
- remove bucket from config
- deploy_stack.py no longer passes bucket
- need to change construction of buildspec
- BUCKET_NAME is now local artifacts bucket, not global bucket
- change value of ARTIFACTS
- artifacts script to look up src, lambdas

### triggering of multiple builds 26/02/21

- every time you push a tag of target repo, generates multiple codebuild processes
- and no amount of deleting the AWS app or changing the git PAT seems to work
- turns out you have a stray webhook on the git side
- the AWS stack, specifically the codebuild project, must create a webhook on the target git repo
- see github -> project -> settings -> webhooks
- sometimes deleting the AWS project doesn't clean up the webhook, deletion must fail
- if you then rebuild the AWS project, you now have two webhooks, probably pointing to an AWS project of the same name
- haven't tested this but changing the AWS project name probably improves things
- but simplest thing is just to clean up the webhook

### slack webhooks 15/02/21

- if you already have a slack app then you don't need to create a new one to add a webhook; you can have multiple webhooks attached to a single app, it seems
- just need to "add features" to app
- then "enable webhooks" will take you into webhook addition territory

### buildspec head artifacts 22/01/21

- it would be nice to be able to report the tag in the slack messages
- but how to get the tag name into the notification channel ?
- would be nice to be able to send it as part of notifications
- but how to export tag name from codebuild into notification channel ?
- feels like you would need codebuild custom notification and haven't seen any support for that anywhere

- alternative mechanism would be to dump it so s3 as part of a header file
- but this would have to be done as part of build phase, so wouldn't be available to all phases
- so feels like a lot of work for little benefit

- the event notification channel feels like a much better solution, if a way can be found

- but overall it might just be better to provide a link to the codebuild logs, which you can inspect and see the tag there
- maybe reporting the tag in slack is overkill
- and you should only have occasional tags, its not like they are going to overlap

### webhooks 20/01/21

- https://api.slack.com/messaging/webhooks
- https://api.slack.com/apps?new_app=1
- enable incoming webhooks
- add webhook to app
- add app icon

### webhooks 15/01/21

- https://api.slack.com/messaging/webhooks
- create slack app
- activate incoming webhooks
- create channel for app
- add new webhook to workspace
- get url
- pass url as argument
- POST to url
- highlight error messages

---

- https://api.slack.com/apps
- [select app] -> add features and functionality -> incoming webhooks -> add New Webhook to Workspace

### codebuild notifications 14/01/21

- https://stelligent.com/2017/10/24/get-notified-on-aws-codepipeline-errors/
- https://medium.com/taptuit/add-notifications-to-your-aws-ci-cd-pipeline-251bba894360
- https://docs.aws.amazon.com/codebuild/latest/userguide/sample-build-notifications.html
- https://stackoverflow.com/questions/62308836/unable-to-successfully-set-up-sns-on-codebuild-project-through-cft-but-works-man

### head filter 14/01/21

- problem with head filter is that once you have defined a tag, the `git describe --tags` command returns that latest tag, regardles of what the current commit is
- (it doesn't get un- tagged by a commit)
- this renders filtering of /refs/heads useless as it never gets called once the first tag is defined
- so best just remove it, so you only get builds on tags
- this is in fact a benefit as it removes the number of code build calls, and also makes pareto simpler in that you can only deploy on a tag

### git tags 14/01/21

```
commands.append("APP_NAME=%s" % config["globals"]["app"])
commands.append("RAW_TAG=$(git describe --tags --abbrev=0)")
commands.append("MOD_TAG=$(echo \"$RAW_TAG\" | sed -e 's/\W/-/g')")
commands.append("if [ -n \"$RAW_TAG\" ]; then ARTIFACTS=$APP_NAME-$MOD_TAG.zip; else ARTIFACTS=$APP_NAME-$CODEBUILD_RESOLVED_SOURCE_VERSION.zip; fi")
```

### git tags 05/01/21

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