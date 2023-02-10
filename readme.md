# Features and Workflow

## Registration☑
As a user, you can connect to the service, which is available online, and register yourself using your email and specifying a password.

## CSV upload☑
After registering, you will be redirected to a page where you can upload a CSV file. The CSV file should contain the following columns:

## Models☑

Here we can see two models in `books_explorer` package one - for saving each file. The second one is used to process CSV

## Validation☑
During the upload process, the unique identifier for the book must be validated. If the identifier is not valid, the upload will be stopped and you will be informed that there is an error with that field in the CSV.

## File handling☑
During the upload process, the CSV file must be renamed to have a unique name (e.g. by appending an UUID) and uploaded to Amazon S3. The name and URL of the file must be saved in the application database.

## Content management☑
After the upload, you will be redirected to a page showing a table, which represents the contents of the CSV file. The page title will display the name of the uploaded CSV. If you are logged into the application, you will also be able to view all of the CSV files you have uploaded in the past, along with their content.

### Bonuses☑☑☑ 100% DONE

## External service integration✅: 

Every time a CSV file is uploaded, the application will send
a notification to an external service, performing a POST request to the following API
endpoint (we are using this service as an example, but any public place where we can see
the POSTs would do as well):

## Super bonus✅: 
Same as point above, but the POST request will include the S3 URL of the
uploaded file in the POST parameters

# Setup

1. Create a Django application
2. Run commands!

```bash

python -m venv venv
source/venv/bin/activate
pip install -r requirements.txt
python manage.py makemigrations 
python manage.py migrate 

```
3. Setup .env file and add your AWS credentials 

```python

AWS_ACCESS_KEY_ID=
AWS_SECRET_ACCESS_KEY=
AWS_STORAGE_BUCKET_NAME=
AWS_S3_ENDPOINT_URL=

```
4. Enjoy the product



## Taken time for this time was approximately 10h
