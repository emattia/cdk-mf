import * as path from 'path';
import * as python from '@aws-cdk/aws-lambda-python-alpha';
import * as cdk from 'aws-cdk-lib';
import * as lambda from 'aws-cdk-lib/aws-lambda';
import * as s3 from 'aws-cdk-lib/aws-s3';
import { Construct } from 'constructs';

export interface ICustomProps {
  readonly name: string;
  //   eventName: string;
  //   metaflowNamespace: string;
  //   outerboundsPerimeter: string;
}

export class EventLambdaConstruct extends Construct {
  constructor(scope: Construct, id: string, props: ICustomProps) {
    super(scope, id);
    const bucket = new s3.Bucket(this, 'MyFirstBucket', {
      bucketName: `${props.name.toLowerCase()}-${cdk.Names.uniqueId(this).toLowerCase()}`,
    });

    const pyFunc = new python.PythonFunction(this, 'EventLambdaFunction', {
      architecture: lambda.Architecture.X86_64,
      runtime: lambda.Runtime.PYTHON_3_12,
      entry: path.join(__dirname, 'lambda'),
      index: 'event_publisher.py',
    });

    bucket.grantReadWrite(pyFunc);
  }
}
