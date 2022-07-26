import { Stack, StackProps } from 'aws-cdk-lib';
import { Construct } from 'constructs';
import * as lambda from 'aws-cdk-lib/aws-lambda';
import * as s3 from 'aws-cdk-lib/aws-s3';
import * as iam from 'aws-cdk-lib/aws-iam';
import * as cdk from 'aws-cdk-lib';
import * as fs from 'fs';
import * as tasks from 'aws-cdk-lib/aws-stepfunctions-tasks';
import * as s3n from "aws-cdk-lib/aws-s3-notifications";
import * as sfn from 'aws-cdk-lib/aws-stepfunctions';
import { DynamoEventSource } from 'aws-cdk-lib/aws-lambda-event-sources';
import * as sns from 'aws-cdk-lib/aws-sns';
//import * as ssm from 'aws-cdk-lib/aws-ssm';
//
export class CdkAppStack extends Stack {
  
  constructor(scope: Construct, id: string, props?: StackProps) {
    super(scope, id, props);

/// 1. S3 생성 
    const resultBucket = new s3.Bucket(this, "resultBucket")

    const resultTopic = new sns.Topic(this, 'resultTopic');
//    const emailAddress = new ssm.CfnParameter(this, 'email-param');

/// 2. Lambda 생성
/// 단순히 람다 생성만 하는 것.
    const checkLambda_A = new lambda.Function(this, 'check-A', {
      code: new lambda.InlineCode(fs.readFileSync('lambda/ssb/checkA/lambda_function.py', {encoding: 'utf-8'})),
      handler: 'index.lambda_handler',
      timeout: cdk.Duration.seconds(30),
      runtime: lambda.Runtime.PYTHON_3_9,
      environment:{
        Bucket: resultBucket.bucketArn,
        Topic: resultTopic.topicArn
      }
    });
    const checkLambda_B = new lambda.Function(this, 'check-B', {
      code: new lambda.InlineCode(fs.readFileSync('lambda/ssb/checkB/lambda_function.py', {encoding: 'utf-8'})),
      handler: 'index.lambda_handler',
      timeout: cdk.Duration.seconds(30),
      runtime: lambda.Runtime.PYTHON_3_9,
      environment:{
        Bucket: resultBucket.bucketArn,
        Topic: resultTopic.topicArn
      }
    });
    const checkLambda_C = new lambda.Function(this, 'check-C', {
      code: new lambda.InlineCode(fs.readFileSync('lambda/ssb/checkC/lambda_function.py', {encoding: 'utf-8'})),
      handler: 'index.lambda_handler',
      timeout: cdk.Duration.seconds(30),
      runtime: lambda.Runtime.PYTHON_3_9,
      environment:{
        Bucket: resultBucket.bucketArn,
        Topic: resultTopic.topicArn
      }
    });
    const checkLambda_D = new lambda.Function(this, 'check-D', {
      code: new lambda.InlineCode(fs.readFileSync('lambda/ssb/checkD/lambda_function.py', {encoding: 'utf-8'})),
      handler: 'index.lambda_handler',
      timeout: cdk.Duration.seconds(30),
      runtime: lambda.Runtime.PYTHON_3_9,
      environment:{
        Bucket: resultBucket.bucketArn,
        Topic: resultTopic.topicArn
      }
    });
    const check_A = new tasks.LambdaInvoke(this, 'check_A', {
      lambdaFunction: checkLambda_A,
      // Lambda's result is in the attribute `Payload`
      outputPath: '$.Payload',
    });
    const check_B = new tasks.LambdaInvoke(this, 'check_B', {
      lambdaFunction: checkLambda_B,
      // Lambda's result is in the attribute `Payload`
      outputPath: '$.Payload',
    });
    const check_C = new tasks.LambdaInvoke(this, 'check_C', {
      lambdaFunction: checkLambda_C,
      // Lambda's result is in the attribute `Payload`
      outputPath: '$.Payload',
    });
    const check_D = new tasks.LambdaInvoke(this, 'check_D', {
      lambdaFunction: checkLambda_D,
      // Lambda's result is in the attribute `Payload`
      outputPath: '$.Payload',
    });
    
    const reportLambda = new lambda.Function(this, 'Create Report', {
      code: new lambda.InlineCode(fs.readFileSync('lambda/report/lambda_function.py', {encoding: 'utf-8'})),
      handler: 'index.lambda_handler',
      timeout: cdk.Duration.seconds(30),
      runtime: lambda.Runtime.PYTHON_3_9,
      environment:{
        Bucket: resultBucket.bucketArn
      }
    });
    const createReport = new tasks.LambdaInvoke(this, 'Create report', {
      lambdaFunction: reportLambda,
      // Lambda's result is in the attribute `Payload`
      outputPath: '$.Payload',
    });
    
    const parallel = new sfn.Parallel(this, 'All jobs')
          .branch(check_A) 
          .branch(check_B) 
          .branch(check_C) 
          .branch(check_D);
    
    const definition = parallel
      .next(createReport);

    const stateMachine = new sfn.StateMachine(this, 'SSB', {
      definition,
      timeout: cdk.Duration.minutes(20),
    });
    
    
    /*
    const stateMachine = new sfn.StateMachine(this, 'SSB', {
      definition: new tasks.LambdaInvoke(this, "Check-A", {
        lambdaFunction: checkLambda_A
      }).next(new sfn.Succeed(this, "Success"))
    });
    */
  }
}