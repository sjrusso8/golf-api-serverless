# Golf Caddie - Serverless API for Posting Personal Golf Stats and Viewing Course Scorecards

## Demo

url link here

## Overview

I have really taken to golfing since graduating from college.  I have also loved to track personal data as a means to plot progress.  So why not combine them?!  

I have tried out a lot of different golf tracking apps, and was not a fan of any of them. Some tracked only a handful of stats, some lacked a good UI, and some didn't work half the time.  I decided to build out my own golf tracker where I can post hole-by-hole stats for any golf course in Ohio!

This means I needed A LOT of golf course data.  So in order to create a database record for every golf course in Ohio I had to scrape a lot of data.  You can see the whole code for the web scraper here.

## Why Serverless?

I really like to explore different frontend designs, and so I wanted to ensure I deployed an API that can be de-coupled from the front end.

## How does it work?

In order to leverage the best of serverless and my knowledge of Python I used the Django Rest Framework (DRF) and Zappa.  DRF makes creating a REST API a breeze, and Zappa makes deploying Python code to AWS super simple.  The hardest part is just configuring the different IAM policies inside AWS.

In order for the REST API to serve data from the AWS API Gateway it needs to source the data from somewhere.  To make the setup very simple (and cheap) I deployed the SQLite database into a S3 bucket.  The REST API sources the data from a secure bucket when it is called, and loads the data into JSON.

## Using Zappa

When deploying with Zappa make sure you run these handful of commands after deploying.

> zappa manage dev "makemigrations"
> zappa manage dev "migrate"
> zappa manage dev create_admin_user < user > < password >
> zappa manage dev "collectstatic --noinput"
