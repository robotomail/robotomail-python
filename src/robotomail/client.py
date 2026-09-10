"""Generated operation bindings."""
from __future__ import annotations
from typing import Optional, Iterator, AsyncIterator
from . import models as M
from .transport import SyncTransport, AsyncTransport, Upload, EventFrame
class Robotomail(SyncTransport):
    def create_signup(self, body: M.SignupRequest) -> M.SignupResponse:
        """Create an account."""
        return self._request("POST", f"/signup", body=body, params=None)

    def check_slug_availability(self, params: Optional[M.CheckSlugAvailabilityParams] = None) -> M.SlugAvailability:
        """Check if an account slug is available."""
        return self._request("GET", f"/signup/check-slug", body=None, params=params)

    def get_account(self) -> M.AccountResponse:
        """Get account stats."""
        return self._request("GET", f"/account", body=None, params=None)

    def delete_account(self, body: M.DeleteAccountRequest) -> M.DeletedResponse:
        """Delete account permanently."""
        return self._request("DELETE", f"/account", body=body, params=None)

    def send_welcome_email(self) -> M.OkResponse:
        """Send the welcome email."""
        return self._request("POST", f"/account/welcome", body=None, params=None)

    def set_post_verify_target(self) -> M.SetPostVerifyTargetResponse:
        """Resolve post-verification target."""
        return self._request("POST", f"/account/post-verify-target", body=None, params=None)

    def list_api_keys(self) -> M.ApiKeyListResponse:
        """List API keys."""
        return self._request("GET", f"/api-keys", body=None, params=None)

    def create_api_key(self, body: M.CreateApiKeyRequest) -> M.CreateApiKeyResponse:
        """Create an API key."""
        return self._request("POST", f"/api-keys", body=body, params=None)

    def revoke_api_key(self, id: str) -> M.RevokedResponse:
        """Revoke an API key."""
        return self._request("DELETE", f"/api-keys/{self._segment(id)}", body=None, params=None)

    def list_mailboxes(self) -> M.MailboxListResponse:
        """List mailboxes."""
        return self._request("GET", f"/mailboxes", body=None, params=None)

    def create_mailbox(self, body: M.CreateMailboxRequest) -> M.MailboxResponse:
        """Create a mailbox."""
        return self._request("POST", f"/mailboxes", body=body, params=None)

    def get_mailbox(self, id: str) -> M.MailboxResponse:
        """Get a mailbox."""
        return self._request("GET", f"/mailboxes/{self._segment(id)}", body=None, params=None)

    def update_mailbox(self, id: str, body: M.UpdateMailboxRequest) -> M.MailboxResponse:
        """Update a mailbox."""
        return self._request("PATCH", f"/mailboxes/{self._segment(id)}", body=body, params=None)

    def delete_mailbox(self, id: str) -> M.DeletedResponse:
        """Delete a mailbox."""
        return self._request("DELETE", f"/mailboxes/{self._segment(id)}", body=None, params=None)

    def list_messages(self, id: str, params: Optional[M.ListMessagesParams] = None) -> M.MessageListResponse:
        """List messages in a mailbox."""
        return self._request("GET", f"/mailboxes/{self._segment(id)}/messages", body=None, params=params)

    def send_message(self, id: str, body: M.SendMessageRequest) -> M.MessageResponse:
        """Send an email from a mailbox."""
        return self._request("POST", f"/mailboxes/{self._segment(id)}/messages", body=body, params=None)

    def get_message(self, id: str, msg_id: str) -> M.MessageResponse:
        """Get a message."""
        return self._request("GET", f"/mailboxes/{self._segment(id)}/messages/{self._segment(msg_id)}", body=None, params=None)

    def list_threads(self, id: str) -> M.ThreadListResponse:
        """List threads in a mailbox."""
        return self._request("GET", f"/mailboxes/{self._segment(id)}/threads", body=None, params=None)

    def get_thread(self, id: str, tid: str) -> M.ThreadResponse:
        """Get a thread with its messages."""
        return self._request("GET", f"/mailboxes/{self._segment(id)}/threads/{self._segment(tid)}", body=None, params=None)

    def upload_attachment(self, file: Upload) -> M.AttachmentUploadResponse:
        """Upload an attachment."""
        return self._request("POST", f"/attachments", body=None, params=None, file=file)

    def download_attachment(self, id: str) -> M.AttachmentDownload:
        """Get an attachment download URL."""
        return self._request("GET", f"/attachments/{self._segment(id)}", body=None, params=None)

    def delete_attachment(self, id: str) -> M.DeletedResponse:
        """Delete an attachment."""
        return self._request("DELETE", f"/attachments/{self._segment(id)}", body=None, params=None)

    def list_domains(self) -> M.DomainListResponse:
        """List custom domains."""
        return self._request("GET", f"/domains", body=None, params=None)

    def create_domain(self, body: M.CreateDomainRequest) -> M.DomainCreatedResponse:
        """Add a custom domain."""
        return self._request("POST", f"/domains", body=body, params=None)

    def get_domain(self, id: str) -> M.DomainResponse:
        """Get a domain and its DNS records."""
        return self._request("GET", f"/domains/{self._segment(id)}", body=None, params=None)

    def delete_domain(self, id: str) -> M.DeletedResponse:
        """Delete a domain."""
        return self._request("DELETE", f"/domains/{self._segment(id)}", body=None, params=None)

    def verify_domain(self, id: str) -> M.DomainVerificationResponse:
        """Trigger domain verification."""
        return self._request("POST", f"/domains/{self._segment(id)}/verify", body=None, params=None)

    def list_webhooks(self) -> M.WebhookListResponse:
        """List webhooks."""
        return self._request("GET", f"/webhooks", body=None, params=None)

    def create_webhook(self, body: M.CreateWebhookRequest) -> M.WebhookCreatedResponse:
        """Create a webhook."""
        return self._request("POST", f"/webhooks", body=body, params=None)

    def get_webhook(self, id: str) -> M.WebhookResponse:
        """Get a webhook."""
        return self._request("GET", f"/webhooks/{self._segment(id)}", body=None, params=None)

    def update_webhook(self, id: str, body: M.UpdateWebhookRequest) -> M.WebhookResponse:
        """Update a webhook."""
        return self._request("PATCH", f"/webhooks/{self._segment(id)}", body=body, params=None)

    def delete_webhook(self, id: str) -> M.DeletedResponse:
        """Delete a webhook."""
        return self._request("DELETE", f"/webhooks/{self._segment(id)}", body=None, params=None)

    def list_webhook_deliveries(self, id: str) -> M.WebhookDeliveryListResponse:
        """List webhook deliveries."""
        return self._request("GET", f"/webhooks/{self._segment(id)}/deliveries", body=None, params=None)

    def stream_events(self, params: Optional[M.StreamEventsParams] = None) -> Iterator[EventFrame]:
        """Stream inbox events over SSE. Close the iterator when stopping early."""
        return self._stream(params)

    def list_suppressions(self) -> M.SuppressionListResponse:
        """List suppressed addresses."""
        return self._request("GET", f"/suppressions", body=None, params=None)

    def create_suppression(self, body: M.CreateSuppressionRequest) -> M.SuppressionResponse:
        """Suppress an address."""
        return self._request("POST", f"/suppressions", body=body, params=None)

    def delete_suppression(self, id: str) -> M.DeletedResponse:
        """Remove a suppression entry."""
        return self._request("DELETE", f"/suppressions/{self._segment(id)}", body=None, params=None)

    def create_upgrade_checkout(self, body: M.UpgradeRequest) -> M.UpgradeCheckoutResponse:
        """Start a plan upgrade."""
        return self._request("POST", f"/billing/upgrade", body=body, params=None)

    def resend_verification_email(self, body: M.ResendVerificationEmailRequest) -> M.OkResponse:
        """Resend the email verification link."""
        return self._request("POST", f"/auth/resend-verification", body=body, params=None)

    def submit_support_ticket(self, body: M.SupportRequest) -> M.OkResponse:
        """Contact support."""
        return self._request("POST", f"/support", body=body, params=None)

