import * as s3 from 'aws-cdk-lib/aws-s3';
import * as cdk from 'aws-cdk-lib';
import * as iam from 'aws-cdk-lib/aws-iam';
import { Construct } from 'constructs';

export class HackerNewsMetadataConstruct extends Construct {
  public readonly bucket: s3.Bucket;

  constructor(scope: Construct, id: string) {
    super(scope, id);

    this.bucket = new s3.Bucket(this, 'HackerNewsMetadata', {
      removalPolicy: cdk.RemovalPolicy.RETAIN,
      versioned: false,
    });

    new cdk.CfnOutput(this, 'BucketName', {
      value: this.bucket.bucketName,
      description: 'The S3 bucket for Metaflow tasks',
    });
  }
}

export class OuterboundsIAMRoleConstruct extends Construct {
  constructor(scope: Construct, id: string, bucket: s3.Bucket, deploymentName: string, taskRoleArn: string) {
    super(scope, id);

    const bucketArn = bucket.bucketArn;
    const bucketArnWithWildcard = `${bucket.bucketArn}/*`;
    const outerboundsTaskBucketAccessRole = new iam.Role(this, 'OuterboundsTaskRole', {
      assumedBy: new iam.ArnPrincipal(taskRoleArn),
      inlinePolicies: {
        S3AccessPolicy: new iam.PolicyDocument({
          statements: [
            new iam.PolicyStatement({
              effect: iam.Effect.ALLOW,
              actions: ['s3:GetObject', 's3:ListBucket', 's3:PutObject', 's3:DeleteObject'],
              resources: [bucketArn, bucketArnWithWildcard],
            }),
          ],
        }),
      },
    });
    outerboundsTaskBucketAccessRole.assumeRolePolicy?.addStatements(
      new iam.PolicyStatement({
        effect: iam.Effect.ALLOW,
        actions: ['sts:AssumeRole', 'sts:SetSourceIdentity'],
        principals: [new iam.ArnPrincipal(taskRoleArn)],
      })
    );
    cdk.Tags.of(outerboundsTaskBucketAccessRole).add('outerbounds.com/accessible-by-deployment', deploymentName);
    new cdk.CfnOutput(this, 'taskRoleArn', {
        value: outerboundsTaskBucketAccessRole.roleArn,
        description: 'The IAM role for Outerbounds tasks to access the Hackernews metadata bucket.',
    }); 
  }
}
