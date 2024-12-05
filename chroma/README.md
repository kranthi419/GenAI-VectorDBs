Learn more about Chroma at [trychroma.com](https://trychroma.com).

Performance:
https://docs.trychroma.com/deployment/performance#memory-and-collection-size

Also see:

Instance Type | System RAM | Approx. Max Collection Size | Mean Latency (insert) | 99.9% Latency (insert) | Mean Latency (query) | 99.9% Latency (query) | Monthly Cost |
---------------|------------|-----------------------------|------------------------|-------------------------|-----------------------|------------------------|--------------|
t3.small      | 2 GB       | 250,000                    | 55ms                  | 250ms                  | 22ms                 | 72ms                  | $15.936      |
t3.medium     | 4 GB       | 700,000                    | 37ms                  | 120ms                  | 14ms                 | 41ms                  | $31.072      |
t3.large      | 8 GB       | 1,700,000                  | 30ms                  | 100ms                  | 13ms                 | 35ms                  | $61.344      |
t3.xlarge     | 16 GB      | 3,600,000                  | 30ms                  | 100ms                  | 13ms                 | 30ms                  | $121.888     |
t3.2xlarge    | 32 GB      | 7,500,000                  | 30ms                  | 100ms                  | 13ms                 | 30ms                  | $242.976     |
r7i.2xlarge   | 64 GB      | 15,000,000                 | 13ms                  | 50ms                   | 7ms                  | 13ms                  | $386.944     |

Deploying Chroma on a system with less than 2GB of RAM is not recommended.

Note that the latency figures in this table are for small collections. Latency increases as collections grow: see [Latency and collection size](https://docs.trychroma.com/deployment/performance#latency-and-collection-size) below for a full analysis.

For more information on performance, see the [Chroma documentation](https://docs.trychroma.com/deployment/performance).

## Disable Telemetry:
Check out the [Chroma documentation](https://docs.trychroma.com/telemetry) for instructions on how to disable telemetry.
