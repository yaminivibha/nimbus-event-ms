from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

def lambda_handler(event, context):
    emails = event['Message']
    to_emails = []
    for email in emails:
        to_emails.append(Mail.To(email))

    message = Mail(
    from_email='nimbuseventupdates@gmail.com',
    to_emails=to_emails,
    subject='An Event You Signed Up For Has Changed!',
    html_content='<strong>Log Into Nimbus to see the event change details!</strong>')

    sg = SendGridAPIClient('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')
    
    try:
        sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
        response = sg.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)
    except Exception as e:
        print(e.message)
    
    
