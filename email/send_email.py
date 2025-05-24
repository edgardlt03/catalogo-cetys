import smtplib

def send_mail():
    server = smtplib.SMTP('localhost', 25)
    server.sendmail('from@example.com', 'to@example.com', 'Subject: Test\n\nHello WebCraft!')
    server.quit()
