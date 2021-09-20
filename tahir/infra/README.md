# How to run the project
npm install @aws-cdk/core@1.123.0
 # In setup.py, make sure to use "aws-cdk.core==1.123.0",
pip install -r requirements.txt
pip install aws_cdk.aws_iam aws_cdk.aws_events_targets aws_cdk.aws-lambda


# How to create a pull request

1. Fork Repo. 
2. Clone forked Repo
3. git checkout -b tahir-dev
4. git add . , git commit -m “”, 
5. git push --set-upstream origin new-branch
6. git remote -v
7. git remote add upstream  https://github.com/SkipQGit/cloudDevops.git
8. git fetch upstream
9. git merge upstream/main

# Using external libraries in your Python AWS Lambda in AWS CDK
Add required libraries need to go in requirements.txt with version number. e.g
requests==2.18.4

