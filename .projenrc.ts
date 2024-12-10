import { awscdk } from 'projen';
import { ArrowParens } from 'projen/lib/javascript';

const cdkVersion = '2.172.0';
const devDeps = [
  '@aws-cdk/integ-tests-alpha',
  'cdk-nag',
  `@aws-cdk/aws-lambda-python-alpha@${cdkVersion}-alpha.0`
];

const project = new awscdk.AwsCdkConstructLibrary({
  author: 'Eddie Mattia',
  authorAddress: 'eddie@outerbounds.com',
  cdkVersion: cdkVersion,
  defaultReleaseBranch: 'main',
  jsiiVersion: '~5.5.0',
  name: 'cdk-mf',
  projenrcTs: true,
  repositoryUrl: 'https://github.com/emattia/cdk-mf.git',

  // deps: [],                /* Runtime dependencies of this module. */
  // description: undefined,  /* The description is just a string that helps people understand the purpose of the package. */
  devDeps: devDeps,            
  // packageName: undefined,  /* The "name" in package.json. */
  eslintOptions: {
    dirs: ['src', 'test'],
    prettier: true,
  },
  prettier: true,
  prettierOptions: {
    settings: {
      singleQuote: true,
      printWidth: 120,
      arrowParens: ArrowParens.AVOID,
    },
  },
});
project.synth();