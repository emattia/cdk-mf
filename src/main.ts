import * as cdk from 'aws-cdk-lib';
import { App, Stack } from 'aws-cdk-lib';
import { EventLambdaConstruct } from './bucket';

class MyStack extends Stack {
  constructor(scope: App, id: string) {
    super(scope, id);

    new EventLambdaConstruct(this, 'EventLambdaConstruct', {
      name: 'cdkS3Bucket',
    });
  }
}

const app = new cdk.App();
new MyStack(app, 'MyStack');
app.synth();
