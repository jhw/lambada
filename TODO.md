### short

- buildspec to zip files, ignoring __pycache, *.pyc

- script to list s3 assets
- script to list codebuild projects
- script to list codebuild builds
- script to show codebuild logs

- lamdemo project
- git PAT

### medium

- buildspec to use git tags
- buildspec to run tests
- buildspec to install python deps
- capture codebuild error
- slack alerts
- remove managed policies

### thoughts

### done

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
