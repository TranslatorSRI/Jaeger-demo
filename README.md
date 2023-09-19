# Jaeger-demo
Examples on instrumenting python FAST-API servers.  


## Quick Start

#### 0. Install requirements
    $ python3.11 -m venv <venvs>/jaeger-demo
    $ source <venvs>/jaeger-demo/bin/activate
    $ pip install -r requirements.txt


#### 1. Run Jaeger

    docker-compose -f jaeger-docker-compose.yaml up

Test out Jaeger on [http://localhost:16686](http://localhost:16686)


#### 2. Run servers 




