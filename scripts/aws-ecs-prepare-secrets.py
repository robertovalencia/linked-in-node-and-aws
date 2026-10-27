#!/usr/bin/env python3
"""Create local mode-0600 lab payloads. This script never calls AWS."""
import argparse
import base64
import json
import os
from pathlib import Path
import re
import secrets
import shutil
import subprocess
import tempfile


def prepare(directory: Path, broker_dns: str) -> None:
    if not re.fullmatch(r"[a-z0-9](?:[a-z0-9.-]{0,251}[a-z0-9])?", broker_dns):
        raise ValueError("Broker DNS must be a lower-case DNS hostname")
    if directory.exists():
        raise ValueError("Destination already exists; refusing an accidental credential rotation")
    directory.mkdir(parents=True, mode=0o700)
    os.chmod(directory, 0o700)
    try:
        with tempfile.TemporaryDirectory(prefix="cert-", dir=directory) as temporary:
            certs = Path(temporary)
            def openssl(*args: str) -> None:
                subprocess.run(["openssl", *args], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            openssl("genpkey", "-algorithm", "RSA", "-pkeyopt", "rsa_keygen_bits:3072", "-out", str(certs / "ca.key"))
            openssl("req", "-x509", "-new", "-sha256", "-days", "30", "-key", str(certs / "ca.key"), "-subj", "/CN=Marketplace ECS lab CA", "-out", str(certs / "ca.pem"))
            openssl("genpkey", "-algorithm", "RSA", "-pkeyopt", "rsa_keygen_bits:2048", "-out", str(certs / "server.key"))
            openssl("req", "-new", "-key", str(certs / "server.key"), "-subj", f"/CN={broker_dns}", "-out", str(certs / "server.csr"))
            (certs / "extensions.cnf").write_text(f"subjectAltName=DNS:{broker_dns}\nbasicConstraints=CA:FALSE\nkeyUsage=digitalSignature,keyEncipherment\nextendedKeyUsage=serverAuth\n")
            openssl("x509", "-req", "-sha256", "-days", "7", "-in", str(certs / "server.csr"), "-CA", str(certs / "ca.pem"), "-CAkey", str(certs / "ca.key"), "-CAcreateserial", "-extfile", str(certs / "extensions.cnf"), "-out", str(certs / "server.pem"))
            ca = (certs / "ca.pem").read_text()
            broker = {
                "KAFKA_SSL_CA": ca,
                "KAFKA_SERVER_KEY": (certs / "server.key").read_text(),
                "KAFKA_SERVER_CERT": (certs / "server.pem").read_text(),
                "KAFKA_ADMIN_PASSWORD": secrets.token_hex(32),
                "INQUIRIES_KAFKA_PASSWORD": secrets.token_hex(32),
                "NOTIFICATIONS_KAFKA_PASSWORD": secrets.token_hex(32),
                "CLUSTER_ID": base64.urlsafe_b64encode(secrets.token_bytes(16)).decode().rstrip("="),
            }
            payloads = {"broker": broker, "shared": {
                "JWT_SECRET": secrets.token_hex(32), "INTERNAL_API_KEY": secrets.token_hex(32), "KAFKA_SSL_CA": ca,
            }}
            for service in ("identity", "catalog", "inquiries", "notifications"):
                payloads[service] = {"password": secrets.token_hex(32)}
                if service in ("inquiries", "notifications"):
                    payloads[service]["kafka_password"] = broker[f"{service.upper()}_KAFKA_PASSWORD"]
            for name, payload in payloads.items():
                target = directory / f"{name}.json"
                descriptor = os.open(target, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
                with os.fdopen(descriptor, "w") as stream:
                    json.dump(payload, stream)
                    stream.write("\n")
    except BaseException:
        shutil.rmtree(directory)
        raise


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--directory", type=Path, required=True, help="Ignored local work directory; never add generated payloads to Git")
    parser.add_argument("--broker-dns", required=True)
    args = parser.parse_args()
    prepare(args.directory.resolve(), args.broker_dns)
    print("Six local secret payloads prepared; no AWS operation was performed. Keep payloads out of Git.")
