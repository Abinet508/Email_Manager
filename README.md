GmailManager
# GmailManager

> > This Python script provides a class `Email` for sending and retrieving emails using SMTP and IMAP protocols.

## Dependencies

> > The script requires the following Python libraries:

- smtplib
- email
- imaplib
- os
- argparse

## Class: Email

> > The `Email` class is initialized with the sender's email address and the SMTP server to use for sending emails.

### Methods

#### `__init__(self, sender_email, smtp_server)`

Initializes the `Email` object.

Parameters:

- `sender_email` (str): The email address of the sender.
- `smtp_server` (str): The SMTP server to use for sending emails.

The sender's password is retrieved from the environment variable 'EMAIL_PASSWORD'.

#### `send_email(self, recipient_emails, subject, body, attachment=None)`

Sends an email.

Parameters:

- `recipient_emails` (list): A list of email addresses of the recipients.
- `subject` (str): The subject of the email.
- `body` (str): The body of the email.
- `attachment` (str, optional): The path to the attachment file (if any).

Returns:

- `str`: A message indicating the success or failure of the email sending process.

## Usage

> > To use this script, you need to import the `Email` class and create an instance with your email address and SMTP server. Then, you can use the `send_email` method to send an email.

```
from GmailManager import Email

email = Email('your-email@example.com', 'smtp.example.com')
email.send_email(['recipient1@example.com', 'recipient2@example.com'], 'Hello', 'This is a test email.')

```

## Note
> > Ensure that the environment variable 'EMAIL_PASSWORD' is set to the sender's email password before running the script.