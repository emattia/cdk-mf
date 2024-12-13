from metaflow import FlowSpec, step, S3, current

ROLE='arn:aws:iam::730335446004:role/OuterboundsIAMRoleStack-d-OuterboundsIAMRoleConstru-zqce9YnidUcc'
FILE_PATH='s3://hackernewsmetadatastack-d-hackernewsmetadataconstr-vximpl675t6d/test.txt'

class TestS3Access(FlowSpec):

    @step
    def start(self):
        with S3(role=ROLE) as s3:
            s3.put(FILE_PATH, f'hello from {current.task_id}')
        self.next(self.end)

    @step
    def end(self):
        with S3(role=ROLE) as s3:
            print(s3.get(FILE_PATH).text)

if __name__ == '__main__':
    TestS3Access()