class AsyncRobotomail(AsyncTransport):
    async def create_signup(self, body: M.SignupRequest) -> M.SignupResponse:
        """Create an account."""
        return await self._request("POST", f"/signup", body=body, params=None)

    async def check_slug_availability(self, params: Optional[M.CheckSlugAvailabilityParams] = None) -> M.SlugAvailability:
        """Check if an account slug is available."""
        return await self._request("GET", f"/signup/check-slug", body=None, params=params)

    async def get_account(self) -> M.AccountResponse:
        """Get account stats."""
        return await self._request("GET", f"/account", body=None, params=None)

    async def delete_account(self, body: M.DeleteAccountRequest) -> M.DeletedResponse:
        """Delete account permanently."""
        return await self._request("DELETE", f"/account", body=body, params=None)

    async def send_welcome_email(self) -> M.OkResponse:
        """Send the welcome email."""
        return await self._request("POST", f"/account/welcome", body=None, params=None)

    async def set_post_verify_target(self) -> M.SetPostVerifyTargetResponse:
        """Resolve post-verification target."""
        return await self._request("POST", f"/account/post-verify-target", body=None, params=None)

    async def list_api_keys(self) -> M.ApiKeyListResponse:
        """List API keys."""
        return await self._request("GET", f"/api-keys", body=None, params=None)

    async def create_api_key(self, body: M.CreateApiKeyRequest) -> M.CreateApiKeyResponse:
        """Create an API key."""
        return await self._request("POST", f"/api-keys", body=body, params=None)

    async def revoke_api_key(self, id: str) -> M.RevokedResponse:
        """Revoke an API key."""
        return await self._request("DELETE", f"/api-keys/{self._segment(id)}", body=None, params=None)

    async def list_mailboxes(self) -> M.MailboxListResponse:
        """List mailboxes."""
        return await self._request("GET", f"/mailboxes", body=None, params=None)

    async def create_mailbox(self, body: M.CreateMailboxRequest) -> M.MailboxResponse:
        """Create a mailbox."""
        return await self._request("POST", f"/mailboxes", body=body, params=None)

    async def get_mailbox(self, id: str) -> M.MailboxResponse:
        """Get a mailbox."""
        return await self._request("GET", f"/mailboxes/{self._segment(id)}", body=None, params=None)

    async def update_mailbox(self, id: str, body: M.UpdateMailboxRequest) -> M.MailboxResponse:
        """Update a mailbox."""
        return await self._request("PATCH", f"/mailboxes/{self._segment(id)}", body=body, params=None)

    async def delete_mailbox(self, id: str) -> M.DeletedResponse:
        """Delete a mailbox."""
        return await self._request("DELETE", f"/mailboxes/{self._segment(id)}", body=None, params=None)

    async def list_messages(self, id: str, params: Optional[M.ListMessagesParams] = None) -> M.MessageListResponse:
        """List messages in a mailbox."""
        return await self._request("GET", f"/mailboxes/{self._segment(id)}/messages", body=None, params=params)

    async def send_message(self, id: str, body: M.SendMessageRequest) -> M.MessageResponse:
        """Send an email from a mailbox."""
        return await self._request("POST", f"/mailboxes/{self._segment(id)}/messages", body=body, params=None)

    async def get_message(self, id: str, msg_id: str) -> M.MessageResponse:
        """Get a message."""
        return await self._request("GET", f"/mailboxes/{self._segment(id)}/messages/{self._segment(msg_id)}", body=None, params=None)

    async def list_threads(self, id: str) -> M.ThreadListResponse:
        """List threads in a mailbox."""
        return await self._request("GET", f"/mailboxes/{self._segment(id)}/threads", body=None, params=None)

    async def get_thread(self, id: str, tid: str) -> M.ThreadResponse:
        """Get a thread with its messages."""
        return await self._request("GET", f"/mailboxes/{self._segment(id)}/threads/{self._segment(tid)}", body=None, params=None)

    async def upload_attachment(self, file: Upload) -> M.AttachmentUploadResponse:
        """Upload an attachment."""
        return await self._request("POST", f"/attachments", body=None, params=None, file=file)

    async def download_attachment(self, id: str) -> M.AttachmentDownload:
        """Get an attachment download URL."""
        return await self._request("GET", f"/attachments/{self._segment(id)}", body=None, params=None)

    async def delete_attachment(self, id: str) -> M.DeletedResponse:
        """Delete an attachment."""
        return await self._request("DELETE", f"/attachments/{self._segment(id)}", body=None, params=None)

    async def list_domains(self) -> M.DomainListResponse:
        """List custom domains."""
        return await self._request("GET", f"/domains", body=None, params=None)

    async def create_domain(self, body: M.CreateDomainRequest) -> M.DomainCreatedResponse:
        """Add a custom domain."""
        return await self._request("POST", f"/domains", body=body, params=None)

    async def get_domain(self, id: str) -> M.DomainResponse:
        """Get a domain and its DNS records."""
        return await self._request("GET", f"/domains/{self._segment(id)}", body=None, params=None)

    async def delete_domain(self, id: str) -> M.DeletedResponse:
        """Delete a domain."""
        return await self._request("DELETE", f"/domains/{self._segment(id)}", body=None, params=None)

    async def verify_domain(self, id: str) -> M.DomainVerificationResponse:
        """Trigger domain verification."""
        return await self._request("POST", f"/domains/{self._segment(id)}/verify", body=None, params=None)

    async def list_webhooks(self) -> M.WebhookListResponse:
        """List webhooks."""
        return await self._request("GET", f"/webhooks", body=None, params=None)

    async def create_webhook(self, body: M.CreateWebhookRequest) -> M.WebhookCreatedResponse:
        """Create a webhook."""
        return await self._request("POST", f"/webhooks", body=body, params=None)

    async def get_webhook(self, id: str) -> M.WebhookResponse:
        """Get a webhook."""
        return await self._request("GET", f"/webhooks/{self._segment(id)}", body=None, params=None)

    async def update_webhook(self, id: str, body: M.UpdateWebhookRequest) -> M.WebhookResponse:
        """Update a webhook."""
        return await self._request("PATCH", f"/webhooks/{self._segment(id)}", body=body, params=None)

    async def delete_webhook(self, id: str) -> M.DeletedResponse:
        """Delete a webhook."""
        return await self._request("DELETE", f"/webhooks/{self._segment(id)}", body=None, params=None)

    async def list_webhook_deliveries(self, id: str) -> M.WebhookDeliveryListResponse:
        """List webhook deliveries."""
        return await self._request("GET", f"/webhooks/{self._segment(id)}/deliveries", body=None, params=None)

    def stream_events(self, params: Optional[M.StreamEventsParams] = None) -> AsyncIterator[EventFrame]:
        """Stream inbox events over SSE. Close the iterator when stopping early."""
        return self._stream(params)

    async def list_suppressions(self) -> M.SuppressionListResponse:
        """List suppressed addresses."""
        return await self._request("GET", f"/suppressions", body=None, params=None)

    async def create_suppression(self, body: M.CreateSuppressionRequest) -> M.SuppressionResponse:
        """Suppress an address."""
        return await self._request("POST", f"/suppressions", body=body, params=None)

    async def delete_suppression(self, id: str) -> M.DeletedResponse:
        """Remove a suppression entry."""
        return await self._request("DELETE", f"/suppressions/{self._segment(id)}", body=None, params=None)

    async def create_upgrade_checkout(self, body: M.UpgradeRequest) -> M.UpgradeCheckoutResponse:
        """Start a plan upgrade."""
        return await self._request("POST", f"/billing/upgrade", body=body, params=None)

    async def resend_verification_email(self, body: M.ResendVerificationEmailRequest) -> M.OkResponse:
        """Resend the email verification link."""
        return await self._request("POST", f"/auth/resend-verification", body=body, params=None)

    async def submit_support_ticket(self, body: M.SupportRequest) -> M.OkResponse:
        """Contact support."""
        return await self._request("POST", f"/support", body=body, params=None)
