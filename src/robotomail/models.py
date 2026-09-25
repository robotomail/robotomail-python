"""Generated API types. Request/response keys use the wire names."""
from __future__ import annotations
from typing import Any, Dict, List, Literal, Optional
from typing_extensions import TypedDict, Required, NotRequired
class ErrorBody(TypedDict):
    error: Required[str]

class EndpointNotFound(TypedDict):
    error: Required[str]
    code: Required[str]
    message: Required[str]
    resolution: Required[EndpointNotFoundResolution]

class UpgradeHint(TypedDict):
    browserUrl: Required[str]
    apiEndpoint: Required[UpgradeHintApiEndpoint]
    hint: Required[str]

class PaymentRequired(TypedDict):
    error: Required[str]
    payment_required: Required[bool]
    code: Required[str]
    upgrade: Required[UpgradeHint]

class TrialPaymentRequired(TypedDict):
    error: Required[str]
    payment_required: Required[bool]
    code: Required[Literal["TRIAL_RECIPIENT_LOCKED", "TRIAL_SEND_LIMIT", "TRIAL_EXPIRED"]]
    upgrade: Required[UpgradeHint]
    resetsAt: NotRequired[str]

class InboundLimitExceeded(TypedDict):
    error: Required[str]
    code: Required[Literal["INBOUND_LIMIT_EXCEEDED", "INBOUND_TRIAL_LIMIT_EXCEEDED"]]
    resource: Required[InboundLimitExceededResource]
    upgrade: Required[UpgradeHint]
    recovery: Required[Literal["reset", "upgrade"]]
    resetAt: NotRequired[str]

class PlanLimit(TypedDict):
    error: Required[str]
    upgrade: Required[str]

class Suspended(TypedDict):
    error: Required[str]
    suspended: Required[bool]
    reason: Required[str]

class DeletedResponse(TypedDict):
    deleted: Required[bool]

class RevokedResponse(TypedDict):
    revoked: Required[bool]

class SignupRequest(TypedDict):
    email: Required[str]
    password: Required[str]
    slug: Required[str]
    name: NotRequired[str]
    plan: NotRequired[str]
    period: NotRequired[str]
    turnstileToken: NotRequired[str]

class SignupResponse(TypedDict):
    user: Required[SignupResponseUser]
    api_key: Required[SignupResponseApiKey]
    mailbox: Required[SignupResponseMailbox]
    mailbox_limit: Required[int]
    daily_send_limit: Required[int]
    monthly_send_limit: Required[int]
    email_verified: Required[bool]
    next_steps: Required[SignupResponseNextSteps]

class SandboxTrial(TypedDict):
    isTrialUser: Required[bool]
    active: Required[bool]
    expired: Required[bool]
    exhausted: Required[bool]
    sendsUsed: Required[int]
    sendsRemaining: Required[int]
    sendCap: Required[int]
    receivesUsed: Required[int]
    receivesRemaining: Required[int]
    receiveCap: Required[int]
    expiresAt: Required[Optional[str]]
    startedAt: Required[Optional[str]]
    resetsAt: NotRequired[Optional[str]]

class Account(TypedDict):
    id: Required[str]
    email: Required[str]
    emailVerified: Required[bool]
    slug: Required[str]
    plan: Required[str]
    billingPeriod: Required[str]
    suspended: Required[bool]
    suspendedReason: Required[Optional[str]]
    suspendedAt: Required[Optional[str]]
    storageUsedBytes: Required[int]
    storageLimitBytes: Required[int]
    mailboxCount: Required[int]
    activeMailboxCount: Required[int]
    sentToday: Required[int]
    sentThisMonth: Required[int]
    receivedToday: Required[int]
    bouncedToday: Required[int]
    monthlyInboundCount: Required[int]
    monthlyInboundLimit: Required[int]
    monthlyInboundPercentage: Required[int]
    monthlyInboundResetAt: Required[str]
    overLimitMessageCount: Required[int]
    billingLinked: Required[bool]
    annualAvailability: Required[AccountAnnualAvailability]
    trial: Required[Optional[SandboxTrial]]

class AccountResponse(TypedDict):
    account: Required[Account]

class ApiKeySummary(TypedDict):
    id: Required[str]
    name: Required[Optional[str]]
    prefix: Required[Optional[str]]
    createdAt: Required[str]
    enabled: Required[bool]

