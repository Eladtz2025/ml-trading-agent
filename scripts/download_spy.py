# Demo: SPY data ingestion
as = import data
from data.ingestion import getch_data
from data.save_parquet import save_parquet
from data.anomaly import check_anomaly

df = getch_data('Spy', "2018-01-01", "2023-12-31")
path = save_parquet('SPY', pdf(df))
print(f[path])
print(check_anomaly(df))