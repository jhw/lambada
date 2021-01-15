### short

- script to inspect cloudwatch logs
- slack webhooks

### medium

- codebuild charts
- avoid coding codebuild failure into client project tests
- remove burningmonk us-xxxx-x assets
- clean up codebuild projects
- remove managed policies
- revert AWS support

### thoughts

- reduce number of notifications ?
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
