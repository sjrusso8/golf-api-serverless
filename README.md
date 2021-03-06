# Golf Caddie - Serverless API for Golf Stats and Course Data

<img src="./img/tiger_lambda.png" alt="tiger woods serverless" width="350"/>

## Demo

Check out the demo site of the API in action.  

The user account is *joegolfer@golfapi.com* and password is *overpar!*.  

[Golf Caddie Live Demo](http://golf.stevenjrusso.com/login)

**Please note** logging in for the first time might take awhile since the lambda function needs to start up.

## Overview

I have really taken to golfing since graduating from college.  I have also loved to track personal data as a means to plot progress.  So why not combine them?!  

I have tried out a lot of different golf tracking apps, and was not a fan of any of them. Some apps only tracked only a handful of stats, some lacked a good UI, and some didn't work half the time.  I decided to build out my own golf tracker where I can post hole-by-hole stats for **any golf course in Ohio!**

## Collecting the Data for every Course in Ohio

To make this API worth while it meant that I had to collect A LOT of golf course data. So in order to create a database record for every golf course in Ohio I had to scrape a lot of data.  The code for the web scraper is here [Course Scraper](https://github.com/sjrusso8/golf-serverless-scraper).  The data is directly loaded into the database as the **web scraper** combs through the different course score cards and GPS data.

## Why Serverless?

### Pros

Serverless computing has become a huge topic in the cloud world.  Serverless computing makes creating different services super agile, and you can respond to changes faster.   The components used in this project relate heavily on **AWS Lambda** and **Aurora Serverless Postgres**. The combination of these two leads to a super reduced cost, automatic scaling, and high availability.  

### Cons

Serverless computing has an additional factor called 'cold start time'.  A 'cold start time' is the time it takes the AWS Lambda to load, mount, and run the script.  This is noticeable when trying to login with the dummy user for the first time.

## How does it work?

In order to leverage the best of serverless and my knowledge of Python I used the Django Rest Framework (DRF) and Zappa.  DRF makes creating a REST API a breeze, and Zappa makes deploying Python code to AWS Lambda super simple.  The hardest part is just configuring the different IAM policies inside AWS.

In order for the REST API to serve data from the AWS API Gateway it needs to source the data from somewhere.  The static assets are stored in S3, and all the data is saved to an Aurora Serverless DB.

## API Docs

View the Open API doc [here](https://fiqohtk7w5.execute-api.us-east-2.amazonaws.com/dev/swagger/)

**Please note** For the live demo I displayed POST methods on most models.

## Areas for more development

- [x] JWT Authentication
- [x] User Profiles with images
- [x] Round Summary
- [x] Shot by Shot statistics
- [x] Mobile friendly UI
- [x] Redepoly Aurora RDS with Terraform
- [ ] Render GPS Coordinates in UI
- [ ] User forms to post detailed data to API
- [ ] Anything else?

## Using Zappa

When deploying with Zappa make sure you run these handful of commands after deploying.

> zappa manage dev create_db
> 
> zappa manage dev migrate
> 
> zappa invoke --raw dev "from apps.users.models import User; User.objects.create_superuser('< email >', '< password >')"
> 
> zappa manage dev "collectstatic --noinput"

## Using Terraform

I am currently in the process of moving the infrastructure state into Terraform.  Terraform allows for infrastructure to be deployed as code (IaC).  This is a great way to manage all the settings of AWS Resources in one spot.  There is a potential conflict with 'Zappa' vs 'Terraform' on the deployment of the lambda function.  As of right now I plan on keeping the lambda function, api gateway, and a few other resources managed by 'Zappa'.
