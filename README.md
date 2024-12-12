# cdk-mf

This repository contains CDK code to deploy a lambda function that can send an event to the Argo event bus, which will trigger Metaflow flows. 

## Instructions

### Prerequisites
First, you need to have a valid Metaflow configuration file.

If you are not using the default configuration at `~/.metaflowconfig/config.json`, you can set the `METAFLOW_HOME` and `METAFLOW_PROFILE` environment variables to point to the desired configuration file.

### Manually running the CDK deployment

Before deploying the lambda function, you need to build the lambda function code which requires authenticating to the ECR Public registry.
```bash
aws ecr-public get-login-password --region us-east-1 | docker login --username AWS --password-stdin public.ecr.aws
npx aws-cdk deploy
```

This will deploy the lambda function and the necessary permissions to send events to the Argo event bus.

### Deploy the workflow

Write the flow definition in a file called `flow.py` and deploy it to Argo.
```python
from metaflow import FlowSpec, step, Parameter, trigger

@trigger(events=["cdk-mf-event"])
class F(FlowSpec):

	p = Parameter('p', default=1, type=int)

	@step
	def start(self):
		print(self.p)
		self.next(self.end)

	@step
	def end(self):
		pass

if __name__ == '__main__':
	F()
```

Now, deploy it:
```bash
python flow.py argo-workflows create
```

### Trigger a workflow

```bash
aws lambda invoke --function-name <YOUR_FUNCTION_NAME> res.json
```