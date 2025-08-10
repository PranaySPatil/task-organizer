# Lambda Deployment Steps

## For future Lambda code updates:

1. Update your `lambda_function.py`
2. Recreate the zip: `zip -r task_organizer.zip lambda_function.py`
3. Run `terraform apply`

Terraform will automatically detect and deploy your code changes.
