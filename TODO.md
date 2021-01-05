### short

- run tests

### medium

- custom pip test deps
- custom git test deps
- capture codebuild test errors
- git tags
- slack alerts

- clean up codebuild projects
- remove managed policies

### thoughts

- `fast` option to avoid zip/pip updates ?
  - probably not a lot of point if you have to add deps
- add variable name for artifacts ?
  - probably not worth it if you're going to code- generate buildspec
- upgrade all scripts to boto3, taking yaml files ?
  - probably not worth it at this stage

### done

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
