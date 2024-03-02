### credential ###
Aws profile: boonsri-prachya
Access key: AKIAU7JK7GMABSGDY64C
Secret access key: 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

### deploy cloudformation ###
aws cloudformation deploy --template-file storage/storage.main.yml --stack-name tm-etl-storage
aws cloudformation deploy --template-file control/control.main.yml --stack-name tm-etl-control --capabilities CAPABILITY_IAM
aws cloudformation deploy --template-file processing/processing.main.yml --stack-name tm-etl-processing --capabilities CAPABILITY_IAM
aws cloudformation deploy --template-file processing/workflow.yml --stack-name tm-etl-workflow --capabilities CAPABILITY_IAM
aws cloudformation deploy --template-file app/app.main.yml --stack-name tm-etl-app --capabilities CAPABILITY_IAM

### deploy lambda ###
aws s3api put-object --bucket  tm-staging-zone --key lamda/controller_package.zip --body controller_package.zip
aws s3api put-object --bucket  tm-staging-zone --key lambda/app_package.zip --body api_package.zip
