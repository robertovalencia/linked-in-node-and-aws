# Data consistency and security

Authentication answers who is calling. Authorization answers whether that caller may take this action on this resource. The provider editor must derive ownership from the verified JWT, reject another provider's ID and avoid accepting owner email from the request. Inquiry listing must filter by actual sender/recipient. Notification read state belongs only to its recipient.

JWT verification checks algorithm, signature, issuer, audience and expiry. A decoded token is not proof of identity. Shared signing keys are intentionally limited to this lab; a public deployment should use asymmetric verification and a dedicated identity provider. Tokens in localStorage are convenient for this demo but exposed to script compromise. React escaping, link protocol validation and minimizing sensitive browser state reduce risk; an HttpOnly session design needs its own CSRF and session specification.

SQL parameters protect values. Identifiers and sort expressions need explicit allowlists; they cannot be made safe by a value placeholder. Validation must reject invalid types, overlong text, negative or nonfinite numbers, unknown state values and malformed arrays. Public profiles must exclude private email/owner fields, including after update.

An inquiry transaction saves the durable request and outbox together. A failure rolls both back. The publisher retries unacknowledged events; duplicate publication after a crash is expected. The notification inbox has a unique event identifier. The consumer must commit its broker offset only after its database operation succeeds. Ordering and idempotency are business properties; adding Kafka does not automatically provide them.

Each database has a separate owner role. The admin login exists only for initialization/operations and is not given to an application service. Local secrets are generated once into ignored `.env`; deleting that file while keeping database volumes changes credentials without changing stored database passwords. Keep both or explicitly reset the disposable local environment.

For a schema rollback, distinguish reverting application image from restoring data. Use backward-compatible expand/contract migrations. An old image cannot undo a dropped column. AWS dev's single persistent host is not a backup strategy: document snapshot/restore before any data becomes valuable.
