"""Invoked by the application's local Playwright suite with disposable accounts."""
import json
import os
from urllib.parse import urlsplit
from robotomail import Robotomail, ApiError

f = json.loads(os.environ["ROBOTOMAIL_SDK_TEST"])
assert urlsplit(f["baseUrl"]).hostname in {"localhost", "127.0.0.1"}
with Robotomail(f["apiKey"], base_url=f["baseUrl"]) as full, Robotomail(f["scopedKey"], base_url=f["baseUrl"]) as scoped:
    assert full.get_account()["account"]["id"] == f["userId"]
    assert full.list_mailboxes()["mailboxes"][0]["id"] == f["mailboxId"]
    assert scoped.list_messages(f["mailboxId"], {"limit": 1, "offset": 0})["messages"][0]["id"] == f["messageId"]
    assert full.get_message(f["mailboxId"], f["messageId"])["message"]["bodyText"] == f["body"]
    scoped.update_mailbox(f["mailboxId"], {"displayName": "SDK integration"})
    assert full.get_mailbox(f["mailboxId"])["mailbox"]["displayName"] == "SDK integration"
    for call, status in [(lambda: scoped.get_account(), 403), (lambda: scoped.get_mailbox(f["foreignMailboxId"]), 404)]:
        try:
            call()
            raise AssertionError("Unauthorized request succeeded")
        except ApiError as error:
            assert error.status == status
    hook = scoped.create_webhook({"url": "https://example.com/sdk-fixture", "mailboxId": f["mailboxId"], "events": ["message.received"]})["webhook"]
    full.update_webhook(hook["id"], {"headers": None})
    assert full.get_webhook(hook["id"])["webhook"]["headers"] is None
    full.delete_webhook(hook["id"])
    sent = full.send_message(f["mailboxId"], {"to": ["delivered@resend.dev"], "subject": "Local SDK test", "bodyText": "No external email is delivered."})["message"]
    assert sent["status"] == "SENT" and sent["externalMessageId"].startswith("email-mock-")
    assert scoped.get_message(f["mailboxId"], sent["id"])["message"]["subject"] == "Local SDK test"
    print(json.dumps({"checks": 12, "sentMessageId": sent["id"]}))
