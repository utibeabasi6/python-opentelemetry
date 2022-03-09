from flask import Flask, render_template
import requests
import os
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
    resource=Resource.create({SERVICE_NAME: "ecommerce-web-service"})
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

products_api_url = os.environ.get("PRODUCTS_API_URL")

tracer = trace.get_tracer(__name__)

@app.get("/")
def index():
    with tracer.start_as_current_span("/ GET"): 
        with tracer.start_as_current_span("/ products"):  
            r = requests.get(products_api_url)
            items = [{"name":item[0], "price": int(item[1]), "image": item[2]} for item in r.json()["items"]]
        return render_template("index.html", items=items)


if __name__ == "__main__":
    app.run(debug=os.environ.get("DEBUG") or True, host="0.0.0.0", port=5001)