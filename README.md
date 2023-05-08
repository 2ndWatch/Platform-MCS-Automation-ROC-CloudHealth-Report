
# CHscripts

[Introduction](#introduction)<br>
[Installation](#installation)<br>
[Usage](#usage)

## Introduction

This repository contains a validator program for the 2nd Watch ROC Cloud Health project. It is meant to speed up the process of verifying information gathered by the Cloud Health policies. Some clients have thousands of resources to be verified - ain't nobody got time for that.

![img.png](src/img_4.png)<br>
_Working on it... but not by hand._

## Installation

Prerequisites:
- AWS CLI: [Installing the AWS Command Line Interface](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html)
- Python: [Download Python](https://www.python.org/downloads/) 

Before running any scripts, install the required non-default Python packages: `pip install -r /path/to/requirements.txt`. This is best done in a separate virtual environment for this script, so that these packages don't mess with any other packages in your OS. Don't go down the dependencies rabbit hole, it's not a good place to be.

Authentication will be through `aws-azure-login`. Perform these steps from the terminal in your IDE; I use PyCharm and the Git Bash terminal because I'm weird, but this should work fine in VS Code and a Powershell/command prompt terminal too. You could even run these commands in a standalone terminal window from within the folder that contains these scripts, and use a basic text editor where needed, but are you _really_ that kind of heathen? 

Follow the `aws-azure-login` [installation instructions](https://github.com/aws-azure-login/aws-azure-login#installation), with the following notes:
- You will need to install Node.js
- If installing on Windows, you probably don't need the Node.js optional extra packages like Chocolatey
- You will probably also not need the `puppeteer` dependency mentioned in the `aws-azure-login` installation instructions, as this is for a GUI interface.

## Usage

Downloaded Cloud Health reports should go in the `cloudhealth` directory. Those downloaded files must adhere to the following naming conventions:
- _insert naming conventions_

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

After you are done selecting clients, the program attempts to log into client accounts, one by one. Each account login requires MFA approval, so you will need to watch for the approval push notification via Microsoft Authenticator. Approve the sign-in, and the program is authenticated into the account.

The program automatically collects resource detailss from every region specified in the clients.txt file for the selected account(s), and compiles all the valid resources of a particular type from all of a given client's accounts into one dataframe. That dataframe is used to compare resources against those collected by Cloud Health. Finally, the program transforms the resource information into three sheets in an Excel file:
- matched resources that both Cloud Health and this program have identified as wasted spend;
- unmatched resources that this program has identified that were not picked up by Cloud Health;
- excluded resources that Cloud Health identified but do not/no longer meet the filtering criteria.

The Excel files are created in the root directory of the program.

The program also outputs a fair amount of test to the terminal as it runs. This text can be used for debugging, if needed, or simplyto monitor the program's progress.