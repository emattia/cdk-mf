import * as cdk from 'aws-cdk-lib';
import { App, Stack } from 'aws-cdk-lib';
import { MetaflowEventLambdaConstruct } from './lambda';
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

  const metaflowProfile = process.env.METAFLOW_PROFILE
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
  constructor(scope: App, id: string) {
    super(scope, id);

    const metaflowConfigStr = fetchMetaflowConfig();

    new MetaflowEventLambdaConstruct(this, 'MetaflowEventLambdaConstruct', {
      eventName: 'cdk-mf-event',
      lambdaRoleName: 'cdk-mf-event-lambda-role',
      metaflowConfigStr: metaflowConfigStr,
    });
  }
}

const app = new cdk.App();
new MetaflowEventLambdaStack(app, 'MetaflowEventLambdaStack');
app.synth();
