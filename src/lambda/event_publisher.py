from aws_lambda_powertools import Logger, Tracer
from aws_lambda_powertools.event_handler import APIGatewayRestResolver
from aws_lambda_powertools.logging import correlation_paths
from aws_lambda_powertools.utilities.typing import LambdaContext
from aws_lambda_powertools.utilities.data_classes import event_source
from aws_lambda_powertools.utilities.data_classes.api_gateway_authorizer_event import (
    APIGatewayAuthorizerRequestEvent,
)

tracer = Tracer()
logger = Logger()
app = APIGatewayRestResolver()


@app.get("/pets")
@tracer.capture_method
def get_pets():
    return {"pets": []}


@logger.inject_lambda_context(correlation_id_path=correlation_paths.API_GATEWAY_REST)
@tracer.capture_lambda_handler
def handler(event: dict, context: LambdaContext) -> dict:
    # return app.resolve(event.raw_event, context)
    return {"statusCode": 200, "body": "Hello from Python Lambda!"}