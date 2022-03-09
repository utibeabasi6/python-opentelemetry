from flask import Flask
import requests
import os
import sqlite3
from opentelemetry import trace
from opentelemetry.instrumentation.flask import FlaskInstrumentor
from opentelemetry.exporter.jaeger.thrift import JaegerExporter
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from opentelemetry.instrumentation.requests import RequestsInstrumentor
from opentelemetry.sdk.trace import TracerProvider

from opentelemetry.sdk.trace.export import (
    BatchSpanProcessor,
)

trace.set_tracer_provider(TracerProvider(
    resource=Resource.create({SERVICE_NAME: "ecommerce-products-service"})
))

app = Flask(__name__)

FlaskInstrumentor().instrument_app(app)
RequestsInstrumentor().instrument()

jaeger_exporter = JaegerExporter(
    agent_host_name="jaeger",
    agent_port=6831,
)

trace.get_tracer_provider().add_span_processor(
    BatchSpanProcessor(jaeger_exporter)
)

tracer = trace.get_tracer(__name__)

@app.get("/")
def index():
    with tracer.start_as_current_span("/ db"): 
        conn = sqlite3.connect("products.db")
        rows = conn.execute("SELECT * from products").fetchall()
        conn.commit()
        conn.close()
    return {"itemCount": len(rows), "items": rows}


if __name__ == "__main__":
    app.run(debug=os.environ.get("DEBUG") or True, host="0.0.0.0", port=5001)
