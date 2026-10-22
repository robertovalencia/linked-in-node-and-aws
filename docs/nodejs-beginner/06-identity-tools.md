# Identity tools: scrypt, Buffer, JWT, Zod and Map

Prerequisites: lessons 02, 03 and 05. Read the mechanism first; use login only as its real example.

[Service guide index](README.md). Study one concept at a time: explain it, open the linked code, then answer the recall question. Code blocks are source excerpts unless the practice section explicitly says to run them.

## Error-first callbacks become promises

**What:** Node’s scrypt API accepts a callback with an error and a result. `promisify` wraps that convention in a Promise-returning function.

**How:** The callback error becomes a rejection; its successful derived key becomes the resolved value. `await` simplifies sequencing but does not change the cryptographic algorithm.

**Real code:** [backend/src/identity/password.ts · lines 3–3](https://github.com/robertovalencia/linked-in-node-and-aws/blob/fbf61d81f9d240e2d974f1bcf21789ac6f2b21fa/backend/src/identity/password.ts#L3-L3).

```ts
const scrypt = promisify(scryptCallback);
```

**Watch for:** promisify does not move arbitrary synchronous code to another thread.

### Why can hashPassword use await scrypt?

scryptCallback was adapted from callback style to a promise by util.promisify.

## scrypt: cost and asynchronous work

**What:** scrypt derives a password-checking key using deliberate CPU and memory cost. A fast general-purpose hash is unsuitable for storing passwords.

**How:** The asynchronous API uses Node’s native worker-pool resources. JavaScript can serve other I/O while awaiting it, but many simultaneous hashes can still exhaust limited capacity.

**Real code:** [backend/src/identity/password.ts · lines 6–7](https://github.com/robertovalencia/linked-in-node-and-aws/blob/fbf61d81f9d240e2d974f1bcf21789ac6f2b21fa/backend/src/identity/password.ts#L6-L7).

```ts
const hash = (await scrypt(password, salt, 64)) as Buffer;
return `scrypt:${salt}:${hash.toString('hex')}`;
```

**Watch for:** Adding async to a CPU-heavy JavaScript function would not produce the same offloading.

### Why throttle login when hashing is asynchronous?

Async avoids blocking JavaScript directly, but password work still consumes finite CPU, memory and worker capacity.

## randomBytes, salt and hex encoding

**What:** A salt makes two equal passwords produce different stored derivations. It is stored beside the hash and is not a secret.

**How:** `randomBytes(16)` produces 16 random bytes; hex represents them using 32 characters. The 64-byte derived key becomes 128 hex characters.

**Real code:** [backend/src/identity/password.ts · lines 5–7](https://github.com/robertovalencia/linked-in-node-and-aws/blob/fbf61d81f9d240e2d974f1bcf21789ac6f2b21fa/backend/src/identity/password.ts#L5-L7).

```ts
const salt = randomBytes(16).toString('hex');
const hash = (await scrypt(password, salt, 64)) as Buffer;
return `scrypt:${salt}:${hash.toString('hex')}`;
```

**Watch for:** Hex is a reversible representation of bytes, not encryption.

### Can the stored salt be public?

Yes. Password safety depends on the derivation cost and password strength, not salt secrecy.

## Buffer and timingSafeEqual

**What:** A Buffer stores bytes. `timingSafeEqual` compares equal-length byte sequences without content-dependent early exit in that comparison.

**How:** Verification checks the stored format, derives a new candidate, decodes the stored hex, then compares bytes. Other branches and surrounding code can still expose timing differences.

**Real code:** [backend/src/identity/password.ts · lines 18–18](https://github.com/robertovalencia/linked-in-node-and-aws/blob/fbf61d81f9d240e2d974f1bcf21789ac6f2b21fa/backend/src/identity/password.ts#L18-L18).

```ts
return timingSafeEqual(candidate, Buffer.from(hash, 'hex'));
```

**Watch for:** Different-length buffers throw; validate the representation before comparing.

### Why not compare two strings with ===?

An ordinary comparison does not promise the same timing behavior for secret-derived bytes.

## Optional chaining and a dummy derivation

**What:** `account?.password_hash ?? dummyHash` supplies a hash even when no account exists.

**How:** The service performs a real derivation before returning its generic login error. This reduces the obvious fast missing-user branch without proving that all account-enumeration signals disappear.

**Real code:** [backend/src/identity/identity.service.ts · lines 52–54](https://github.com/robertovalencia/linked-in-node-and-aws/blob/fbf61d81f9d240e2d974f1bcf21789ac6f2b21fa/backend/src/identity/identity.service.ts#L52-L54).

```ts
const valid = await verifyPassword(password, account?.password_hash ?? this.dummyHash);
if (!account || !valid) throw new UnauthorizedException('Invalid email or password');
const actor: Actor = {
```

**Watch for:** The fallback protects timing behavior; it never authorizes a missing account.

### Can the dummy hash accidentally log in a missing user?

The next condition explicitly rejects !account regardless of the verification result.

## JWT signing: claims, encoding and HMAC

**What:** A JWT normally has header.payload.signature sections encoded for transport. Encoding does not hide the claims.

**How:** jwt.sign uses HS256 to authenticate the header/payload with a shared secret. The options add issuer, audience, subject and a one-hour expiry; the expiry is not a server-side session record.

**Real code:** [backend/src/common/auth.ts · lines 14–21](https://github.com/robertovalencia/linked-in-node-and-aws/blob/fbf61d81f9d240e2d974f1bcf21789ac6f2b21fa/backend/src/common/auth.ts#L14-L21).

```ts
  return jwt.sign(actor, required('JWT_SECRET'), {
    algorithm: 'HS256',
    issuer: 'marketplace',
    audience: 'marketplace',
    subject: actor.email,
    expiresIn: '1h',
  });
}
```

**Watch for:** Every verifier holding this HMAC secret can also mint a token. The signature does not provide encryption.

### What does expiresIn do here?

The library adds an expiration claim; later verification rejects an expired token unless explicitly configured otherwise.

## jsonwebtoken: signature versus claims

**What:** A JWT contains encoded header/payload data plus a signature. HS256 uses the same secret for signing and verification.

**How:** jwt.verify checks the allowed algorithm, signature, expiry and configured issuer/audience rules. The remaining code checks subject/email and id/email equality plus valid actor fields.

**Real code:** [backend/src/common/auth.ts · lines 24–29](https://github.com/robertovalencia/linked-in-node-and-aws/blob/fbf61d81f9d240e2d974f1bcf21789ac6f2b21fa/backend/src/common/auth.ts#L24-L29).

```ts
const value = jwt.verify(token, required('JWT_SECRET'), {
  algorithms: ['HS256'],
  issuer: 'marketplace',
  audience: 'marketplace',
});
if (
```

**Watch for:** jwt.decode only reads data; it does not establish signature validity.

### Does a valid JWT prove permission to edit a row?

No. The service still checks role and the resource’s stored owner.

## Map-based throttling and mutable objects

**What:** Map stores key/value pairs in process memory. Here each value tracks an IP’s count and expiry.

**How:** The increment mutates the stored object; expired entries are removed on later calls. Counts reset on restart and are not shared with another service replica.

**Real code:** [backend/src/identity/identity.controller.ts · lines 26–30](https://github.com/robertovalencia/linked-in-node-and-aws/blob/fbf61d81f9d240e2d974f1bcf21789ac6f2b21fa/backend/src/identity/identity.controller.ts#L26-L30).

```ts
const key = request.ip ?? 'unknown';
const attempts = this.attempts.get(key) ?? { count: 0, until: now + 60_000 };
if (++attempts.count > 30)
  throw new HttpException('Too many login attempts; retry in one minute', 429);
this.attempts.set(key, attempts);
```

**Watch for:** Behind a proxy, effective request IP depends on proxy configuration; this is not a distributed rate limiter.

### What does a second replica do to the limit?

It has another Map, so a process-local limit does not enforce one global counter.

## Zod validates before service use

**What:** The strict login schema limits email/password shape and rejects unexpected fields.

**How:** Validation returns parsed values to the controller; a ZodError becomes a 400 through the shared filter. Credentials still require database lookup and password verification.

**Real code:** [backend/src/identity/identity.controller.ts · lines 15–17](https://github.com/robertovalencia/linked-in-node-and-aws/blob/fbf61d81f9d240e2d974f1bcf21789ac6f2b21fa/backend/src/identity/identity.controller.ts#L15-L17).

```ts
const loginSchema = z
  .object({ email: z.email().max(254), password: z.string().min(1).max(200) })
  .strict();
```

**Watch for:** A validated email address is not evidence that the sender owns that account.

### Is validation authentication?

No. Validation checks input shape; authentication checks the supplied credentials.

## Practice and mastery

- Trace `callback → promisify → Promise → await → Buffer` using the linked password code.
- Predict the salt and derived-key hex lengths: 32 and 128 characters.
- Run `npm --prefix backend test -- --runTestsByPath test/security.spec.ts` from the project root.
- Explain HS256 verification, role and row ownership separately. Do not save bearer tokens in study notes.
- Production extensions: external asymmetric identity provider, rotation and distributed throttling. These are not implemented by adding a decorator.

## References

Code links are pinned to the inspected source commit. The repository lockfiles define the study baseline; library documentation may cover newer versions.

- [Node crypto](https://nodejs.org/api/crypto.html)
- [Node util.promisify](https://nodejs.org/api/util.html#utilpromisifyoriginal)
- [jsonwebtoken](https://github.com/auth0/node-jsonwebtoken)
- [Zod](https://zod.dev/api)
- [Project example: Error-first callbacks become promises](https://github.com/robertovalencia/linked-in-node-and-aws/blob/fbf61d81f9d240e2d974f1bcf21789ac6f2b21fa/backend/src/identity/password.ts#L3-L3)
- [Project example: scrypt: cost and asynchronous work](https://github.com/robertovalencia/linked-in-node-and-aws/blob/fbf61d81f9d240e2d974f1bcf21789ac6f2b21fa/backend/src/identity/password.ts#L6-L7)
- [Project example: randomBytes, salt and hex encoding](https://github.com/robertovalencia/linked-in-node-and-aws/blob/fbf61d81f9d240e2d974f1bcf21789ac6f2b21fa/backend/src/identity/password.ts#L5-L7)
- [Project example: Buffer and timingSafeEqual](https://github.com/robertovalencia/linked-in-node-and-aws/blob/fbf61d81f9d240e2d974f1bcf21789ac6f2b21fa/backend/src/identity/password.ts#L18-L18)
- [Project example: Optional chaining and a dummy derivation](https://github.com/robertovalencia/linked-in-node-and-aws/blob/fbf61d81f9d240e2d974f1bcf21789ac6f2b21fa/backend/src/identity/identity.service.ts#L52-L54)
- [Project example: JWT signing: claims, encoding and HMAC](https://github.com/robertovalencia/linked-in-node-and-aws/blob/fbf61d81f9d240e2d974f1bcf21789ac6f2b21fa/backend/src/common/auth.ts#L14-L21)
- [Project example: jsonwebtoken: signature versus claims](https://github.com/robertovalencia/linked-in-node-and-aws/blob/fbf61d81f9d240e2d974f1bcf21789ac6f2b21fa/backend/src/common/auth.ts#L24-L29)
- [Project example: Map-based throttling and mutable objects](https://github.com/robertovalencia/linked-in-node-and-aws/blob/fbf61d81f9d240e2d974f1bcf21789ac6f2b21fa/backend/src/identity/identity.controller.ts#L26-L30)
- [Project example: Zod validates before service use](https://github.com/robertovalencia/linked-in-node-and-aws/blob/fbf61d81f9d240e2d974f1bcf21789ac6f2b21fa/backend/src/identity/identity.controller.ts#L15-L17)
