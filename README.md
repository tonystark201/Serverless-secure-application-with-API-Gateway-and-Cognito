# API Gateway and Cognito
## Cognito

+ __What is cognito__

> With Amazon Cognito, you can quickly and easily add user registration, login, and access control to your web and mobile applications. Amazon Cognito scales to millions of users and supports sign-in with social identity providers such as Apple, Facebook, Google, and Amazon, as well as enterprise identity providers, via SAML 2.0 and OpenID Connect.

+ __Pro and Cons__

>+ Pros
>   + **Secure Passwords**
>   + **OAuth, SAML, and More**
>   + **Simple Integration**
>   + **Quick Startup**
>+ Cons
>   + **Limited Configurability**
>   + **Better Setup Your Pool Correctly**
>   + **Integration with Outside Services**
>   + **Disaster Recovery**

+ __User Pool__

> A user pool is a user directory in Amazon Cognito. With a user pool, your users can sign in to your web or mobile app through Amazon Cognito. Your users can also sign in through social identity providers like Google, Facebook, Amazon, or Apple, and through SAML identity providers.

+ __Identity pools__

> Amazon Cognito identity pools (federated identities) enable you to create unique identities for your users and federate them with identity providers. With an identity pool, you can obtain temporary, limited-privilege AWS credentials to access other AWS services. 

## Terraform

__*All the infrastructure code is stored in the folder of `IaC`*__

### Steps

+ initialization: Initialize the terraform environment

  ```shell
  terraform init
  ```
+ Validation: Check the syntax error

  ```shell
  terraform validation
  ```
+ Plan: check the deploy plan

  ```shell
  terraform plan
  ```
+ Apply: deploy the infrastructure

  ```shell
  terraform apply
  ```
+ Destroy: Delete all the infrastructure

  ```shell
  terraform destroy
  ```

### Resource

The resources we need are listed below.

+ API Gateway

  We need a API Gateway to deal with the request. And We must config the integration and route.

+ Lambda

  We need a Lambda Handler to process the request event from the API Gateway.

+ S3

  We need a Bucket to store the code of the Lambda Function.
  
+ Cognito User Pool

  We need  the user pool to act as authorizer for API Gateway.

### Tips

You must provide your AWS key and secret, and give the value in the `terraform.tfvars` as below:

```shell
# provider
aws_region = "us-east-1"
aws_access_key = "xxxxxx"
aws_secret_key = "xxxxxx"
```
When the infrastructure build successfully, you will see the output as below.

```
Apply complete! Resources: 22 added, 0 changed, 0 destroyed.

Outputs:

api_gateway_endpoint = "https://090oq9xisg.execute-api.us-east-1.amazonaws.com/serverless_lambda_stage"
function_name = "api-backend-demo"
lambda_function_name = "api-backend-demo"
s3_bucket_name = "demo-rationally-eminently-epic-tapir"
```

## Github Action

We use the github action workflow to automate the deployment of code to the cloud. __*You can check and view the github action configuration in the folder of ".github" in this Repo*__

### Workflow

The workflow as below:

+ CI
  + Checkout the Code to the github runner
  + Lint the code, you can run flake8 or other tools to check the code format.
  + Run the unittest, you can use tox, pytets, unittest or some tools to implement the unit test of the code.
+ CD
  + Checkout the Code to the github runner
  + Configure AWS credentials
  + Generate zip package
  + Upload the zip file to S3.
  + Update Lambda Function Code

### Tips

1. You need to add your secret key in the Repo.(Click settings of the Repo you will find the place to add secret key)
2. We use Terraform build and run the minimum usable program, so the in the CI jobs, we just need to update the lambda handler code and update the file to AWS S3, then update the lambda function code.
3. You must update the `env` parameters in the `.github.yml` file.

## Demo Display

### Step1: Launch Hosted UI

__*We need to open Cognito's Hosted UI in order to register users.*__You can customize the style of the UI interface, such as CSS styles, etc. You can also use your existing user registration and login interfaces, such as pages built with React or Vue.js. 

Of course, as a demo project, we use the Hosted UI that comes with Cognito, which requires us to login to the AWS console and open the Cognito service. We can select manage user pools in the Cognito service manage console. And then we chose the app client setting, then we can launch the Host UI. 

+ The App client settings page.(__Launch Hosted UI__)

