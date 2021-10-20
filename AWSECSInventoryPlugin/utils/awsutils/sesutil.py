import logging

from botocore.exceptions import ClientError

from base.aws_base_processor import AWSBaseProcessor
from data.program_data import ProgramData


class SES(AWSBaseProcessor):
    def __init__(self):
        super(SES, self).__init__('ses')
        self.ses = super().get_service_client()
        self.sender = ProgramData.get_instance().environment.value["ses_sender_email"]

    def send_notification(self, subject, html_body, recipients):
        # The character encoding for the email.
        CHARSET = "UTF-8"
        try:
            # Provide the contents of the email.
            return self.ses.send_email(
                Destination={'ToAddresses': recipients},
                Message={
                    'Body': {
                        'Html': {
                            'Charset': CHARSET,
                            'Data': html_body,
                        },
                        'Text': {
                            'Charset': CHARSET,
                            'Data': "",
                        },
                    },
                    'Subject': {
                        'Charset': CHARSET,
                        'Data': subject,
                    },
                },
                Source=self.sender,
            )
        except ClientError as e:
            logging.error("Email sending Exception:" + e.response['Error']['Message'])
            return False