class ApiKeyListResponse(TypedDict):
    keys: Required[List[ApiKeySummary]]

class CreateApiKeyRequest(TypedDict):
    name: NotRequired[str]
    mailboxIds: NotRequired[List[str]]

class CreateApiKeyResponse(TypedDict):
    key: Required[str]
    prefix: Required[str]
    scoped: Required[bool]

class Mailbox(TypedDict):
    id: Required[str]
    userId: Required[str]
    domainId: Required[Optional[str]]
    address: Required[str]
    fullAddress: Required[str]
    displayName: Required[Optional[str]]
    dailySendCount: Required[int]
    dailySendLimit: Required[int]
    monthlySendCount: Required[int]
    monthlySendLimit: Required[int]
    status: Required[Literal["ACTIVE", "PAUSED", "SUSPENDED"]]
    pausedByBilling: Required[bool]
    stalwartProvisioned: Required[bool]
    suspendedAt: Required[Optional[str]]
    suspendedReason: Required[Optional[str]]
    suspensionIncidentId: Required[Optional[str]]
    createdAt: Required[str]
    updatedAt: Required[str]
    receivedThisMonth: NotRequired[int]

class MailboxResponse(TypedDict):
    mailbox: Required[Mailbox]

class MailboxListResponse(TypedDict):
    mailboxes: Required[List[Mailbox]]

class CreateMailboxRequest(TypedDict):
    address: Required[str]
    domainId: NotRequired[str]
    displayName: NotRequired[str]

class UpdateMailboxRequest(TypedDict):
    displayName: NotRequired[str]
    status: NotRequired[Literal["ACTIVE", "PAUSED"]]

class SendMessageRequest(TypedDict):
    to: Required[List[str]]
    cc: NotRequired[List[str]]
    bcc: NotRequired[List[str]]
    subject: Required[str]
    bodyText: Required[str]
    bodyHtml: NotRequired[str]
    inReplyTo: NotRequired[str]
    attachments: NotRequired[List[str]]
    headers: NotRequired[Dict[str, str]]

class Message(TypedDict):
    id: Required[str]
    mailboxId: Required[str]
    direction: Required[Literal["INBOUND", "OUTBOUND"]]
    messageId: Required[str]
    inReplyTo: Required[Optional[str]]
    threadId: Required[Optional[str]]
    fromAddress: Required[str]
    toAddresses: Required[List[str]]
    ccAddresses: Required[List[str]]
    bccAddresses: Required[List[str]]
    subject: Required[str]
    bodyText: Required[str]
    bodyHtml: Required[Optional[str]]
    headers: Required[Dict[str, Any]]
    status: Required[Literal["QUEUED", "SENT", "DELIVERED", "BOUNCED", "COMPLAINED", "FAILED", "RECEIVED"]]
    externalMessageId: Required[Optional[str]]
    hasAttachments: Required[bool]
    attachmentsDropped: Required[bool]
    attachmentsDroppedReason: Required[Optional[str]]
    eventDispatchedAt: Required[Optional[str]]
    overLimit: Required[bool]
    overLimitReason: Required[Optional[Literal["MONTHLY", "TRIAL"]]]
    pendingSseEventData: Required[Any]
    createdAt: Required[str]
    attachments: NotRequired[List[Attachment]]

class MessageResponse(TypedDict):
    message: Required[Message]

class InboundUsage(TypedDict):
    current: Required[int]
    limit: Required[int]
    percentage: Required[int]
    reset_date: Required[str]
    status: Required[Literal["healthy", "approaching", "near", "limit_reached"]]

class ListMetadata(TypedDict):
    overLimitCount: Required[int]
    upgrade: Required[UpgradeHint]
    limitHint: NotRequired[InboundUsage]

class MessageListResponse(TypedDict):
    messages: Required[List[Message]]
    metadata: Required[ListMetadata]

class Attachment(TypedDict):
    id: Required[str]
    messageId: Required[Optional[str]]
    userId: Required[str]
    filename: Required[str]
    contentType: Required[str]
    sizeBytes: Required[int]
    r2Key: Required[str]
    contentId: Required[Optional[str]]
    createdAt: Required[str]

class AttachmentUploadResponse(TypedDict):
    id: Required[str]
    filename: Required[str]
    sizeBytes: Required[int]

