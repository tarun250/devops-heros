# DynamoDB & RDS — Database Services

## DynamoDB (NoSQL)

**What it is:** a fully managed, serverless key-value / document database. Single-digit-millisecond reads at any scale, no servers to patch.

**NoSQL** — no fixed schema and no joins. Items in one table can have different attributes; you design the table around how you will query it.

| Concept | Meaning |
|---|---|
| **Table** | a collection of items |
| **Item** | one record (like a row), max 400 KB |
| **Attribute** | one field of an item (`name`, `price`) — string, number, binary, list, map… |
| **Partition key** | required; hashed to pick the partition that stores the item. Should spread traffic evenly (`userId`, not `country`) |
| **Sort key** | optional; orders items that share a partition key and allows range queries (`orderDate BETWEEN …`) |

Primary key = partition key alone, or partition key + sort key.

```text
Table: Orders
userId (PK)   orderDate (SK)   total   status
u-101         2026-10-01       499     SHIPPED
u-101         2026-10-05       120     PENDING
```

Extras: global/local secondary indexes for other query patterns, on-demand or provisioned capacity, TTL, Streams, point-in-time recovery.

**Use cases:** sessions, shopping carts, user profiles, IoT/event data, leaderboards, Terraform state locking.

## RDS (Relational)

**What it is:** managed relational databases. AWS handles provisioning, patching, backups and failover; you still own the schema and the SQL.

**Relational** — tables with a fixed schema, joins, ACID transactions, SQL.

**Supported engines:** PostgreSQL, MySQL, MariaDB, Oracle, SQL Server, Db2, plus **Aurora** (AWS's MySQL/PostgreSQL-compatible engine).

| Topic | Notes |
|---|---|
| **DB instance** | the database server: instance class (`db.t4g.micro`, `db.r7g.large`), storage (gp3/io2), and an endpoint to connect to |
| **Security** | run it in **private subnets** (DB subnet group); allow only the app's security group on 5432/3306; encryption at rest with KMS; TLS in transit; IAM DB auth; password in Secrets Manager |
| **Backups** | automated daily snapshots + transaction logs → point-in-time restore (retention 1–35 days); manual snapshots are kept until you delete them |
| **Multi-AZ** | synchronous standby in another AZ with automatic failover — for **availability**; the standby doesn't serve reads |
| **Read replicas** | asynchronous copies (same or another region) that serve **reads** — for **scaling**; can be promoted to standalone |

**Use cases:** e-commerce orders, banking/finance, CRM/ERP, any app that needs joins and transactions (like a backend's PostgreSQL in production).

## Which one?

| | DynamoDB | RDS |
|---|---|---|
| Data model | key-value / document | tables + relations |
| Schema | flexible | fixed |
| Queries | by key or index | any SQL, joins |
| Scaling | automatic, horizontal | bigger instance + read replicas |
| Operations | serverless | managed instances |
