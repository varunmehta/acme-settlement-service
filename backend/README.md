## Backend 

### Installation

To run and build is locally, please install [poetry](https://python-poetry.org/docs/). Docker is the preferred way of running this app. The assumption is you have docker running on your local machine, and can use that to build and run your app.

#### Build 

```
    docker build -t acme-backend .
```

#### Run 

``` 
    docker run -it -p 8000:8000 acme-backend
```

### Using datamodel-codegen

Use [datamodel-code-generator](https://github.com/koxudaxi/datamodel-code-generator) to quickly generate the pydantic style data model for OpenAPI request file, then modify per your need
```
    datamodel-codegen \
        --input ../docs/acme_payments_api.yaml \
        --output-model-type pydantic_v2.BaseModel \
        --strict-nullable \
        --snake-case-field \
        --capitalize-enum-members \
        --reuse-model \
        --output acme-payments-api-client/acme-payments-api-client/models/models.py \
        --target-python-version 3.13
```