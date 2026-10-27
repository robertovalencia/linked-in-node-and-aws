#!/usr/bin/env python3
"""Credential-free Docker TLS PostgreSQL / owned-role integration drill. Never calls AWS."""
import argparse
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import secrets
import subprocess
import tempfile
import time

ROOT = Path(__file__).resolve().parents[1]


def main(report: Path) -> None:
    checks = []
    container = f"marketplace-ecs-tls-test-{os.getpid()}"
    def run(arguments, *, env=None, check=True):
        return subprocess.run(arguments, cwd=ROOT / "backend", env=env, check=check, capture_output=True, text=True)
    def passed(name):
        checks.append({"name": name, "status": "PASS"})
    with tempfile.TemporaryDirectory(prefix="marketplace-pg-tls-") as temporary:
        fixtures = Path(temporary)
        run(["openssl", "req", "-x509", "-newkey", "rsa:2048", "-nodes", "-days", "1", "-subj", "/CN=localhost", "-addext", "subjectAltName=DNS:localhost,IP:127.0.0.1", "-keyout", str(fixtures / "server.key"), "-out", str(fixtures / "server.crt")])
        (fixtures / "pg_hba.conf").write_text("local all all trust\nhostssl all all 0.0.0.0/0 scram-sha-256\nhostnossl all all 0.0.0.0/0 reject\n")
        admin_password = secrets.token_hex(32)
        environment = {**os.environ, "POSTGRES_PASSWORD": admin_password}
        try:
            run(["docker", "run", "-d", "--name", container, "--memory", "384m", "--tmpfs", "/var/lib/postgresql/data:rw,nosuid,size=256m", "-p", "127.0.0.1::5432", "-e", "POSTGRES_PASSWORD", "-e", "POSTGRES_USER=marketplace_admin", "-v", f"{fixtures}:/fixtures:ro", "--entrypoint", "/bin/sh", "postgres:17.6-alpine@sha256:ef257d85f76e48da1c64832459b59fcaba1a4dac97bf5d7450c77753542eee94", "-c", "cp /fixtures/server.* /tmp/; chown postgres:postgres /tmp/server.*; chmod 600 /tmp/server.key; exec docker-entrypoint.sh postgres -c ssl=on -c ssl_cert_file=/tmp/server.crt -c ssl_key_file=/tmp/server.key -c hba_file=/fixtures/pg_hba.conf -c log_min_error_statement=panic"], env=environment)
            port = run(["docker", "port", container, "5432/tcp"]).stdout.strip().rsplit(":", 1)[1]
            for attempt in range(60):
                if run(["docker", "exec", container, "pg_isready", "-U", "marketplace_admin"], check=False).returncode == 0:
                    break
                time.sleep(1)
            else:
                raise RuntimeError("Local TLS PostgreSQL did not become ready")
            run(["npm", "run", "build"])
            environment = {**os.environ, "DB_HOST": "127.0.0.1", "DB_PORT": port, "DB_NAME": "postgres", "DB_USER": "marketplace_admin", "DB_PASSWORD": admin_password, "DB_SSL": "true", "DB_SSL_CA_FILE": str(fixtures / "server.crt"), "DEPLOYMENT_MODE": "aws-ecs"}
            environment.pop("DB_URL", None)
            environment.pop("DB_SSL_CA", None)
            for service in ("identity", "catalog", "inquiries", "notifications"):
                environment[f"{service.upper()}_DB_PASSWORD"] = secrets.token_hex(32)
            for name in ("bootstrap_initial", "bootstrap_idempotent_rerun"):
                run(["node", "dist/operations/database-bootstrap.js"], env=environment)
                passed(name)
            verification = r"""
import { Client } from 'pg';
import { databaseOptions } from './dist/common/connections.js';
import { Database } from './dist/common/database.js';
const services=['identity','catalog','inquiries','notifications'];
const results=[];
const connect=async(extra={})=>{ const c=new Client({...databaseOptions(),...extra});try { await c.connect();return c; } catch(e){await c.end();throw e;} };
for (const service of services) {
  Object.assign(process.env,{SERVICE:service,DB_NAME:service,DB_USER:service,DB_PASSWORD:process.env[service.toUpperCase()+'_DB_PASSWORD']});
  const client=await connect();
  const row=(await client.query('SELECT current_user AS owner, ssl FROM pg_stat_ssl WHERE pid=pg_backend_pid()')).rows[0];
  if(row.owner!==service || row.ssl!==true)throw Error('Ownership or TLS failed');
  await client.end();results.push({name:'verified_tls_owned_'+service,status:'PASS'});
  const db=new Database();await db.onModuleInit();await db.onModuleInit();await db.onModuleDestroy();
  results.push({name:'checksummed_migrations_rerun_'+service,status:'PASS'});
  for (const other of services.filter(x=>x!==service)) {
    let denied=false;try{const forbidden=await connect({database:other});await forbidden.end();}catch(e){if(e.code==='42501')denied=true;else throw e;}
    if(!denied)throw Error('Cross-database connect unexpectedly permitted');
    results.push({name:'deny_'+service+'_to_'+other,status:'PASS'});
  }
}
for (const [name,options] of [
 ['plaintext',{ssl:false}],
 ['wrong_ca',{ssl:{rejectUnauthorized:true}}],
 ['wrong_hostname',{ssl:{...databaseOptions().ssl,servername:'wrong.internal'}}],
]) {
 let denied=false;try{const c=await connect(options);await c.end();}catch{denied=true;}
 if(!denied)throw Error('TLS negative unexpectedly connected');
 results.push({name:'deny_'+name,status:'PASS'});
}

// Rebuild delivery metadata after permanent broker loss without losing original identities.
Object.assign(process.env,{SERVICE:'inquiries',DB_NAME:'inquiries',DB_USER:'inquiries',DB_PASSWORD:process.env.INQUIRIES_DB_PASSWORD,REPLAY_OUTBOX_CONFIRM:'replay-all-published-events'});
const { replayPublishedOutbox }=await import('./dist/operations/replay-outbox.js');
const inquiry='00000000-0000-4000-8000-000000000001',event='00000000-0000-4000-8000-000000000002';
let client=await connect();
await client.query("INSERT INTO inquiries(id,provider_id,provider_email,provider_name,client_email,client_name,subject,message,budget,client_type,idempotency_key,request_hash) VALUES($1,'provider','provider@test','Provider','client@test','Client','Recovery','Recovery fixture',100,'COMPANY','recovery-fixture','hash')",[inquiry]);
await client.query("INSERT INTO outbox(event_id,inquiry_id,payload,published_at) VALUES($1,$2,$3,now())",[event,inquiry,JSON.stringify({eventId:event,inquiryId:inquiry,subject:'Recovery'})]);
await client.end();
if(await replayPublishedOutbox()!==1)throw Error('Published backlog did not reset');
if(await replayPublishedOutbox()!==0)throw Error('Replay metadata reset is not idempotent');
client=await connect();const replay=(await client.query('SELECT event_id,payload,published_at FROM outbox WHERE event_id=$1',[event])).rows[0];await client.end();
if(replay.event_id!==event||replay.payload.eventId!==event||replay.published_at!==null)throw Error('Replay altered event identity or payload');
results.push({name:'broker_loss_outbox_replay_preserves_identity',status:'PASS'},{name:'replay_metadata_reset_idempotent',status:'PASS'});
Object.assign(process.env,{SERVICE:'notifications',DB_NAME:'notifications',DB_USER:'notifications',DB_PASSWORD:process.env.NOTIFICATIONS_DB_PASSWORD});
client=await connect();
for(let n=0;n<2;n++)await client.query("INSERT INTO notifications(id,event_id,inquiry_id,recipient_email,message,created_at) VALUES(gen_random_uuid(),$1,$2,'provider@test','Recovery',now()) ON CONFLICT(event_id) DO NOTHING",[event,inquiry]);
if(Number((await client.query('SELECT count(*) FROM notifications WHERE event_id=$1',[event])).rows[0].count)!==1)throw Error('Replayed event duplicated durable notification');await client.end();
results.push({name:'replayed_event_has_one_durable_notification_effect',status:'PASS'});

console.log(JSON.stringify(results));
"""
            results = run(["node", "--input-type=module", "-e", verification], env=environment)
            checks.extend(json.loads(results.stdout))
            # The CLI must redact raw SQL and passwords even when ownership checks fail.
            fail_env = {**environment, "DB_USER": "identity", "DB_NAME": "identity", "DB_PASSWORD": environment["IDENTITY_DB_PASSWORD"]}
            failed = run(["node", "dist/operations/database-bootstrap.js"], env=fail_env, check=False)
            if failed.returncode == 0 or "Database bootstrap failed" not in failed.stderr or any(value in failed.stderr for key, value in fail_env.items() if key.endswith("PASSWORD")):
                raise RuntimeError("Bootstrap failure was not safely redacted")
            passed("bootstrap_failure_redacts_sql_and_passwords")
            server_logs = run(["docker", "logs", container]).stdout + run(["docker", "logs", container]).stderr
            if any(value in server_logs for key, value in environment.items() if key.endswith("PASSWORD")):
                raise RuntimeError("Database logs disclosed a bootstrap password")
            passed("database_logs_do_not_disclose_bootstrap_passwords")
        finally:
            run(["docker", "rm", "-f", container], check=False)
    evidence = {"timestamp": datetime.now(timezone.utc).isoformat(), "scope": "Local disposable Docker PostgreSQL 17 with required TLS; no AWS execution", "checks": checks, "passed": len(checks), "failed": 0}
    report.parent.mkdir(parents=True, exist_ok=True)
    report.write_text(json.dumps(evidence, indent=2) + "\n")
    print(f"Local ECS runtime database drill: {len(checks)} passed, 0 failed; report {report}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--report", type=Path, required=True)
    main(parser.parse_args().report.resolve())
