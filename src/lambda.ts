import * as path from 'path';
import * as python from '@aws-cdk/aws-lambda-python-alpha';
import * as cdk from 'aws-cdk-lib';
import * as lambda from 'aws-cdk-lib/aws-lambda';
import * as iam from 'aws-cdk-lib/aws-iam';
import { Construct } from 'constructs';
import * as s3 from 'aws-cdk-lib/aws-s3';

export interface ICustomProps {
  readonly eventName: string;
  readonly lambdaRoleName: string;
  readonly metaflowConfigStr: string;
  readonly bucket: s3.IBucket; 
}

export class MetaflowEventLambdaConstruct extends Construct {
  constructor(scope: Construct, id: string, props: ICustomProps) {
    super(scope, id);

    const metaflowEventLambda = new python.PythonFunction(this, 'MetaflowEventLambdaFunction', {
      architecture: lambda.Architecture.X86_64,
      runtime: lambda.Runtime.PYTHON_3_12,
      entry: path.join(__dirname, 'lambda'),
      index: 'event_publisher.py',
      timeout: cdk.Duration.seconds(30),
      role: new iam.Role(this, 'EventLambdaRole', {
        assumedBy: new iam.ServicePrincipal('lambda.amazonaws.com'),
        roleName: props.lambdaRoleName,
        managedPolicies: [
          iam.ManagedPolicy.fromAwsManagedPolicyName('service-role/AWSLambdaBasicExecutionRole'),
        ],
      }),
      environment: {
        METAFLOW_EVENT_NAME: props.eventName,
        METAFLOW_CONFIG_STR: props.metaflowConfigStr,
        BUCKET_NAME: props.bucket.bucketName, 
      },
    });

    props.bucket.grantPut(metaflowEventLambda);
    props.bucket.grantRead(metaflowEventLambda);
  }
}
