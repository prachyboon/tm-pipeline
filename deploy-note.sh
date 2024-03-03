### credential ###
Aws profile: boonsri-prachya
Access key: AKIAU7JK7GMABSGDY64C
Secret access key: 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

### deploy cloudformation ###
aws cloudformation deploy --template-file storage/storage.yml --stack-name tm-etl-storage
aws cloudformation deploy --template-file control/control.yml --stack-name tm-etl-control --capabilities CAPABILITY_IAM
aws cloudformation deploy --template-file processing/processing.yml --stack-name tm-etl-processing --capabilities CAPABILITY_IAM
aws cloudformation deploy --template-file processing/workflow.yml --stack-name tm-etl-workflow --capabilities CAPABILITY_IAM
aws cloudformation deploy --template-file app/app.yml --stack-name tm-etl-app --capabilities CAPABILITY_IAM

### deploy lambda ###
# cd to /src/${project}
zip controller_package.zip controller.py
aws s3api put-object --bucket  tm-staging-zone --key lamda/controller_package.zip --body controller_package.zip

zip api_package.zip api_caller.py
aws s3api put-object --bucket  tm-staging-zone --key lambda/app_package.zip --body api_package.zip

### upload daily data in case to trigger in landing zone
aws s3api put-object --bucket  tm-raw-zone --key table=dailycheckins/year=2024/month=3/day=3/dailycheckins.csv --body data/dailycheckins.csv

### upload glue script
# cd to /notebook/glue-script
aws s3api put-object --bucket  tm-staging-zone --key glue-script/tm-loader.py --body tm-loader.py
aws s3api put-object --bucket  tm-staging-zone --key glue-script/tm-tester.py --body tm-tester.py
aws s3api put-object --bucket  tm-staging-zone --key glue-script/tm-transformer.py --body tm-transformer.py