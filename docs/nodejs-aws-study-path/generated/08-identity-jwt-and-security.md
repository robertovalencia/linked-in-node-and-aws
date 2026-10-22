---
title: Passwords, JWTs, roles and resource ownership
topic: Security
last_researched: 2026-10-22
source_labels: Project source evidence; Interview PDF requirements; Official documentation; Proposed extensions explicitly labeled
---
# Identity answers who; authorization answers what

Prerequisites: 05–07. Follow backend/src/identity/identity.controller.ts → identity.service.ts → password.ts → common/auth.ts. Login validates input and rate-limits attempts per request IP in process memory. Identity looks up a normalized email with parameterized SQL, verifies a password and signs an actor token.

## Password and token explanation

The application uses asynchronous scrypt with a random 16-byte salt and a 64-byte derived key. The stored value is scrypt:salt:hexhash, not plaintext and not reversible encryption. Verification checks the encoded format, derives the candidate and compares equal-size bytes using timingSafeEqual. A dummy hash for unknown accounts reduces an obvious fast missing-user path; it is not a proof that every timing channel is eliminated. The demo seed shares a synthetic demonstration password, which is appropriate only for this laboratory.

signActor creates an HS256 token with issuer and audience marketplace, email subject and one-hour expiry. verifyActor fixes the accepted algorithm, checks issuer/audience, lets the library verify expiry and signature, and validates principal fields. JWT payloads are encoded, not encrypted; never put secrets in claims. The guard rejects missing/invalid bearer tokens and adds the verified actor. requireRole and per-resource ownership checks then enforce business permission.

Catalog protects private owner lookups with a distinct internal key and timing-safe comparison. It checks byte lengths before timingSafeEqual, because different lengths would throw. Being reachable only through internal routing is additional exposure control, not a substitute for this check.

## Executable negative lab

With local services up, run curl -i -H 'Authorization: Bearer invalid' http://127.0.0.1:8180/api/inquiries. Expect 401 with generic JSON detail. Use the UI to log in as a synthetic client, attempt a provider-only action through an authenticated HTTP client, and expect 403. Log in as one provider and attempt to change another provider's inquiry; expect ownership rejection. Reuse repository acceptance/security tests to build correct bodies and tokens rather than publishing a token in notes. Never record bearer tokens or real passwords in evidence.

Run npm --prefix backend test -- --runTestsByPath test/security.spec.ts to inspect the repository's focused security behavior. Record actual output; this command exercises code, while an external security audit remains separate.

## Debugging scenarios

A good signature with a wrong issuer/audience is invalid. A CLIENT token is not a provider permission grant. Expiry can explain a 401 after an hour, but inspect clock assumptions and actual response before assuming it. A UI hiding the edit button does not protect the endpoint. Test direct calls. An internal secret accidentally copied to frontend code is exposed because browser assets are public to that user.

## Senior tradeoffs and proposed hardening

All verifiers possessing the shared HMAC secret can mint tokens. Production extensions include asymmetric identity-provider tokens and rotation, hardened session handling, distributed login throttling, account lifecycle/revocation and audited access. Browser localStorage token persistence is currently implemented; XSS can read it. HttpOnly cookie sessions change XSS/CSRF design and require careful same-site, CSRF and proxy decisions; they are not a one-line universal fix. Helmet and input validation reduce specific risks but do not establish total security.



### Hashing versus encryption?

Password verification needs a deliberately costly one-way derivation, whereas encryption is reversible with a key.

### Role versus ownership?

Role permits a class of operation; ownership restricts the particular resource.

- [ ] Trace login and token verification without skipping runtime checks.
- [ ] Explain salt, scrypt, timing-safe comparison and dummy hash.
- [ ] Demonstrate 401 and ownership/role 403 paths.
- [ ] Name existing controls and production extensions accurately.



## References

Official references were checked 2026-10-22. Use the repository version/lockfiles as the compatibility baseline; current documentation may describe newer releases. Local source paths below are relative to /Users/robertovalencia/Documents/Business/linked-in-node-and-aws/. GitHub links require access and may lag that local baseline.

- [Node crypto](https://nodejs.org/api/crypto.html) — accessed 2026-10-22.
- [jsonwebtoken project](https://github.com/auth0/node-jsonwebtoken) — accessed 2026-10-22.
- [OWASP authentication guidance](https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html) — accessed 2026-10-22.
- [Project source: backend/src/identity/identity.controller.ts](https://github.com/robertovalencia/linked-in-node-and-aws/blob/main/backend/src/identity/identity.controller.ts) — local baseline inspected 2026-10-22; private published source may lag.
- [Project source: backend/src/identity/identity.service.ts](https://github.com/robertovalencia/linked-in-node-and-aws/blob/main/backend/src/identity/identity.service.ts) — local baseline inspected 2026-10-22; private published source may lag.
- [Project source: backend/src/identity/password.ts](https://github.com/robertovalencia/linked-in-node-and-aws/blob/main/backend/src/identity/password.ts) — local baseline inspected 2026-10-22; private published source may lag.
- [Project source: backend/src/common/auth.ts](https://github.com/robertovalencia/linked-in-node-and-aws/blob/main/backend/src/common/auth.ts) — local baseline inspected 2026-10-22; private published source may lag.
- [Project source: backend/test/security.spec.ts](https://github.com/robertovalencia/linked-in-node-and-aws/blob/main/backend/test/security.spec.ts) — local baseline inspected 2026-10-22; private published source may lag.
