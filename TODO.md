### super short

- is looking for buildspec.yaml in lamdemo directory!
- revert buildspec src
- could buildspec be included inline, like in layers ?
- maybe its better to include it in the client, as it solves the deps issue
- maybe including it in the pipeline is over- centralisation
- maybe its equivalent to gitlab.yaml
- maybe just include it as root buildspec.yaml ? or better to specify ?
- maybe remove templates directory as you only have one template in each of target and pipeline
- rename deploy_pipeline.py as deploy_stack.yaml

### short

```
Phase context status code: YAML_FILE_ERROR Message: stat /codebuild/output/src990799852/src/templates/buildspec.yaml: no such file or directory
```

- start_codebuild_build generating following error

```
n error occurred (InvalidInputException) when calling the StartBuild operation: ArtifactsOverride must be set when using artifacts type CodePipelines
```

- auto restart codebuild on pipeline redeployment ?
  - this should at least be a default variable
  - avoid needing to tear pipeline down and redeploy each time

### medium

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
