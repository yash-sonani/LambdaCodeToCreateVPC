# LambdaCodeToCreateVPC
This Lambda Function read details from xls file present in S3 and create VPC.

Steps for implementation:

1.] Download all python files.

2.] Bundle the python files with external library [lxml](https://pypi.org/project/lxml/).

3.] To create lambda deployment package follow [aws documentation](https://docs.aws.amazon.com/lambda/latest/dg/lambda-python-how-to-create-deployment-package.html#python-package-dependencies).

4.] Upload zip file to lambda function.

5.] Create your own vpc_detial.xls file taking reference of [vpc_detail.xls](https://github.com/yash-sonani/LambdaCodeToCreateVPC/blob/master/vpc_detail.xls).

6.] Give lambda function S3 Read Access, increase execution time.

7.] Run lambda function.
