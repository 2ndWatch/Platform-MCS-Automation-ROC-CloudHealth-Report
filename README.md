
# CHscripts

[Introduction](#introduction)<br>
[Installation](#installation)<br>
[Usage](#usage)

## Introduction

This repository contains a validator program for the 2nd Watch ROC Cloud Health project. It is meant to speed up the process of verifying information gathered by the Cloud Health policies. Some clients have thousands of resources to be verified - ain't nobody got time for that.

![img.png](src/img_4.png)<br>
_Working on it... but not by hand._

## Installation

Prerequisite:

Follow the `aws-azure-login` [installation instructions](https://github.com/aws-azure-login/aws-azure-login#installation), with the following notes:
- You will need to install Node.js
- If installing on Windows, you probably don't need the Node.js optional extra packages like Chocolatey
- You will probably also not need the `puppeteer` dependency mentioned in the `aws-azure-login` installation instructions, as this is for a GUI interface.

Once that is installed, download the latest release of this program.

## Usage

Extract the files to an arbitrary location on your computer, add Cloud Health downloaded reports, and run the program from the terminal. See Confluence for specific instructions.