class AttachmentDownload(TypedDict):
    id: Required[str]
    messageId: Required[Optional[str]]
    userId: Required[str]
    filename: Required[str]
    contentType: Required[str]
    sizeBytes: Required[int]
    r2Key: Required[str]
    contentId: Required[Optional[str]]
    createdAt: Required[str]
    url: Required[str]

class Thread(TypedDict):
    id: Required[str]
    mailboxId: Required[str]
    subject: Required[str]
    messageCount: Required[int]
    lastMessageAt: Required[str]
    participants: Required[List[str]]
    createdAt: Required[str]

class ThreadDetail(TypedDict):
    id: Required[str]
    mailboxId: Required[str]
    subject: Required[str]
    messageCount: Required[int]
    lastMessageAt: Required[str]
    participants: Required[List[str]]
    createdAt: Required[str]
    messages: Required[List[Message]]

class ThreadListResponse(TypedDict):
    threads: Required[List[Thread]]
    metadata: Required[ListMetadata]

class ThreadResponse(TypedDict):
    thread: Required[ThreadDetail]

class Domain(TypedDict):
    id: Required[str]
    userId: Required[str]
    domain: Required[str]
    status: Required[Literal["PENDING_VERIFICATION", "DNS_VERIFIED", "VERIFIED", "FAILED"]]
    mxVerified: Required[bool]
    spfVerified: Required[bool]
    dkimVerified: Required[bool]
    dmarcVerified: Required[bool]
    dkimPublicKey: Required[Optional[str]]
    dkimSelector: Required[Optional[str]]
    externalDomainId: Required[Optional[str]]
    stalwartProvisioned: Required[bool]
    createdAt: Required[str]
    updatedAt: Required[str]

class MxDnsRecord(TypedDict):
    type: Required[str]
    host: Required[str]
    value: Required[str]
    priority: Required[int]

class TxtDnsRecord(TypedDict):
    type: Required[str]
    host: Required[str]
    value: Required[str]

class DkimDnsRecord(TypedDict):
    type: Required[Literal["CNAME", "TXT"]]
    host: Required[str]
    value: Required[str]

class DnsRecords(TypedDict):
    mx: Required[MxDnsRecord]
    sendMx: Required[MxDnsRecord]
    spf: Required[TxtDnsRecord]
    dkim: Required[List[DkimDnsRecord]]
    dmarc: Required[TxtDnsRecord]

class CreateDomainRequest(TypedDict):
    domain: Required[str]

class DomainListResponse(TypedDict):
    domains: Required[List[Domain]]

class DomainCreatedResponse(TypedDict):
    domain: Required[Domain]
    dnsRecords: Required[DnsRecords]

class DomainResponse(TypedDict):
    domain: Required[Domain]
    dnsRecords: Required[Optional[DnsRecords]]

class DomainVerificationResponse(TypedDict):
    domain: Required[Domain]
    verification: Required[DomainVerificationResponseVerification]

class Webhook(TypedDict):
    id: Required[str]
    userId: Required[str]
    mailboxId: Required[Optional[str]]
    url: Required[str]
    events: Required[List[Literal["message.received", "message.sent", "message.delivered", "message.bounced", "message.complaint"]]]
    headers: Required[Optional[Dict[str, str]]]
    status: Required[Literal["ACTIVE", "PAUSED", "FAILED"]]
    failureCount: Required[int]
    lastTriggeredAt: Required[Optional[str]]
    createdAt: Required[str]
    updatedAt: Required[str]

class WebhookCreated(TypedDict):
    id: Required[str]
    userId: Required[str]
    mailboxId: Required[Optional[str]]
    url: Required[str]
    events: Required[List[Literal["message.received", "message.sent", "message.delivered", "message.bounced", "message.complaint"]]]
    headers: Required[Optional[Dict[str, str]]]
    status: Required[Literal["ACTIVE", "PAUSED", "FAILED"]]
    failureCount: Required[int]
    lastTriggeredAt: Required[Optional[str]]
    createdAt: Required[str]
    updatedAt: Required[str]
    secret: Required[str]

WebhookHeaders = Dict[str, str]
class CreateWebhookRequest(TypedDict):
    url: Required[str]
    mailboxId: NotRequired[str]
    events: Required[List[Literal["message.received", "message.sent", "message.delivered", "message.bounced", "message.complaint"]]]
    headers: NotRequired[WebhookHeaders]

