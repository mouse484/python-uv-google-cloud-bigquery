import time
from gpiozero import MCP3008
from google.cloud import bigquery
from datetime import datetime
from typing import TypedDict, List

client = bigquery.Client.from_service_account_json("it_bigquery_secret.json")
table_ref = client.dataset("yuto_test").table("test_table")

moisture_sensor = MCP3008(channel=0)

last_sent = time.time()


class MoistureData(TypedDict):
    time: str
    value: float


rows: List[MoistureData] = []

while True:
    raw_value = moisture_sensor.value
    timestamp = datetime.now().isoformat()

    rows.append({"time": timestamp, "value": raw_value})

    print(f"[{timestamp}] {raw_value:3f}")

    if time.time() - last_sent >= 60:
        errors = client.insert_rows_json(table_ref, rows)
        if errors == []:
            print("データ送信成功")
        else:
            print(f"データ送信失敗: {errors}")
        rows.clear()
        last_sent = time.time()

    time.sleep(1)
