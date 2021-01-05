### short

- add parameter for autoredeploy with default value true
- remove commit temporarily

- codebuild status pinging script
- re- check logs script
- code- generate buildspec
- move stack.yaml into root

### medium

- commit messages
- replace GetAtt
- start_codebuild_build generating error
- buildspec to install python deps
- buildspec to run tests
- capture codebuild errors
- buildspec to use git tags
- slack alerts
- remove managed policies

### thoughts

- avoid having to specify ../ in codebuild src ?
  - not sure it's worth it
- upgrade all scripts to boto3, taking yaml files ?
  - probably not worth it at this stage
- script to get latest codebuild project status, on timer ?
  - probably not directly relevant yet

### done

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
