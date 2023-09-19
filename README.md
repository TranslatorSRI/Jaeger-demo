# Jaeger-demo
Examples on instrumenting python FAST-API servers.  


## Quick Start

#### 0. Install requirements
    $ python3.11 -m venv <venvs>/jaeger-demo
    $ source <venvs>/jaeger-demo/bin/activate
    $ pip install -r requirements.txt


#### 1. Run Jaeger

    docker-compose -f jaeger-docker-compose.yaml up

Test out Jaeger UI on [http://localhost:16686](http://localhost:16686)


#### 2. Run servers 

    python service-A server.py
    python service-B server.py
    python service-C server.py
    python service-D server.py



#### 3. Architeture

<img width="508" alt="image" src="https://github.com/helxplatform/roger/assets/45075777/0e2a2e96-2ed4-4411-846e-11aea84c2201">


