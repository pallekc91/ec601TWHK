import smtplib, ssl


# coding=utf-8
def sendemail(mail_cred_json_file, username, content):
	with open(mail_cred_json_file) as json_file:
        emailCreds = json.load(json_file)
    port = 465  # For SSL
    smtp_server = "smtp.gmail.com"
    sender_email = emailCreds['sender']  # Enter your address
    receiver_email = emailCreds['receiver']  # Enter receiver address
    password = emailCreds['password']
    message = """    Subject: Gravience from twitter
    """ + "\n" + content + "\n" + "From " + username

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message)