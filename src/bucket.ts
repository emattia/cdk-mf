import * as lambda from 'aws-cdk-lib/aws-lambda';
import * as s3 from 'aws-cdk-lib/aws-s3';
// import * as python from '@aws-cdk/aws-lambda-python-alpha';
import { Construct } from 'constructs';
// import * as path from 'path';

export interface CustomProps {
  Name: string;
  //   EventName: string;
  //   MetaflowNamespace: string;
  //   OuterboundsPerimeter: string;
}

declare const myLambda: lambda.Function;

export class EventLambdaConstruct extends Construct {
  constructor(scope: Construct, id: string, props: CustomProps) {
    super(scope, id);
    const bucket = new s3.Bucket(this, 'MyFirstBucket', {
      bucketName: props.Name,
    });
    bucket.grantReadWrite(myLambda);

    // eslint-disable-next-line @typescript-eslint/no-unused-vars
    // const _pyFunc = new python.PythonFunction(
    //   this,
    //   'EventLambdaFunction',
    //   {
    //     architecture: lambda.Architecture.X86_64,
    //     runtime: lambda.Runtime.PYTHON_3_12,
    //     entry: path.join(__dirname, 'lambda'),
    //     index: 'event_publisher.py',
    //   }
    // );
  }
}
