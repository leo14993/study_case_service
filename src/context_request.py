from contextvars import ContextVar

context_request = ContextVar('context_request', default=None)
