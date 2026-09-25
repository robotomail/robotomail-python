"""Official Robotomail SDK. API models use the public JSON field names."""
from .client import Robotomail, AsyncRobotomail
from .transport import ApiError, Upload, EventFrame, verify_webhook
from . import models

__version__ = "0.2.0"
__all__ = ["Robotomail", "AsyncRobotomail", "ApiError", "Upload", "EventFrame", "verify_webhook", "models"]
