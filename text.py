
import json
import os
import logging
import boto3
from botocore.exceptions import ClientError

# Configure logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# DynamoDB configuration
dynamodb = boto3.resource("dynamodb")
TABLE_NAME = os.environ["CUSTOMERS_TABLE"]
table = dynamodb.Table(TABLE_NAME)


def response(status_code, body):
    """Return an API Gateway-compatible JSON response."""
    return {
        "statusCode": status_code,
        "headers": {
            "Content-Type": "application/json"
        },
        "body": json.dumps(body, default=str)
    }


def lambda_handler(event, context):
    """
    Mock Account API
    Endpoint: GET /accounts/{customerId}

    Success response fields:
    customerId, plan, balance, lastPaymentDate, status

    Never returns:
    pin, phoneNumber, customerName
    """

    try:
        # Read customerId from API Gateway path parameters.
        # Also supports direct Lambda console testing.
        path_params = event.get("pathParameters") or {}

        customer_id = (
            path_params.get("customerId")
            or event.get("customerId")
            or ""
        )

        # Validate customer ID
        if not isinstance(customer_id, str) or not customer_id.strip():
            return response(400, {
                "error": "customerId is required"
            })

        customer_id = customer_id.strip()

        # Retrieve customer from DynamoDB
        result = table.get_item(
            Key={
                "customerId": customer_id
            }
        )

        customer = result.get("Item")

        # Customer does not exist
        if not customer:
            return response(404, {
                "error": "Customer not found",
                "customerId": customer_id
            })

        # Return only approved account information.
        # Do not expose PIN, phone number, or customer name.
        account = {
            "customerId": str(customer.get("customerId", "")),
            "plan": str(customer.get("plan", "")),
            "balance": float(customer.get("balance", 0)),
            "lastPaymentDate": str(
                customer.get("lastPaymentDate", "")
            ),
            "status": str(customer.get("status", ""))
        }

        return response(200, account)

    except ClientError as e:
        error_code = e.response.get(
            "Error", {}
        ).get("Code", "Unknown")

        # Log error metadata, not customer information.
        logger.error(
            "DynamoDB lookup failed. ErrorCode=%s",
            error_code
        )

        return response(500, {
            "error": "Internal server error"
        })

    except Exception as e:
        # Avoid logging full exception messages or request data.
        logger.error(
            "Unexpected error. ErrorType=%s",
            type(e).__name__
        )

        return response(500, {
            "error": "Internal server error"
        })
