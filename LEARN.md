<p align="right">
    <img src="./src/email-sent.png" with="20px" heigh="20px" align="right">
</p>

# PyMailCat 🐈📧

PyMailCat is a Python interface built using Dear PyGui. It provides a user-friendly way to manage emails and perform various tasks related to email communication.

This repository houses a delightful graphical interface for sending emails with attachments. Whether it’s PDFs or images, our feline postman ensures your messages reach their destination with a touch of whiskered charm. 🐾📧🐱

## How I built it?
- Using Python versión 3.10.
- Pandas
- opencv
- dearpy

## What is a SMTP?
**SMTP** means *Simple Mail Transfer Protocol*, we are talking about the email (i.e Gmail, Yahoo, Outlook, etc.).

## SMTP into a interface?
Yes, and you can add pictures as PDF Files (NOT USED FOR MALICIOUS INTENTIONS). You can use a interface for sending from your (GMAIL, OUTLOOK or Yahoo).
If you have a any companie and you want to send emails to your costumers, you can use this tool. However, **Google only admits 1<=100 recipients by email**.

## What can you use it?
- Upload a TXT, Excel or CSV file with recipients.
- Upload Pictures, PDF files.
- Use BCC for recipients


>[!NOTE]
> For **Gmail acount**. You need two factor authentication and create password app. See more here [sign in with app passwords
](https://support.google.com/accounts/answer/185833?hl=en&sjid=2504093778559336064-NC&dark=1).
> For **Outlook and Yahoo aconnt**. You will need to use your personal password

>[!WARNING]
>Choose whether you want to add a recipient manually. However, if you choose a file, the program will open the file browser. Select your TXT or Excel or CSV file (Your column of your email must say 'Email'.)

>[!WARNING]
>If you choose to write your body manually, it is important that you select the *Manual text* button. You can upload TXT (supports UTF-8) or html (also supports UTF-8) files.

>[!NOTE]
>(OPTIONAL) You can upload images or PDF files. (Make sure that both are in the same directory if you choose *Both*).

>[!NOTE]
>Tab. Important. Choose the *manual* option before typing your token and then select *Google* if it is your SMTP service.

>[!WARNING]
>Google only admits 1<=100 recipients by email

