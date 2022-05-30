
# WEB HEALTH MONITORING via CRUD API Gateway

## SkipQ Cohort Voyager: Sprint 4

## Objective

Objective of sprint 4 is to get hands-on knowledge about AWS Cloud9 Environment and learn AWS Services: API Gateway and DynamoDB, RESTful API Gateway interface for web crawler CRUD operations, lambda function to back the API Gateway and extend test and prod/beta CI/CD pipelines in CodeDeploy/ CodePipeline. And use CI/CD to automate multiple deployment stages.
## Best Practices:

- Docstring in each fn describing overall working of function
- Modular approach should be used
- Avoid usage of local variables, make separate global vars file
- Use Environmental variables

## Technologies used:

- Python
- Python Requests
- AWS EC2
- AWS Cloud9
- AWS Lambda
- AWS SDK
- S3 Bucket
- AWS CloudWatch
- AWS SNS
- AWS DynamoDB
- AWS Secrets Manager
- AWS CodePipeline
- AWS CodeDeploy
- AWS API Gateway

## Requirements


- Use Cloud 9 IDE
- Language used Python v3.7.10
- CI/CD Pipeline
- API Gateway

First of all,  We have to setup the AWS cloud9 environment (our local machine). 

Starting with the following command:

``` vim ~/.bashrc ```

After running this command, Insert the following at the end:
``` alias python = '/usr/bin/python3' ```

Then execut these commands,

```
source ~/.bashrc
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip awscliv2.zip
sudo ./aws/install
```

Now Create a new directory where you want to initialize your CDK app, after doing that run the following commands step by step:

``` cdk init app --language python ```

This project is set up like a standard Python project.  The initialization
process also creates a virtualenv within this project, stored under the `.venv`
directory.  To create the virtualenv it assumes that there is a `python3`
(or `python` for Windows) executable in your path with access to the `venv`
package. If for any reason the automatic creation of the virtualenv fails,
you can create the virtualenv manually.

To manually create a virtualenv on MacOS and Linux:

```
$ python3 -m venv .venv
```

After the init process completes and the virtualenv is created, you can use the following
step to activate your virtualenv.

```
$ source .venv/bin/activate
```

If you are a Windows platform, you would activate the virtualenv like this:

```
% .venv\Scripts\activate.bat
```

Once the virtualenv is activated, you can install the required dependencies.

```
$ pip install -r requirements.txt
```

At this point you can now synthesize the CloudFormation template for this code.

```
$ cdk synth
```

To add additional dependencies, for example other CDK libraries, just add
them to your `setup.py` file and rerun the `pip install -r requirements.txt`
command.

## Useful commands

 * `cdk ls`          list all stacks in the app
 * `cdk synth`       emits the synthesized CloudFormation template
 * `cdk deploy`      deploy this stack to your default AWS account/region
 * `cdk diff`        compare deployed stack with current state
 * `cdk docs`        open CDK documentation

Happy Coding :)

Enjoy!
