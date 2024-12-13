import * as cdk from 'aws-cdk-lib';
import * as s3 from 'aws-cdk-lib/aws-s3';
import { App, Stack } from 'aws-cdk-lib';
import { MetaflowEventLambdaConstruct } from './lambda';
import { HackerNewsMetadataConstruct, OuterboundsIAMRoleConstruct } from './bucket';
import * as fs from 'fs';
import * as path from 'path';

function fetchMetaflowConfig(configDir: string = ''): string {
  if (!configDir) {
    configDir = path.resolve((process.env.METAFLOW_HOME || process.env.HOME) || '', '.metaflowconfig');
  }

  if (!fs.existsSync(configDir)) {
    throw new Error(`Configuration directory "${configDir}" does not exist.`);
  }

  const potentialConfigFiles = fs.readdirSync(configDir)
    .filter((file) => file.endsWith('.json'))
    .map((file) => path.join(configDir, file));

  if (potentialConfigFiles.length === 0) {
    throw new Error(`No JSON configuration files found in "${configDir}".`);
  }

  const metaflowProfile = process.env.METAFLOW_PROFILE;
  let chosenConfigFile = '';
  if (!metaflowProfile) {
    chosenConfigFile = path.join(configDir, 'config.json');
  } else {
    console.log(`Using profile: ${metaflowProfile}`);
    chosenConfigFile = path.join(configDir, `config_${metaflowProfile}.json`);
  }

  console.log(`Using configuration file: ${chosenConfigFile}`);
  let chosenConfigContents = '';
  try {
    chosenConfigContents = fs.readFileSync(chosenConfigFile, 'utf-8');
  } catch (error) {
    throw new Error(`Failed to read configuration file: ${chosenConfigFile}`);
  }

  try {
    JSON.parse(chosenConfigContents);
  } catch (error) {
    throw new Error(`Invalid JSON in configuration file: ${chosenConfigFile}`);
  }

  return chosenConfigContents;
}

class MetaflowEventLambdaStack extends Stack {
  constructor(scope: App, id: string, bucketArn: string) {
    super(scope, id);

    const metaflowConfigStr = fetchMetaflowConfig();

    new MetaflowEventLambdaConstruct(this, 'MetaflowEventLambdaConstruct', {
      eventName: 'cdk-mf-event',
      lambdaRoleName: 'cdk-mf-event-lambda-role',
      metaflowConfigStr: metaflowConfigStr,
      bucket: s3.Bucket.fromBucketArn(this, 'Bucket', bucketArn),
    });
  }
}

class HackerNewsMetadataStack extends Stack {
  public readonly metadataBucket: HackerNewsMetadataConstruct;

  constructor(scope: App, id: string) {
    super(scope, id);

    this.metadataBucket = new HackerNewsMetadataConstruct(this, 'HackerNewsMetadataConstruct');
  }
}

class OuterboundsIAMRoleStack extends Stack {
  constructor(scope: App, id: string, bucket: HackerNewsMetadataConstruct, deploymentName: string, taskRoleArn: string) {
    super(scope, id);
    new OuterboundsIAMRoleConstruct(this, 'OuterboundsIAMRoleConstruct', bucket.bucket, deploymentName, taskRoleArn);
  }
}

// Outerbounds props
const deploymentName = 'playground';
const taskRoleArn = 'arn:aws:iam::590183801547:role/obp-iquod5-task'

const app = new cdk.App();
const environment = app.node.tryGetContext('environment') || 'dev';

const hackerNewsMetadataStack = new HackerNewsMetadataStack(app, `HackerNewsMetadataStack-${environment}`);
new OuterboundsIAMRoleStack(app, `OuterboundsIAMRoleStack-${environment}`, hackerNewsMetadataStack.metadataBucket, deploymentName, taskRoleArn);
new MetaflowEventLambdaStack(app, `MetaflowEventLambdaStack-${environment}`, hackerNewsMetadataStack.metadataBucket.bucket.bucketArn);

app.synth();
