
# CHscripts

[Introduction](#introduction)<br>
[ch-getresources](#ch-getresources.py)<br>
[ch-parsley.py](#ch-parsley.py)<br>
[Installation](#installation)<br>
[Authentication](#authentication)<br>
[Usage](#usage)

## Introduction

This repository contains helper scripts for the 2nd Watch ROC Cloud Health project. These scripts are meant to speed up the process of verifying information gathered by the Cloud Health policies. Some clients have thousands of resources to be verified - ain't nobody got time for that.

![img.png](src/img_4.png)<br>
_Working on it... but not by hand._

## main.py
Work in progress!

This is the primary user interface for this suite of scripts.

## getresources.py
Work in progress!

Mostly complete. Resources are collected into dataframes. Working on comparing resource data with Cloud Health data using pandas.

## ch-parsley.py
Work in progress!

Actions:
- Reads from cypherworxmain-us-east-1-old-images.csv and makes Cypherworx-RAW.xlsx
- Reads from Cypherworx-RAW.xlsx and compares policy-alert-2023-04-28-9345855749691.csv

---- Cypherworx-RAW.xlsx ----

The script will grab info from the AWS generated csv 'cypherworxmain-us-east-1-old-images.csv' and check to see if an AMI was created within the last 90 days. If so, it will copy that entry from the 'main-us-east-1-old-images' sheet to either the 'false-alarms' or 'valid-alarms' sheets.

---- Cypherworx-Matching.xlsx ----

The script verifies if info from Cypherworx-RAW.xlsx sheet 'main-us-east-1-old-images' and info grabbed from CloudHealth 'policy-alert-2023-04-28-9345855749691.csv' match. If they do, they go to the 'matched' sheet, else they go to the 'unmatched' sheet.

## Installation

Prerequisites:
- AWS CLI: [Installing the AWS Command Line Interface](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html)
- Python: [Download Python](https://www.python.org/downloads/) 

Before running any scripts, install the required non-default Python packages: `pip install -r /path/to/requirements.txt`. This is best done in a separate virtual environment for this script, so that these packages don't mess with any other packages in your OS. Don't go down the dependencies rabbit hole, it's not a good place to be.



Authentication will be through `aws-azure-login`. Perform these steps from the terminal in your IDE; I use PyCharm and the Git Bash terminal because I'm weird, but this should work fine in VS Code and a Powershell/command prompt terminal too. You could even run these commands in a standalone terminal window from within the folder that contains these scripts, and use a basic text editor where needed, but are you _really_ that kind of heathen? 

- Follow the `aws-azure-login` [installation instructions](https://github.com/aws-azure-login/aws-azure-login#installation):
  - You will need to install Node.js
  - If installing on Windows, you probably don't need the Node.js optional extra packages like Chocolatey
  - You will probably also not need the `puppeteer` dependency mentioned in the `aws-azure-login` installation instructions, as this is for a GUI interface.




## Usage

This program is best run in its own virtual environment, to keep environment variables and authentication information segregated from the rest of your operating system. I run it from the terminal in my IDE.

To start the program, make sure your terminal is in the root directory of the project. Enter `python main.py`.

![img.png](src/img.png)
_Schmancy!_

Your username is what you log into My Apps with, minus the '@2ndwatch.com' part. 

After entering your username, you will be prompted for a password. This is the same password you use to log into My Apps.

![img_1.png](src/img_1.png)
_No, you can't see my password. Nice try._

At this point, you will be asked to select which client or clients you want to collect resource information for. You can also exit the program from here.

If you choose option a, you will see the following prompt:

![img_2.png](src/img_2.png)

If you choose option b, you will see the following prompt:

![img_3.png](src/img_3.png)
_I selected some things._

After you are done selecting clients, the program will attempt to log into client accounts, one by one. Each account login requires MFA approval, so you will need to watch for the approval push notification via Microsoft Authenticator. Approve the sign-in, and you will be authenticated into the account.

The program will then automatically collect resources from every region specified in the clients.txt file for a given account, and will compile all the valid resources of a particular type from all of a given client's accounts into one dataframe. That dataframe is used to compare resources against those collected by Cloud Health. 