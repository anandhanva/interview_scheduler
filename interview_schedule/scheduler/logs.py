import logging

class RequestIDFilter(logging.Filter):
    def filter(self, record):
        # Add custom attributes to the log record
        record.request_id = getattr(record, 'request_id', 'N/A')  # Default to 'N/A' if not provided
        record.class_name = getattr(record, 'class_name', 'N/A')  # Default for %(class)s
        return True

logger = logging.getLogger(__name__)