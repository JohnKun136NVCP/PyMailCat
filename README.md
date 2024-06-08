<p align="right">
    <img src="./src/email-sent.png" with="15px" heigh="15px" align="right">
</p>

# PyMailCat 🐈📧

PyMailCat is a Python interface built using Dear PyGui. It provides a user-friendly way to manage emails and perform various tasks related to email communication.

This repository houses a delightful graphical interface for sending emails with attachments. Whether it’s PDFs or images, our feline postman ensures your messages reach their destination with a touch of whiskered charm. 🐾📧🐱

## Features

- **Compose Email**: Create and send new emails.
- **Search**: Search for specific emails based on keywords or sender.
- **Attachments**: Handle email attachments.
- **Settings**: Configure your email recipients and preferences.

## Installation 🔧

1. Clone this repository:
   ```
   git clone https://github.com/JohnKun136NVCP/PyMailCat.git
   ```
2. Enter the repository directory

   ```
   cd PyMailCat/
   ```
3. Install dependencies:
   ```
   pip install -r requirements.txt 
   ```
4. Run the application:
   ```
   python main.py
   ```

## SMTP Services Available
- Gmail. You need two factor authentication and create password app. See more here [sign in with app passwords
](https://support.google.com/accounts/answer/185833?hl=en&sjid=2504093778559336064-NC&dark=1).
- Outlook (use your personal password)
- Yahoo (user your personal password)
## How it works?.
1. Enter your e-mail address
2. Enter your subject
3. ⚠️ Important! Choose whether you want to add a recipient manually. However, if you choose a file, the program will open the file browser. Select your TXT or Excel or CSV file.
4. ⚠️ If you choose to write your body manually, it is important that you select the *Manual text* button. You can upload TXT (supports UTF-8) or html (also supports UTF-8) files.
5. (OPTIONAL) You can upload images or PDF files. (⚠️ Make sure that both are in the same directory if you choose *Both*).
6. Tab. Important. ⚠️. Choose the *manual* option before typing your token and then select *Google* if it is your SMTP service.
7. Send your email(s)

⚠️ If you have more than 200 recipients, Google does not allow you to send many emails.
## Interface

![](/img/email_cat_1.png)

![](/img/email_cat_1%20-%20param.png)

## Sending emails
![](/img/email_cat-sender.png)

![](/img/email_cat-popupgood.png)

![](/img/sender-ok.png)

## Empty email or sending with wrong data

![](/img/email_cat-popupbad.png)


## Available on
- Windows
- Linux
- MacOS

## Contributing

Contributions are welcome! If you find any issues or have suggestions, feel free to open an issue or submit a pull request.

