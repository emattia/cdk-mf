import * as path from 'path';
import * as python from '@aws-cdk/aws-lambda-python-alpha';
import * as cdk from 'aws-cdk-lib';
import * as lambda from 'aws-cdk-lib/aws-lambda';
// import * as iam from 'aws-cdk-lib/aws-iam';
import * as s3 from 'aws-cdk-lib/aws-s3';
import { Construct } from 'constructs';

export interface ICustomProps {
  readonly eventName: string;
  readonly lambdaRoleName: string; // TODO: pass in string or role interface
  readonly metaflowConfigStr: string;
}

export class MetaflowEventLambdaConstruct extends Construct {
  constructor(scope: Construct, id: string, props: ICustomProps) {
    super(scope, id);
    const pyFunc = new python.PythonFunction(this, 'MetaflowEventLambdaFunction', {
      architecture: lambda.Architecture.X86_64,
      runtime: lambda.Runtime.PYTHON_3_12,
      entry: path.join(__dirname, 'lambda'),
      index: 'event_publisher.py',
      timeout: cdk.Duration.seconds(30),
      // role: new iam.Role(this, 'EventLambdaRole', {
      //   assumedBy: new iam.ServicePrincipal('lambda.amazonaws.com'),
      //   roleName: props.lambdaRoleName,
      // }),
      environment: {
        METAFLOW_EVENT_NAME: props.eventName,
        METAFLOW_CONFIG_STR: props.metaflowConfigStr,
      }
    });

    const bucket = new s3.Bucket(this, 'MetaflowEventLambdaBucket', {
      bucketName: `${cdk.Names.uniqueId(this).toLowerCase()}`,
    });
    bucket.grantReadWrite(pyFunc);
  }
}