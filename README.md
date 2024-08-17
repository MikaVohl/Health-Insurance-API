# Health Insurance API

The Health Insurance API retrieves and formats health insurance information from all providers within the United States. This API aims to simplify the painstaking process of finding an insurance plan by being a single source that displays all relevant information from every US health insurance provider.

This API is an extension of the CMS Marketplace API which aims to simplify the complex search parameters and outputs.

## Requirements
- Must have registered with CMS (Centers for Medicare & Medicaid Services) to receive an API key for the [Marketplace API](https://developer.cms.gov/marketplace-api/)
- Include a .env file in the root directory of the project with the following lines
  - ```API_KEY="your_actual_api_key_here"```
- Install the python packages listed in ```requirements.txt```

## How to run
- Run the Flask application by executing ```$ flask run```

## Endpoints

### `/plans`
- **Method**: POST
- **Description**: Lists available health plans based on the provided criteria.
- **Request Body**:
  ```json
  {
    "place": {
      "zipcode": "string",  // Required
      "state": "string",  // Required
      "countyfips": "string"  // Optional, will be fetched if not provided
    },
    "market": "string"  // Required
  }
  ```
  Any additional parameters supported by the CMS Marketplace API are supported
- **Responses**:
  - **200 OK**: Returns a list of health plans.
  - **400 Bad Request**: Returns an error message

### `/plan`
- **Method**: GET
- **Description**: Retrieves details of a specific health plan.
- **Query Parameters**:
  - `plan_id` (required): The ID of the plan.
  - `year` (optional): The year for which the plan details are requested.
- **Responses**:
  - **200 OK**: Returns the details of the specified health plan.

### `/issuers`
- **Method**: GET
- **Description**: Retrieves a list of issuers based on the provided criteria.
- **Query Parameters**:
  - `year` (optional): The year for which the issuers are requested.
  - `state` (optional): The state for which the issuers are requested.
  - `limit` (optional): The maximum number of issuers to return.
  - `offset` (optional): The offset for pagination.
- **Responses**:
  - **200 OK**: Returns a list of issuers.
