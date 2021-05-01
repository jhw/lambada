### short

- retest
- tag

### layman

- add webhook function name

### medium

- create sample tag via Python
- eventbridge charts

### thoughts

- replace sns with direct lambda invocation ?
  - sns gives you a nice json message with records, which direct invocation does not
- convert scripts to python ?
  - probably not worth it
- codebuild charts ?
  - probably not worth it
- do you really want separation between app name and stack name ?
- `-lambada-ci` suffix to be stored in app.props ?
  - then u have problems finding app.props if loaded as a dependency
  - harcoding better for now probably
- pass git tag to cloudwatch events  ?
  - how
- how to keep git and pip tags in sync ?
- slack webhook to link to codebuild logs ?
  - first problem is you need to get region
  - second, what if aws change the url structure ?
  - seems better just to leave it as is
- buildspec to save head artifacts ?
  - no; see notes
- new assets folder for testing ?
  - not clear its worth it
- filter out stages/statuses ?
  - no because gives less info
  - solution is to have shorter messages
- script to auto- bump lamdemo ?
  - probably not worth it now
- better quote handling in input template ?
  - simply can't be bothered now
- script to inspect cloudwatch logs ?
  - doesn't seem worth it if webhook is working
- restrict number of messages being sent ?
- move build steps externally ?
  - don't think it's worth it
- consider moving webhook lambda, event pattern, event template into deploy script as args ?
  - feels like a lot of work, just need to get it over the line
  - also problems with respect to correct formatting of input template
- avoid coding codebuild failure into client project tests ?
- how to set event subject ?
- expand EventPattern ?
  - simply not worth it; it works and is what it is
- test removing EVENT filter ?
  - no is required
- PAT as secret ?
  - no because it's only needed at build time, not runtime
- remove build end time from ping_build.py
  - no is useful if a build has completed
- `fast` option to avoid zip/pip updates ?
  - probably not a lot of point if you have to add deps
- upgrade all scripts to boto3, taking yaml files ?
  - probably not worth it at this stage

### done

- re- check resource names
- custom event bus
  - https://console.aws.amazon.com/support/home?#/case/?caseId=8281695661&displayId=8281695661&language=en
- check codebuild custom deps vs default/test deps
- script to search webhook logs
- fix search build logs
- lamdemo to import moto
- remove *.pyc from s3 deployable
- flatten eventbridge event config
- rename list_auth.py as list_auth_creds.py
- scripts for auth events, auth resources
- clean up stack resource names
- moto test deps
- deploy auth
- update lamdemo auth arn
- deploy stack
- test tag creation
- script to list auth
  - aws codebuild list-source-credentials
- refactor pat_arn as auth  
- rename pat as auth
- deploy_pat to take command line arg
  - replace .py with .sh script
- new pat
- codebuild source auth [notes]
- test stack deployment/deletion
- test pat deployment/deletion
- delete_pat.py
- deploy_pat.py
- delete_stack.py needs to check if bucket exists
- bash scripts to split config arg and drop yaml
- test lamdemo deployment
- can't deploy project
  - check lamdemo project webhooks
  - new git tag
  - new slack webhook
