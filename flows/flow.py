from metaflow import FlowSpec, step, Parameter, trigger, JSONType

@trigger(events=["cdk-mf-event"])
class F(FlowSpec):

	p = Parameter('p', default=1, type=int)
	triggering_lambda_context = Parameter('context', default='{}', type=JSONType)

	@step 
	def start(self):
		print(self.p)
		print(self.triggering_lambda_context)
		self.next(self.end)

	@step
	def end(self):
		pass

if __name__ == '__main__':
	F()
