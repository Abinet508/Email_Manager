import smtplib, email
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import imaplib
import os
import argparse

class Email:
    """
    A class for sending and retrieving emails.
    """

    def __init__(self, sender_email, smtp_server):
        """
        Initializes the Email object.

        Args:
            sender_email (str): The email address of the sender.
            smtp_server (str): The SMTP server to use for sending emails.
        """
        self.sender_email = sender_email
        self.sender_password = os.environ.get('EMAIL_PASSWORD')
        self.smtp_server = smtp_server

    def send_email(self, recipient_emails, subject, body, attachment=None):
        """
        Sends an email.

        Args:
            recipient_emails (list): A list of email addresses of the recipients.
            subject (str): The subject of the email.
            body (str): The body of the email.
            attachment (str, optional): The path to the attachment file (if any).

        Returns:
            str: A message indicating the success or failure of the email sending process.
        """
        message = MIMEMultipart()
        message["From"] = self.sender_email
        message["To"] = ", ".join(recipient_emails)
        message["Subject"] = subject

        message.attach(MIMEText(body, "plain"))

        if attachment:
            with open(attachment, "rb") as file:
                part = MIMEBase("application", "octet-stream")
                part.set_payload(file.read())
            encoders.encode_base64(part)
            part.add_header(
                "Content-Disposition",
                f"attachment; filename= {attachment.split('/')[-1]}",
            )
            message.attach(part)

        try:
            with smtplib.SMTP(self.smtp_server) as server:
                server.login(self.sender_email, self.sender_password)
                server.sendmail(self.sender_email, recipient_emails, message.as_string())
            return "Email sent successfully."
        except Exception as e:
            return f"Failed to send email. Error: {str(e)}"


    def get_emails_by_subject(self, subject):
        """
        Retrieves emails by subject.

        Args:
            subject (str): The subject of the emails to retrieve.

        Returns:
            list: A list of email objects matching the specified subject.
        """
        emails = []
        with imaplib.IMAP4_SSL(self.smtp_server) as server:
            server.login(self.sender_email, self.sender_password)
            server.select("inbox")
            _, data = server.search(None, f'SUBJECT "{subject}"')
            email_ids = data[0].split()
            for email_id in email_ids:
                _, email_data = server.fetch(email_id, "(RFC822)")
                raw_email = email_data[0][1]
                email_message = email.message_from_bytes(raw_email)
                emails.append(email_message)
        return emails

    def get_emails_by_body(self, body):
        """
        Retrieves emails by body.

        Args:
            body (str): The body of the emails to retrieve.

        Returns:
            list: A list of email objects matching the specified body.
        """
    
        emails = []
        with imaplib.IMAP4_SSL(self.smtp_server) as server:
            server.login(self.sender_email, self.sender_password)
            server.select("inbox")
            _, data = server.search(None, "ALL")
            email_ids = data[0].split()
            for email_id in email_ids:
                _, email_data = server.fetch(email_id, "(RFC822)")
                raw_email = email_data[0][1]
                email_message = email.message_from_bytes(raw_email)
                if body in email_message.get_payload():
                    emails.append(email_message)
        return emails
        

    def get_emails_by_date(self, date):
        """
        Retrieves emails by date.

        Args:
            date (str): The date of the emails to retrieve.

        Returns:
            list: A list of email objects matching the specified date.
        """
        emails = []
        with imaplib.IMAP4_SSL(self.smtp_server) as server:
            server.login(self.sender_email, self.sender_password)
            server.select("inbox")
            _, data = server.search(None, "ALL")
            email_ids = data[0].split()
            for email_id in email_ids:
                _, email_data = server.fetch(email_id, "(RFC822)")
                raw_email = email_data[0][1]
                email_message = email.message_from_bytes(raw_email)
                if date in email_message["Date"]:
                    emails.append(email_message)
        return emails

    def get_emails_by_recipient(self, recipient):
        """
        Retrieves emails by recipient.

        Args:
            recipient (str): The recipient of the emails to retrieve.

        Returns:
            list: A list of email objects matching the specified recipient.
        """
        emails = []
        with imaplib.IMAP4_SSL(self.smtp_server) as server:
            server.login(self.sender_email, self.sender_password)
            server.select("inbox")
            _, data = server.search(None, f'TO "{recipient}"')
            email_ids = data[0].split()
            for email_id in email_ids:
                _, email_data = server.fetch(email_id, "(RFC822)")
                raw_email = email_data[0][1]
                email_message = email.message_from_bytes(raw_email)
                emails.append(email_message)
        return emails

    def get_emails_by_sender(self, sender):
        """
        Retrieves emails by sender.

        Args:
            sender (str): The sender of the emails to retrieve.

        Returns:
            list: A list of email objects matching the specified sender.
        """
        emails = []
        with imaplib.IMAP4_SSL(self.smtp_server) as server:
            server.login(self.sender_email, self.sender_password)
            server.select("inbox")
            _, data = server.search(None, f'FROM "{sender}"')
            email_ids = data[0].split()
            for email_id in email_ids:
                _, email_data = server.fetch(email_id, "(RFC822)")
                raw_email = email_data[0][1]
                email_message = email.message_from_bytes(raw_email)
                emails.append(email_message)
        return emails
    
    def get_attachments(self, email):
        """
        Retrieves attachments from an email.

        Args:
            email (email.message.Message): The email from which to retrieve attachments.

        Returns:
            list: A list of attachment objects.
        """
        attachments = []
        for part in email.walk():
            if part.get_content_maintype() == "multipart":
                continue
            if part.get("Content-Disposition") is None:
                continue
            file_name = part.get_filename()
            if bool(file_name):
                attachments.append(part)
        return attachments
    
    def get_email_body(self, email):
        """
        Retrieves the body of an email.

        Args:
            email (email.message.Message): The email from which to retrieve the body.

        Returns:
            str: The body of the email.
        """
        if email.is_multipart():
            return self.get_email_body(email.get_payload(0))
        else:
            return email.get_payload(None, True)
        
    def get_email_subject(self, email):
        """
        Retrieves the subject of an email.

        Args:
            email (email.message.Message): The email from which to retrieve the subject.

        Returns:
            str: The subject of the email.
        """
        return email["Subject"]
    
    def get_email_sender(self, email):
        """
        Retrieves the sender of an email.

        Args:
            email (email.message.Message): The email from which to retrieve the sender.

        Returns:
            str: The sender of the email.
        """
        return email["From"]
    
    def get_email_recipient(self, email):
        """
        Retrieves the recipient of an email.

        Args:
            email (email.message.Message): The email from which to retrieve the recipient.

        Returns:
            str: The recipient of the email.
        """
        return email["To"]
    
    def get_email_date(self, email):
        """
        Retrieves the date of an email.

        Args:
            email (email.message.Message): The email from which to retrieve the date.

        Returns:
            str: The date of the email.
        """
        return email["Date"]
    
    def get_email_id(self, email):
        """
        Retrieves the ID of an email.

        Args:
            email (email.message.Message): The email from which to retrieve the ID.

        Returns:
            str: The ID of the email.
        """
        return email["Message-ID"]
    
    def get_email_content_type(self, email):
        """
        Retrieves the content type of an email.

        Args:
            email (email.message.Message): The email from which to retrieve the content type.

        Returns:
            str: The content type of the email.
        """
        return email.get_content_type()
    
    def get_email_content(self, email):
        """
        Retrieves the content of an email.

        Args:
            email (email.message.Message): The email from which to retrieve the content.

        Returns:
            str: The content of the email.
        """
        return email.get_payload()
    
    def get_email_headers(self, email):
        """
        Retrieves the headers of an email.

        Args:
            email (email.message.Message): The email from which to retrieve the headers.

        Returns:
            dict: A dictionary of the email headers.
        """
        return dict(email.items())
    

if __name__ == "__main__":
    
    parser = argparse.ArgumentParser() 
    parser.add_argument("--from_email", help="The email address of the sender.") 
    parser.add_argument("--to_email", help="The email address of the recipient.")
    args = parser.parse_args()
    from_email = args.from_email
    to_email = args.to_email
    if not from_email:
        raise ValueError("Please provide the email address of the sender.")
    if not to_email:
        raise ValueError("Please provide the email address of the recipient.")
    
    email = Email(from_email, "smtp.gmail.com")
    email.send_email([to_email], "Test", "This is a test email.", "test.txt")
    emails = email.get_emails_by_subject("Test")