from fastapi import  FastAPI
import httpx


APP = FastAPI(title="Service-A")



@APP.get("/hello")
async def root():
    async with httpx.AsyncClient() as client:
        # calls service b
        response_raw = await client.get("http://localhost:9092/make_calls")
        return response_raw.json()





def instrument(app):
    print("instrumenting app")
    # import libs

    from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
    from opentelemetry import trace    
    from opentelemetry.sdk.resources import SERVICE_NAME as telemetery_service_name_key, Resource
    from opentelemetry.sdk.trace import TracerProvider
    from opentelemetry.sdk.trace.export import BatchSpanProcessor
    from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter

    # add httpx instrumetation
    from opentelemetry.instrumentation.httpx import HTTPXClientInstrumentor

    service_name = "service-A"


    # set the service name for our trace provider 
    # this will tag every trace with the service name given
    trace.set_tracer_provider(
        TracerProvider(
            resource=Resource.create({telemetery_service_name_key: service_name})
        )
    )

    # create an exporter  to  jaeger
    
    jaeger_exporter = OTLPSpanExporter(endpoint="http://127.0.0.1:4318/v1/traces")
    # here we use the exporter to export each span in a trace
    trace.get_tracer_provider().add_span_processor(
        BatchSpanProcessor(jaeger_exporter)
    )
    
    # setup fast api instrumentation for our app 
    FastAPIInstrumentor.instrument_app(app, tracer_provider=trace)
                                    #    excluded_urls=
                                    #    "docs,openapi.json")

    HTTPXClientInstrumentor().instrument()



# call instrumentation code
instrument(app=APP)

if __name__=="__main__":
    import uvicorn
    uvicorn.run(app=APP, port=9093)