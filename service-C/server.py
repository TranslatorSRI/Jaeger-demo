from fastapi import  FastAPI
import asyncio

APP = FastAPI(title="Service-C")



@APP.get("/slightly-verbose")
async def root():
    await asyncio.sleep(3)
    return {"message": "Hello World"}





def instrument(app):
    print("instrumenting app")
    # import libs

    from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
    from opentelemetry import trace
    from opentelemetry.trace.span import Span
    from opentelemetry.sdk.resources import SERVICE_NAME as telemetery_service_name_key, Resource
    from opentelemetry.sdk.trace import TracerProvider
    from opentelemetry.sdk.trace.export import BatchSpanProcessor
    from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter

    service_name = "service-C"


    # set the service name for our trace provider 
    # this will tag every trace with the service name given
    trace.set_tracer_provider(
        TracerProvider(
            resource=Resource.create({telemetery_service_name_key: service_name})
        )
    )

    # create an exporter    
    jaeger_exporter = OTLPSpanExporter(endpoint="http://127.0.0.1:4318/v1/traces")


    # here we use the exporter to export each span in a trace
    trace.get_tracer_provider().add_span_processor(
        BatchSpanProcessor(jaeger_exporter)
    )
    
    ## Using hooks to the instrumetor we can add attributes to our span 

    def server_request_hook(span: Span, scope: dict):
        if span and span.is_recording():
            span.set_attribute("custom_user_attribute_from_request_hook", "some-value")
        return span

    def client_request_hook(span: Span, scope: dict):
        if span and span.is_recording():
            span.set_attribute("custom_user_attribute_from_client_request_hook", "some-value")
        return span

    def client_response_hook(span: Span, message: dict):
        if span and span.is_recording():
            span.set_attribute("custom_user_attribute_from_response_hook", "some-value")
        return span

    ## Instrument the app
    FastAPIInstrumentor().instrument_app(app,
        server_request_hook=server_request_hook, 
        client_request_hook=client_request_hook, 
        client_response_hook=client_response_hook,
        excluded_urls="docs,openapi.json"
        )



    ##



# call instrumentation code
instrument(app=APP)

if __name__=="__main__":
    import uvicorn
    uvicorn.run(app=APP, port=9091)