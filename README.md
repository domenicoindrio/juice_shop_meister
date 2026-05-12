# Juice Shop Meister - Challenges Extract
This repository features a selection of four hacking challenges from the **OWASP Juice Shop** (including video walktroughs), demonstrating practical exploitation and mitigation techniques. 

This repository was created during my training at the ***Developer Akademie***.

> [!WARNING]  
> The content provided in this repository is for educational and ethical security testing purposes only. All demonstrations were performed in a controlled, local environment using the OWASP Juice Shop, a deliberately insecure web application. Unauthorized access to computing systems is illegal. The author is not responsible for any misuse of this information. Always obtain explicit permission before testing any system that you do not own.

## Table of Contents:
- [Overview](#overview)
- [Prerequisites](#prerequisites)
- [The Target](#the-target)
- [Challenges](#challenges)
    - [XXE Data Access](#xxe-data-access)
    - [Database Schema (with bonus challenge User Credentials)](#database-schema-with-bonus-challenge-user-credentials)
    - [Admin Registration](#admin-registration)
    - [Captcha Bypass](#captcha-bypass)
- [Extended Documentation](#extended-documentation)

## Overview
This README functions as the *Main Hub* and provides technical prerequisites, toolset and a summary of the challenges reports.

For a in-depth analysis, each challenge is documented in its own dedicated directory and follow the same structure:
- **Vulnerability Overview**
- **Risk and Impact**
- **Reproduction Steps** (including a video walktrough)
- **Remediation**

## Prerequisites
To reproduce these challenge in an isolated local environment, following setup is recommended:

### Local Hosting Requirements
- **Virtualization Software** (VirtualBox, VMware Fusion, etc.)
- **Operating System** of choice (in this project was used Kali Linux)
- [**Juice Shop** (Installation through Node.js, Docker, etc.)](https://github.com/juice-shop/juice-shop#setup)

### Tools & Technologies
- **[Burp Suite](https://portswigger.net/burp)**: Used as proxy for request manipulation, fuzzing (Intruder), and manual exploitation (Repeater).
- **Python 3:** for custom scripting.

## The Target
The web application used in this project as the **Target**, is the *deliberately vulnerable* [**OWASP Juice shop**](https://owasp.org/www-project-juice-shop/).  
Citing the official website:
> OWASP Juice Shop is probably the most modern and sophisticated insecure web application! It can be used in security trainings, awareness demos, CTFs and as a guinea pig for security tools! Juice Shop encompasses vulnerabilities from the entire OWASP Top Ten along with many other security flaws found in real-world applications!

## Challenges
### XXE Data Access
- **Summary**: This challenge exploits a vulnerability in a deprecated XML file upload feature. By defining an External Entity into a XML payload, the (misconfigured) server's parser resolves it and leaks sensitive system files (like /etc/passwd).
- [Full Report and Video Walkthtough](./Challenges/XXE%20Data%20Access/README.md)

### Database Schema (with bonus challenge User Credentials)
- **Summary**: Using a UNION-based SQL Injection, the application's search logic is bypassed and the internal SQLite database structure is extracted. The Chain of Attack then continues with one additional SQL injection, exfiltrating all user credentials (emails and hashed passwords).
- [Full Report and Video Walkthtough](./Challenges/Database%20Schema/README.md)

### Admin Registration
- **Summary**: By manipulating the JSON body of a registration request, administrative privileges are granted to a newly created account. 
- [Full Report and Video Walkthtough](./Challenges/Admin%20Registration/README.md)

### Captcha Bypass
- **Summary**: By reusing a Captcha Token, the bot protection is bypassed and the server is flooded with feedbacks.
- [Full Report and Video Walkthtough](./Challenges/Captcha%20Bypass/README.md)

## Extended Documentation
While this repository highlights a curated selection of challenges, I am compiling my raw notes from the remaining challenges into a dedicated *Learning Log* (that I will upload sometime soon). This separate repository will serve as a chronological journal of my journey, documenting initial findings, frustrations, breakthroughs, and technical evolution as I work my way through the entire Juice Shop catalog.