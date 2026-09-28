---
name: db-prisma-migration
description: Best practices for Prisma schema modeling, index optimization, transactions, and zero-downtime migrations.
author: "Prisma Community & ai-assist-bootstrap"
version: "1.0.0"
license: "MIT"
metadata:
  origin_repo: "https://github.com/prisma/prisma-examples"
  upstream_file: "databases/relational/README.md"
  source_type: "official-grounded"
  lineage: "curated"
  last_upstream_sync: "2026-09-26T23:40:00Z"
  customizations:
    - "Production zero-downtime expand-and-contract patterns"
    - "Strict lock_timeout recommendation"
    - "Concurrent index creation guidelines"
---

# Prisma Database & Migration Runbook

## When to Use
Use this skill when modifying `schema.prisma`, running migrations, designing relational models, or optimizing queries in PostgreSQL/MySQL applications using Prisma ORM.

---

## 1. Migration Command Rules

| Environment | Allowed Command | Strictly Forbidden |
| :--- | :--- | :--- |
| **Local Dev** | `npx prisma migrate dev` | `npx prisma db push` (destroys migration history) |
| **CI / Production** | `npx prisma migrate deploy` | `npx prisma migrate dev` (requires shadow DB & interactive prompts) |
| **Custom SQL Audit** | `npx prisma migrate dev --create-only` | Unreviewed direct schema pushes |

---

## 2. Zero-Downtime Expand-and-Contract Pattern

Never rename a column or drop a column in a single migration on a live database.

1. **Phase 1: Expand (Non-breaking)**
   - Add new column as nullable in `schema.prisma`.
   - Run `npx prisma migrate dev --name expand_column`.
   - Update application code to dual-write to both old and new columns.
   - Deploy application.

2. **Phase 2: Backfill**
   - Run a batched script to backfill historical data from old column to new column.

3. **Phase 3: Contract (Cleanup)**
   - Update application code to read and write exclusively from new column.
   - Deploy application.
   - Mark old column as deprecated, then remove it in a final migration:
     `npx prisma migrate dev --name drop_old_column`.

---

## 3. High-Performance Indexing & Concurrent Locks

In PostgreSQL, standard `CREATE INDEX` acquires a share lock that blocks writes:
- For large tables, generate the migration with `--create-only`:
  ```bash
  npx prisma migrate dev --create-only --name add_index_concurrently
  ```
- Edit the generated `migration.sql` to remove the default `CREATE INDEX` and use:
  ```sql
  -- Disable Prisma's transactional migration wrapper if required by PostgreSQL
  CREATE INDEX CONCURRENTLY "idx_users_email" ON "User"("email");
  ```
- Always configure a low session `lock_timeout` (e.g. 5s) before heavy migrations:
  ```sql
  SET lock_timeout = '5s';
  ```

---

## 4. Query Optimization & Transactions

- **Avoid N+1 queries**: Always use `include` or `select` judiciously; avoid looping over async Prisma queries.
- **Interactive Transactions**: Keep transactions short and focused to avoid connection starvation:
  ```typescript
  await prisma.$transaction(async (tx) => {
    const sender = await tx.account.update({
      where: { id: senderId },
      data: { balance: { decrement: amount } },
    });
    if (sender.balance < 0) throw new Error('Insufficient funds');
    await tx.account.update({
      where: { id: receiverId },
      data: { balance: { increment: amount } },
    });
  }, {
    maxWait: 5000, // 5s max wait to acquire connection
    timeout: 10000, // 10s max execution time
  });
  ```

