from fastapi import  FastAPI


APP = FastAPI(title="Service-D")



@APP.get("/hello")
async def root():
    return {"message": "Hello World"}





def instrument(app):
    print("instrumenting app")
    # import libs

    from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
    from opentelemetry import trace    
    from opentelemetry.sdk.resources import SERVICE_NAME as telemetery_service_name_key, Resource
    from opentelemetry.sdk.trace import TracerProvider
    from opentelemetry.sdk.trace.export import BatchSpanProcessor
    from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter

    service_name = "service-D"


    # set the service name for our trace provider 
    # this will tag every trace with the service name given
    trace.set_tracer_provider(
        TracerProvider(
            resource=Resource.create({telemetery_service_name_key: service_name})
        )
    )

    # create an exporter
    # jaeger_exporter = JaegerExporter(
    #     agent_host_name="localhost",
    #     agent_port=6831,
    # )
    jaeger_exporter = OTLPSpanExporter(endpoint="http://127.0.0.1:4318/v1/traces")
    # here we use the exporter to export each span in a trace
    trace.get_tracer_provider().add_span_processor(
        BatchSpanProcessor(jaeger_exporter)
    )
    
    # setup fast api instrumentation for our app 
    FastAPIInstrumentor.instrument_app(app, tracer_provider=trace)
                                    #    excluded_urls=
                                    #    "docs,openapi.json")
    



# call instrumentation code
instrument(app=APP)

if __name__=="__main__":
    import uvicorn
    uvicorn.run(app=APP, port=9090)