![image-20220707230000165](https://github.com/tonystark201/Serverless-secure-application-with-API-Gateway-and-Cognito/blob/main/img/image-20220707230000165.png)

### Step2: Register and Login user

According to the prompts on the Launched user login page, we need register users first. We can input the Email and Password, and after submitting the form, the system will send a verification code to our email.

+ Confirm Account

![image-20220707173756460](https://github.com/tonystark201/Serverless-secure-application-with-API-Gateway-and-Cognito/blob/main/img/image-20220707173756460.png)

+ The Code in the Email

![image-20220707173946575](https://github.com/tonystark201/Serverless-secure-application-with-API-Gateway-and-Cognito/blob/main/img/image-20220707173946575.png)

Then, we input the code in the form and confirm the account. Then we can use the email to login.
After we login, the URL will change to the callback url which is configured by us(You can found it in the `main.tf` file). The URL show as below.

```
https://tsztwozeroone/callback?code=306e77fe-c5d1-4aaa-9629-31734b7029c5
```

The `tsztwozeroone` is the Cognito Domain we configured. And the `code` in the URL is important and we need to use it to apply the id token and access token from Cognito.

### Step3: Apply the token

As we config the cognito client generate secret, we need to checkout the client_id and client_secret in the page of App client(`General settings `>> `App client`). My client id and secret as below.

```
client_id:     6vo4qadm0jp3e8kkk0c2d2l8im
client_secret: 1s3pth9n1trt2aejtarj81a4d707fjmrbenrnb08raiih8v37he5
```

__Then we need to retrieve the token, and the url and request parameters as below.__

+ Request URL: https://tsztwozeroone.auth.us-east-1.amazoncognito.com/oauth2/token
+ Request Parameters
  + grant_type: authorization_code
  + client_id: \<Your client id\>
  + code: \<Your user login code\>
  + redirect_uri: \<Your callback url\>
+ Headers
  + Authorization: Basic  \<Base64Encode(client_id:client_secret)\>
  + Content-Type: application/x-www-form-urlencoded

__For example:__

I use the postman to post my request to the Cognito identity server.

![image-20220707184219711](https://github.com/tonystark201/Serverless-secure-application-with-API-Gateway-and-Cognito/blob/main/img/image-20220707184219711.png)

+ The POST Request

```
POST https://tsztwozeroone.auth.us-east-1.amazoncognito.com/oauth2/token&
                       Content-Type='application/x-www-form-urlencoded'&
                       Authorization=Basic NnZvNHFhZG0wanAzZThra2swYzJkMmw4aW06MXMzcHRoOW4xdHJ0MmFlanRhcmo4MWE0ZDcwN2ZqbXJiZW5ybmIwOHJhaWloOHYzN2hlNQ==
                       
                       grant_type=authorization_code&
                       client_id=6vo4qadm0jp3e8kkk0c2d2l8im&
                       code=100f0672-b6d2-4d22-921b-d21179a00499&
                       redirect_uri=https://tsztwozeroone/callback
```

+ The Response

```
{
    "id_token": "eyJraWQiOiJjQnlwaE42cGFxZ3FHVTAyQk9Me...",
    "access_token": "eyJraWQiOiJkZmNsUkd2WFp3cW16K...",
    "refresh_token": "eyJjdHkiOiJKV1QiLCJlbmMiOiJBMj...",
    "expires_in": 3600,
    "token_type": "Bearer"
}
```

__We can decode the JWT id_token as below.__

+ Decoded Header

  ```json
  {
    "kid": "cByphN6paqgqGU02BOLyWMDMfsPLTX/hebRvC2G0VKs=",
    "alg": "RS256"
  }
  ```

+ Decoded Payload

  ```json
  {
    "at_hash": "9ggweZJ8oRpVKQ6SRCyv6g",
    "sub": "035c1d45-48c5-418e-9421-eddfa3eb145a",
    "email_verified": true,
    "iss": "https://cognito-idp.us-east-1.amazonaws.com/us-east-1_c2Z1Qxxx",
    "cognito:username": "035c1d45-48c5-418e-9421-eddfa3eb145a",
    "origin_jti": "9656305e-aa6c-4c71-8694-1f0ae3df0a43",
    "aud": "6vo4qadm0jp3e8kkk0c2d2l8im",
    "token_use": "id",
    "auth_time": 1657190158,
    "exp": 1657193758,
    "iat": 1657190159,
    "jti": "164fa925-57a5-4285-85d1-e87d8bd3b001",
    "email": "xxxxxx@xxxxxx.com"
  }
  ```

### Step4: Visit the API Gateway with access token

Since each Route of API Gateway is configured with an authorizer, we need to put the JWT in the request header so that it can be routed to the specified backend resource after authorization.

![image-20220707230954253](https://github.com/tonystark201/Serverless-secure-application-with-API-Gateway-and-Cognito/blob/main/img/image-20220707230954253.png)

The request header we configured that must take the Authorization Key (you can see how we configured it in `main.tf` file), so the request header is as follows.

![image-20220707184249819]([E:\GitTonyStark\RepoPublic\Serverless-secure-application-with-API-Gateway-and-Cognito\img\image-20220707184249819.png](https://github.com/tonystark201/Serverless-secure-application-with-API-Gateway-and-Cognito/blob/main/img/image-20220707184249819.png))

Then we can get the response successfully.

### Tips

1. __When we apply for a token, the Authorization in the request header must be the Base64 encoded string of client_id and client_secret.__
2. __The Cognito uses client_id as audience in the JWT by default, so when we configure the authorizer of API Gateway, we need to use client_id as audience.__



## Reference

+ [AWS Cognito official document](https://docs.aws.amazon.com/cognito/latest/developerguide/what-is-amazon-cognito.html)
+ [Pros and Cons of Using Amazon Cognito for User Authentication](https://www.gavant.com/library/pros-and-cons-of-using-amazon-cognito-for-user-authentication/)
+ [What is user pool in AWS cognito?](https://www.educative.io/answers/what-is-user-pool-in-aws-cognito)
+ [What is identity pool in AWS Cognito?](https://www.educative.io/answers/what-is-identity-pool-in-aws-cognito)
+ [Building fine-grained authorization using Amazon Cognito, API Gateway, and IAM](https://aws.amazon.com/cn/blogs/security/building-fine-grained-authorization-using-amazon-cognito-api-gateway-and-iam/)
+ [Token endpoint](https://docs.aws.amazon.com/cognito/latest/developerguide/token-endpoint.html)