- check master branch specified as default
- test
- delete_stack.py
- add waiter to all scripts
- add default branch param
- remove layman clean_artifacts.py
- delete stack to clean artifacts
- test if you can use NO_ARTIFACTS
- check if src, lambda paths collide 
- test deployment
- list_artifacts.py
- change value of buildspec ARTIFACTS
- change buildspec BUCKET_NAME to be local bucket
- deploy_stack.py should no longer pass bucket
- remove StagingBucket parameter, replace with local bucket ref
- add bucket to stack.yaml
- remove bucket from config
- notes re multiple builds
- all scripts to use `-lambada-ci` suffix
- why are we getting two builds triggered on each commit ?
- rename lambada/webhooks/slack.py as lambada/templates/webhook.py
- move stack.yaml to lambada/templates
- deploy_stack.py to manage stack as body rather than filename
- clean up codebuild projects
- remove managed policies
- revert AWS support
- remove burningmonk us-xxxx-x assets
- test removing webhook mocking
- webhook.py testing
- highlight webhook error message
- write up webhook process
- change build icon
- re- test process
- test failure
- pass webhook url as environment variable
- configure logging and check "slack says" message
- webhook to post
- sample post
- pass url as argument
- pass webhook as arg
- move webhook externally
- convert template to JSON
- clean_artifacts.py
- scripts/*.py to strip `.yaml` from $1 if not required
- see if cloudwatch event rule role is required
- see if sns topic policy is required
- reduce sns permissions down to sns:Publish
- restrict cloudwatch event permissions to sns:publish
- rename and move lambda invoke permission
- rename SampleNotification as CloudWatchEvent

- https://console.aws.amazon.com/support/home#/case/?displayId=7867317481&language=en
- https://stackoverflow.com/questions/65725094/sns-topic-not-receiving-codebuild-notifications

- topic policies
- project name ?
- cloudwatch event rule role arn
- test notification
- cloudwatch event rule with event pattern
- test pushing sns message
- sns/lambda connectivity
- test capturing of build failure
- single build phase
- test build on test.py runtime error
- log RAW_TAG, MOD_TAG
- move APP_NAME into env/variables
- remove head filter
- replace dots in tags
  - https://stackoverflow.com/questions/13043344/search-and-replace-in-bash-using-regular-expressions
- add tags filter
- test tags
- modify ARTIFACTS to use tag if available
- new tags branch
- commit/tag if/else example
- test calling git command
- test defining commit slug as variable
- https://console.aws.amazon.com/support/home#/case/?displayId=7830810411
- add requests to lamdemo
  - does it get built automatically ?
- list_builds.py needs to check against endTime not existing
- custom pip test deps
- custom git test deps
- list_builds.py
- ping_build.py should just take app name
- rename search-codebuild_logs as simply search_build_logs.py
- run tests
- script to ping latest codebuild status
- print buildspec on deployment
- code- generate buildspec
- move stack.yaml into root
- codebuild status pinging script
- replace start_build.sh with run_pipeline.sh

```
- ArtifactsOverride must be set when using artifacts type CodePipelines
```

- pipeline not restarting on redeploy
  - check pipeline redeploy spec
- handler is missing from s3 zipfile
- replace GetAtt
- test adding back commit messages
- re- check logs script
- fix missing s3 cp
- add parameter for autoredeploy with default value true
- remove commit temporarily
- hardcode buildspec parameter values and remove environment variables
- text- substitution of buildspec

```
[Container] 2021/01/05 09:41:48 Phase context status code: YAML_FILE_ERROR Message: mapping values are not allowed in this context at line 0
```

- rename deploy_pipeline.py as deploy_stack.py
- replace buildspec ref with inline buildspec, as per layers
  - pass as string
- script to ping codebuild process
- An error occurred (ValidationError) when calling the CreateStack operation: [/Resources/CodePipeline/Type/RestartExecutionOnUpdate] 'null' values are not allowed in templates
- test deployment
- complete pipeline deployment
- script to deploy pipeline
- script to get codebuild logs
- config.yaml
- boto3 script to list s3 assets w/ prefix
- lamdemo project
- script to list codebuild builds
- script to list codebuild projects
- script to list s3 assets
- buildspec to zip files, ignoring __pycache, *.pyc
- buildspec to include commit in artifact name
- buildspec to push to s3
- check codebuild artifact options for type CODEPIPELINE
  - CODEPIPELINE seems to completely bypass artifacts!
- PYTHON_VERSION parameter
- ensure codebuild is configured as per build_layer.py
- use buildspec similar to layer script
- consider renaming s3 bucket as staging bucket
- codepipeline/codebuild templates
- aws scripts
