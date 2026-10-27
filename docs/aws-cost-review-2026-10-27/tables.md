# Calculated comparison

Gross list-price estimates; workload assumptions, not capacity or invoice predictions.
30 days = 720 running hours; monthly storage/metric rates normalized over 730 hours.

| Option | 24h idle | 24h expected | 24h higher | 30d idle | 30d expected | 30d higher |
|---|---:|---:|---:|---:|---:|---:|
| 0 Current SSM baseline | $2.55 | $2.66 | $4.71 | $76.51 | $79.68 | $141.24 |
| 1 Hardened SSM host | $2.61 | $3.21 | $11.07 | $78.45 | $96.56 | $334.29 |
| 2 ALB HTTPS + same host | $3.40 | $4.01 | $12.24 | $101.86 | $120.54 | $369.21 |
| 3 Private ECS/RDS + one NAT | $7.45 | $8.37 | $23.12 | $209.51 | $237.16 | $681.81 |
| 3e Private ECS/RDS + six endpoints | $7.68 | $8.40 | $19.16 | $216.46 | $238.06 | $563.01 |
| 3r Two-AZ tasks/RDS + two NATs | $11.02 | $11.93 | $27.59 | $316.47 | $344.11 | $815.77 |
| 3re Two-AZ tasks/RDS + twelve endpoints | $11.49 | $12.20 | $23.87 | $330.62 | $352.21 | $704.17 |

## Optional streaming service only

| Duration/profile | GiB per broker | Two small brokers + storage | Three small brokers + storage | Serverless six partitions + bytes |
|---|---:|---:|---:|---:|---:|
| 24h idle | 20 | $2.32 | $3.48 | $18.26 |
| 24h expected | 20 | $2.32 | $3.48 | $19.44 |
| 24h higher | 160 | $3.24 | $4.86 | $42.61 |
| 720h idle | 20 | $69.61 | $104.41 | $547.94 |
| 720h expected | 20 | $69.61 | $104.41 | $583.07 |
| 720h higher | 160 | $97.23 | $145.84 | $1278.32 |
