# Acme Settlement Service 

## Purpose 

> Project built as part of take home test for ◼️◼️◼️◼️◼️ (name withheld)
>
> 💡This should not take longer than 4 hours to complete.

### The Problem
ACME Payments, Inc. needs settlement service to replace their paper and pencil bookkeeping. ACME processes payments on behalf of its customers, who are `Merchants`. When a `Customer` buys something from a `Merchant`, the funds are pulled from the `Customer`'s bank account to an `FBO Account` (think of this as a placeholder or virtual account) associated with the `Merchant`. The `Settlement` is the net balance for a `Merchant` on a given day. Unfortunately, the system was implemented in COBOL back in 1972 and runs on a valve tube computer. Expect the API to be slow at times. It also randomly fails when a bug flies into the mainframe and may return corrupt data. Be ready for some error handling. 

You will create a service that integrates with ACME Payments core API to retrieve data, process it and expose a settlement endpoint which we can use to determine the settlement amount for a merchant for a given date. 

### Requirements
* Must integrate with the ACME Payments API.
* The API is documented at:
  * [OpenAPI Schema JSON](/docs/acme_payments_api.json)
  * [OpenAPI Schema YAML](/docs/acme_payments_api.yaml)
* All the data is public and read only
* Must expose a REST endpoint with the settlement data
  * It must allow specifying a merchant and a date for the settlement
  > The date specified is the "settlement date". All transactions from the end of the previous business day through the end of business on the settlement date should be included in the settlement calculations.
* It must return a json payload with the settlement data, which must include the settlement amount (i.e. the net balance for the settlement period)
* Beyond these requirements, the design of this endpoint and what is included in the settlement response is part of the exercise

### Bonus
* Put together a simple summary view or UI that explains to an end user what is in a settlement.
* Think about what would be involved in running a full settlement system in production. You don't need to implement this but what orchestration is necessary to run this daily? When would the money actually move?

### What we're looking for
The ultimate goal of the take home exercise is for us to better understand your technical approach and problem-solving skills — what factors are you taking into account, how are you ensuring what you've implemented is correct, etc. Use this project as an opportunity to **showcase** your personality, skills, and opinions :)

All submissions will be carefully evaluated and we will review the implementation with you live to answer any questions about approach.

Best of luck and thank you for taking the time to work on this project!

## Installation and Running

The `backend` service can be built and run using Docker.

```bash
    docker build -t acme-backend .
```
Sources: [backend/README.md:10-11]()

```bash
    docker run -it -p 8000:8000 acme-backend
```

### Local Development 

To run and build is locally, please install [poetry](https://python-poetry.org/docs/).

```bash
    poetry run fastapi run src/main.py --port 8000
```

### Data Model Generation

The project utilizes `datamodel-code-generator` to generate Pydantic data models from an OpenAPI specification file. This tool helps in quickly creating Python classes that represent the API's data structures, which are then manually modified for refinement.

The generation process involves specifying the input OpenAPI YAML file, the desired output model type (Pydantic v2 `BaseModel`), and various formatting options.

```bash
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

### Incomplete Frontend

The project includes a `frontend` directory, but its `README.md` is minimal, and the `docker-compose.yml` is to combine frontend, backend when ready. The frontend component is currently undeveloped.