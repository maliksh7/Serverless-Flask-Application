
# Serverless Flask Application with Docker, ECR and ECS

## SkipQ Cohort Voyager: Sprint 6

### Objective

Objective of sprint 6 is to get hands-on knowledge about FLASK, ECS, ECR, Docker and Fargate.


### Best Practices:

- Docstring in each fn describing overall working of function
- Modular approach should be used
- Avoid usage of local variables, make separate global vars file
- Use Environmental variables


### Technologies used:

- Flasks
- ECR
- ECS
- Fargate
- Docker Images

### Requirements


- Use Cloud 9 IDE
- Language used Python v3.7.10
- Flask 2.0.3
- Docker
- ECR and ECS along with Fargate

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



The `cdk.json` file tells the CDK Toolkit how to execute your app.

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

### Useful commands

 * `cdk ls`          list all stacks in the app
 * `cdk synth`       emits the synthesized CloudFormation template
 * `cdk deploy`      deploy this stack to your default AWS account/region
 * `cdk diff`        compare deployed stack with current state
 * `cdk docs`        open CDK documentation

Enjoy!


