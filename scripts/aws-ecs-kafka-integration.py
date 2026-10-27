#!/usr/bin/env python3
"""Local disposable Kafka TLS/SCRAM/ACL drill from the actual userdata config; no AWS."""
import argparse
from datetime import datetime, timezone
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import tempfile
import time

ROOT = Path(__file__).resolve().parents[1]
IMAGE = "apache/kafka:4.0.1@sha256:9a129e03121d46d74349a480f8f17082df3dd411b28281c9eabb95cf096370b9"


def main(report: Path) -> None:
    name = f"marketplace-ecs-kafka-test-{os.getpid()}"
    def run(args, *, env=None, check=True):
        return subprocess.run(args, env=env, check=check, capture_output=True, text=True)
    spec = importlib.util.spec_from_file_location("prepare", ROOT / "scripts/aws-ecs-prepare-secrets.py")
    prepare = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(prepare)
    with tempfile.TemporaryDirectory(prefix="marketplace-kafka-tls-") as temporary:
        fixtures = Path(temporary)
        prepare.prepare(fixtures / "payloads", "kafka.test")
        secret = json.loads((fixtures / "payloads/broker.json").read_text())
        (fixtures / "broker-secret.json").write_text(json.dumps(secret))
        (fixtures / "config").mkdir()
        source = (ROOT / "infra/aws-ecs-dev/kafka-user-data.sh.tftpl").read_text()
        config = source.split("python3 - <<'CONFIG'\n", 1)[1].split("\nCONFIG", 1)[0]
        config = config.replace("root=Path('/opt/marketplace-kafka')", f"root=Path({str(fixtures)!r})")
        # Local fixture ownership differs from Linux host UID1000; container copy below applies real UID.
        config = config.replace("os.chown(file,1000,1000)", "None").replace("os.chown(config,1000,1000)", "None")
        original_dns = os.environ.get("BROKER_DNS")
        os.environ["BROKER_DNS"] = "kafka.test"
        exec(compile(config, "userdata-CONFIG", "exec"), {})
        if original_dns is None: os.environ.pop("BROKER_DNS")
        else: os.environ["BROKER_DNS"] = original_dns
        try:
            run(["docker", "network", "create", name])
            for volume in (name + "-config", name + "-data"):
                run(["docker", "volume", "create", volume])
            run(["docker", "run", "-d", "--name", name, "--network", name, "--network-alias", "kafka.test", "--memory", "1536m", "-e", "KAFKA_HEAP_OPTS=-Xms256m -Xmx768m", "-v", f"{name}-config:/run/kafka", "-v", f"{name}-data:/var/lib/kafka/data", "-v", f"{fixtures / 'config'}:/fixtures:ro", "--entrypoint", "/bin/bash", IMAGE, "-c", "until [ -r /run/kafka/format.sh ]; do sleep 1; done; exec bash /run/kafka/format.sh"])
            run(["docker", "exec", "-u", "0", name, "/bin/bash", "-c", "cp /fixtures/* /run/kafka/; chown -R 1000:1000 /run/kafka /var/lib/kafka/data; chmod 700 /run/kafka; chmod 600 /run/kafka/*"])
            cli = ["docker", "exec", name, "/opt/kafka/bin/kafka-topics.sh", "--bootstrap-server", "kafka.test:9093", "--command-config", "/run/kafka/admin.properties"]
            for attempt in range(90):
                if run(cli + ["--list"], check=False).returncode == 0: break
                time.sleep(1)
            else: raise RuntimeError("Local Kafka authenticated startup failed; inspect disposable container logs before cleanup")
            run(cli + ["--create", "--topic", "inquiry.created.v1", "--partitions", "1", "--replication-factor", "1"])
            acl = ["docker", "exec", name, "/opt/kafka/bin/kafka-acls.sh", "--bootstrap-server", "kafka.test:9093", "--command-config", "/run/kafka/admin.properties", "--add", "--allow-principal"]
            for principal, operations in (("inquiries", ("Write", "Describe")), ("notifications", ("Read", "Describe"))):
                for operation in operations:
                    run(acl + [f"User:{principal}", "--operation", operation, "--topic", "inquiry.created.v1"])
            run(acl + ["User:notifications", "--operation", "Read", "--group", "marketplace-notifications-v1"])
            verification = r"""
import { Kafka, logLevel } from 'kafkajs';
import { kafkaOptions } from './dist/common/connections.js';
process.env.SERVICE='inquiries';process.env.DEPLOYMENT_MODE='aws-ecs';
process.env.KAFKA_BROKERS='kafka.test:9093';process.env.KAFKA_SSL='true';process.env.KAFKA_SASL_MECHANISM='scram-sha-512';
const options=kafkaOptions();const results=[];
const config={...options,logLevel:logLevel.NOTHING,retry:{retries:4},connectionTimeout:5000,requestTimeout:10000};
const producer=new Kafka(config).producer({allowAutoTopicCreation:false});
await producer.connect();await producer.send({topic:'inquiry.created.v1',messages:[{key:'tls-test',value:'authenticated event'}]});await producer.disconnect();
results.push({name:'scram_tls_inquiries_publish',status:'PASS'});
const consumer=new Kafka({...config,sasl:{mechanism:'scram-sha-512',username:'notifications',password:process.env.NOTIFICATIONS_PASSWORD}}).consumer({groupId:'marketplace-notifications-v1',allowAutoTopicCreation:false});
await consumer.connect();await consumer.subscribe({topic:'inquiry.created.v1',fromBeginning:true});
try{await new Promise(async(resolve,reject)=>{const timeout=setTimeout(()=>reject(Error('consume timeout')),30000);try{await consumer.run({eachMessage:async({message})=>{if(message.value?.toString()==='authenticated event'){clearTimeout(timeout);resolve();}}});}catch(error){clearTimeout(timeout);reject(error);}});}finally{await consumer.disconnect();}
results.push({name:'scram_tls_notifications_consume',status:'PASS'});
for (const [name,override] of [
 ['wrong_password',{sasl:{mechanism:'scram-sha-512',username:'inquiries',password:'incorrect'}}],
 ['wrong_ca',{ssl:{rejectUnauthorized:true}}],
 ['wrong_hostname',{ssl:{...options.ssl,servername:'wrong.internal'}}],
 ['plaintext',{ssl:false}],
 ['anonymous',{sasl:undefined}],
]){const client=new Kafka({...config,...override,retry:{retries:0},connectionTimeout:1000,requestTimeout:2000}).producer();let denied=false;try{await client.connect();await client.send({topic:'inquiry.created.v1',messages:[{value:'forbidden-negative-test'}]});}catch{denied=true;}finally{await client.disconnect().catch(()=>{});}if(!denied)throw Error('Unexpected Kafka access: '+name);results.push({name:'deny_'+name,status:'PASS'});}
const deniedProducer=new Kafka({...config,sasl:{mechanism:'scram-sha-512',username:'notifications',password:process.env.NOTIFICATIONS_PASSWORD}}).producer({allowAutoTopicCreation:false});
let denied=false;try{await deniedProducer.connect();await deniedProducer.send({topic:'inquiry.created.v1',messages:[{value:'forbidden'}]});}catch{denied=true;}finally{await deniedProducer.disconnect();}
if(!denied)throw Error('Consumer principal unexpectedly permitted publish');results.push({name:'deny_notifications_publish_acl',status:'PASS'});
console.log(JSON.stringify(results));
"""
            env = {**os.environ, "KAFKA_SSL_CA": secret["KAFKA_SSL_CA"], "KAFKA_USERNAME": "inquiries", "KAFKA_PASSWORD": secret["INQUIRIES_KAFKA_PASSWORD"], "NOTIFICATIONS_PASSWORD": secret["NOTIFICATIONS_KAFKA_PASSWORD"]}
            output = run(["docker", "run", "--rm", "--network", name, "-v", f"{ROOT / 'backend/dist'}:/app/dist:ro", "-e", "KAFKA_SSL_CA", "-e", "KAFKA_USERNAME", "-e", "KAFKA_PASSWORD", "-e", "NOTIFICATIONS_PASSWORD", "--entrypoint", "node", "linked-in-node/backend:local", "--input-type=module", "-e", verification], env=env)
            checks = [{"name": "actual_userdata_config_authenticated_startup", "status": "PASS"}] + json.loads(output.stdout)
        except BaseException as error:
            if isinstance(error, subprocess.CalledProcessError):
                detail = error.stderr or error.stdout or str(error.returncode)
                for value in secret.values(): detail = detail.replace(value, "<redacted>")
                print("Local Kafka client failure: " + detail[-4000:])
            logs = run(["docker", "logs", "--tail", "100", name], check=False)
            # Never print broker config or passwords; only preserve redacted exception hints.
            redacted = logs.stdout + logs.stderr
            for value in secret.values(): redacted = redacted.replace(value, "<redacted>")
            print(redacted[-12000:])
            raise
        finally:
            run(["docker", "rm", "-f", name], check=False)
            for volume in (name + "-config", name + "-data"): run(["docker", "volume", "rm", volume], check=False)
            run(["docker", "network", "rm", name], check=False)
    report.parent.mkdir(parents=True, exist_ok=True)
    report.write_text(json.dumps({"timestamp": datetime.now(timezone.utc).isoformat(), "scope": "Local disposable Kafka from actual userdata config; no AWS execution", "checks": checks, "passed": len(checks), "failed": 0}, indent=2) + "\n")
    print(f"Local Kafka TLS/SCRAM/ACL drill: {len(checks)} passed, 0 failed; report {report}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--report", type=Path, required=True)
    main(parser.parse_args().report.resolve())
