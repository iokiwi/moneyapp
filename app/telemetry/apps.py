from django.apps import AppConfig
from opentelemetry import trace
from opentelemetry.sdk.resources import Resource, SERVICE_NAME
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor

from django.conf import settings


class TelemetryConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "telemetry"

    def ready(self) -> None:
        # return super().ready()

        resource = Resource(attributes={SERVICE_NAME: "moneyapp-dev"})
        trace.set_tracer_provider(TracerProvider(resource=resource))

        if settings.OTEL_EXPORTER == "collector":
            from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
            otlp_exporter = OTLPSpanExporter(
                endpoint="http://localhost:4317",
                # credentials=ChannelCredentials(credentials),
                # headers=(("metadata","value")),
            )
            span_processor = BatchSpanProcessor(otlp_exporter)
        elif settings.OTEL_EXPORTER == "console":
            from opentelemetry.sdk.trace.export import ConsoleSpanExporter
            span_processor = BatchSpanProcessor(ConsoleSpanExporter())

        trace.get_tracer_provider().add_span_processor(span_processor)
