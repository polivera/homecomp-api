import logging
import os
import sys

import structlog


def configure_structlog(use_json: bool = False) -> None:
    """
    Configure structlog for the application.

    Args:
        use_json: If True, use JSON formatting (recommended for production).
                  If False, use console formatting (recommended for development).
    """
    # Structlog processors - shared across all handlers
    shared_processors = [
        structlog.contextvars.merge_contextvars,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
    ]

    if use_json:
        # Production: JSON formatting for Docker logs
        renderer = structlog.processors.JSONRenderer()
    else:
        # Development: Console formatting with colors
        renderer = structlog.dev.ConsoleRenderer()

    # Configure structlog to use stdlib logging as backend
    structlog.configure(
        processors=shared_processors
        + [
            structlog.stdlib.ProcessorFormatter.wrap_for_formatter,
        ],
        wrapper_class=structlog.make_filtering_bound_logger(logging.INFO),
        context_class=dict,
        logger_factory=structlog.stdlib.LoggerFactory(),
        cache_logger_on_first_use=True,
    )

    # Configure stdlib logging handlers
    logging.root.setLevel(logging.INFO)
    logging.root.handlers = []  # Clear any existing handlers

    # Console handler with formatting
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(
        structlog.stdlib.ProcessorFormatter(
            processor=renderer,
            foreign_pre_chain=shared_processors,
        )
    )
    logging.root.addHandler(console_handler)

    # Add Loki handler in development (sends structured data directly)
    if os.getenv("APP_ENV") != "prod":
        try:
            import logging_loki

            # Create a custom processor that returns the event dict as JSON string
            # This is needed because logging_loki expects a formatted message
            def json_message_processor(logger, method_name, event_dict):
                """Convert event dict to JSON string for Loki"""
                import json

                # Extract the message and include all structured data
                return json.dumps(event_dict, default=str)

            loki_handler = logging_loki.LokiHandler(
                url="http://localhost:3100/loki/api/v1/push",
                tags={"app": "homecomp-api", "env": "dev"},
                version="1",
            )
            # Use ProcessorFormatter with custom JSON processor
            loki_handler.setFormatter(
                structlog.stdlib.ProcessorFormatter(
                    processor=json_message_processor,
                    foreign_pre_chain=shared_processors,
                )
            )
            logging.root.addHandler(loki_handler)
        except ImportError:
            # python-logging-loki not installed (production)
            pass