class UpdateWebhookRequest(TypedDict):
    url: NotRequired[str]
    events: NotRequired[List[Literal["message.received", "message.sent", "message.delivered", "message.bounced", "message.complaint"]]]
    status: NotRequired[Literal["ACTIVE", "PAUSED"]]
    headers: NotRequired[Optional[WebhookHeaders]]

class WebhookListResponse(TypedDict):
    webhooks: Required[List[Webhook]]

class WebhookResponse(TypedDict):
    webhook: Required[Webhook]

class WebhookCreatedResponse(TypedDict):
    webhook: Required[WebhookCreated]

class WebhookDelivery(TypedDict):
    id: Required[str]
    event: Required[str]
    responseStatus: Required[Optional[int]]
    status: Required[Literal["PENDING", "DELIVERED", "FAILED"]]
    attempts: Required[int]
    nextRetryAt: Required[Optional[str]]
    createdAt: Required[str]

class WebhookDeliveryListResponse(TypedDict):
    deliveries: Required[List[WebhookDelivery]]

class SuppressionEntry(TypedDict):
    id: Required[str]
    email: Required[str]
    reason: Required[Literal["BOUNCE", "COMPLAINT", "MANUAL"]]
    createdAt: Required[str]

class CreateSuppressionRequest(TypedDict):
    email: Required[str]
    reason: NotRequired[Literal["BOUNCE", "COMPLAINT", "MANUAL"]]

class SuppressionListResponse(TypedDict):
    suppressions: Required[List[SuppressionEntry]]

class SuppressionResponse(TypedDict):
    suppression: Required[SuppressionEntry]

class UpgradeRequest(TypedDict):
    plan: NotRequired[Literal["developer", "growth", "scale"]]
    period: NotRequired[Literal["monthly", "annual"]]

class UpgradeCheckoutResponse(TypedDict):
    checkout_url: Required[str]
    expires_at: Required[Optional[int]]
    message: Required[str]

class SupportRequest(TypedDict):
    category: Required[Literal["technical", "billing", "account", "other"]]
    subject: Required[str]
    message: Required[str]

class OkResponse(TypedDict):
    ok: Required[bool]

class SlugAvailability(TypedDict):
    available: Required[bool]
    reason: NotRequired[str]

class CheckSlugAvailabilityParams(TypedDict):
    slug: Required[str]

class DeleteAccountRequest(TypedDict):
    confirm: Required[str]

class SetPostVerifyTargetResponse(TypedDict):
    target: Required[Literal["/dashboard?verified=true", "/onboarding"]]

class ListMessagesParams(TypedDict):
    direction: NotRequired[Literal["INBOUND", "OUTBOUND"]]
    threadId: NotRequired[str]
    since: NotRequired[str]
    limit: NotRequired[int]
    offset: NotRequired[int]

StreamEventsParams = TypedDict("StreamEventsParams", {"mailboxId": NotRequired[str], "events": NotRequired[str], "Last-Event-ID": NotRequired[str]})

class ResendVerificationEmailRequest(TypedDict):
    email: Required[str]

class EndpointNotFoundResolution(TypedDict):
    openapi: Required[str]
    docs: Required[str]
    endpoints: Required[str]
    commonEndpoints: Required[List[str]]

class UpgradeHintApiEndpoint(TypedDict):
    method: Required[str]
    path: Required[str]

class InboundLimitExceededResource(TypedDict):
    type: Required[Literal["message", "attachment"]]
    id: Required[str]

class SignupResponseUser(TypedDict):
    id: Required[str]
    email: Required[str]
    slug: Required[str]
    name: Required[str]
    plan: Required[str]
    platform_email: Required[str]

class SignupResponseApiKey(TypedDict):
    key: Required[str]
    prefix: Required[str]
    name: Required[str]

class SignupResponseMailbox(TypedDict):
    id: Required[str]
    address: Required[str]
    fullAddress: Required[str]
    status: Required[Literal["ACTIVE", "PAUSED", "SUSPENDED"]]

class SignupResponseNextSteps(TypedDict):
    verify_email: Required[str]
    add_payment: Required[str]
    add_domain: Required[str]
    send_email: Required[str]

class AccountAnnualAvailability(TypedDict):
    developer: Required[bool]
    growth: Required[bool]
    scale: Required[bool]

class DomainVerificationResponseVerification(TypedDict):
    mx: Required[bool]
    spf: Required[bool]
    dkim: Required[bool]
    dmarc: Required[bool]
    allVerified: Required[bool]
