import httpx
import polars as pl
from metaflow import S3, FlowSpec, Parameter, current, step


class SetIDsFlow(FlowSpec):

    '''
    Run on a schedule to generate chunks of IDs to visit.
    Dump results to S3.
    '''

    s3_bucket = Parameter(
        "s3_bucket", help="S3 bucket for reading/writing state.", default="metaflow-r-s3"
    )
    s3_prefix = Parameter(
        "s3_prefix",
        help="Prefix within the S3 bucket where state & data are stored.",
        default="set-ids-workflow",
    )

    @step
    def start(self):
        with httpx.Client(timeout=10.0) as client:
            r = client.get("https://hacker-news.firebaseio.com/v0/maxitem.json")
            r.raise_for_status()
            self.max_item_id = int(r.text.strip())

        self.last_final = 0
        self.last_final_filename = f"{self.s3_prefix}/last_final.txt"

        with S3(run=self) as s3:
            objs = s3.info_many([self.last_final_filename], return_missing=True)
            if objs and objs[0].exists:
                obj = s3.get(self.last_final_filename)
                if obj and obj.downloaded:
                    content = obj.text.strip()
                    if content.isdigit():
                        self.last_final = int(content)

        self.next(self.generate_chunks)

    @step
    def generate_chunks(self):
        start_id = self.last_final
        end_id = self.max_item_id

        if end_id <= start_id:
            self.ids = []
        else:
            self.ids = list(range(start_id + 1, end_id + 1))

        chunk_size = 20
        chunks = []
        for i in range(0, len(self.ids), chunk_size):
            chunk = self.ids[i : i + chunk_size]
            chunks.append(
                {"chunk_start": chunk[0], "chunk_end": chunk[-1], "ids": chunk}
            )

        if chunks:
            df = pl.DataFrame(chunks)
        else:
            df = pl.DataFrame({"chunk_start": [], "chunk_end": [], "ids": []})

        output_filename = (
            f"{self.s3_prefix}/to_visit_{current.run_id}_{current.step_name}.parquet"
        )

        local_parquet = "to_visit.parquet"
        df.write_parquet(local_parquet)

        with S3(run=self) as s3:
            s3.put_files([(output_filename, local_parquet)])

        with open("last_final.txt", "w") as f:
            f.write(str(end_id))
        with S3(run=self) as s3:
            s3.put_files([(self.last_final_filename, "last_final.txt")])

        self.next(self.end)

    @step
    def end(self):
        """
        End step.
        """
        print("Set-IDs workflow completed.")


if __name__ == "__main__":
    SetIDsFlow()