from robotomail import Robotomail

with Robotomail() as mail:  # reads ROBOTOMAIL_API_KEY
    result = mail.list_mailboxes()
    print([box["fullAddress"] for box in result["mailboxes"]])
