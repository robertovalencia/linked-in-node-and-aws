# RDS database trust bundle

`rds-us-east-2-bundle.pem` is the public AWS RDS Ohio regional CA bundle downloaded on 27 October 2026 from [AWS trust storage](https://truststore.pki.rds.amazonaws.com/us-east-2/us-east-2-bundle.pem). Its SHA-256 is `d46e1bdfda05c8e7644e50930806a19b139a222542bf0348082fb59ece2b5fa5`.

The backend image includes this public trust anchor at `/app/certs/rds-us-east-2-bundle.pem`. ECS sets `DB_SSL=true` and `DB_SSL_CA_FILE` to this path. Node verifies both the certificate chain and RDS hostname. Secret passwords are passed through `DB_PASSWORD`, not interpolated into URLs. Do not add `sslmode` parameters to `DB_URL`; they can replace `pg`'s explicit TLS settings and are rejected.

[Official RDS TLS documentation](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/UsingWithRDS.SSL.html) describes the regional bundle and rotation. Review certificate expiry and the configured RDS CA before each cloud rehearsal. Replace this file only from the official HTTPS source, record its digest, rebuild the image, run the positive/wrong-CA/wrong-hostname tests and deploy through the normal reviewed release path. Do not disable verification to bypass a rotation failure.
