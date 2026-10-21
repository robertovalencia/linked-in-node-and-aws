CREATE TABLE inquiries (
 id uuid PRIMARY KEY, provider_id text NOT NULL, provider_email text NOT NULL, provider_name text NOT NULL,
 client_email text NOT NULL, client_name text NOT NULL, subject text NOT NULL, message text NOT NULL,
 budget numeric(12,2) NOT NULL CHECK (budget >= 1), client_type text NOT NULL CHECK (client_type IN ('COMPANY','INDIVIDUAL')),
 status text NOT NULL DEFAULT 'PENDING' CHECK (status IN ('PENDING','ACCEPTED','DECLINED')), created_at timestamptz NOT NULL DEFAULT now(),
 idempotency_key text NOT NULL, request_hash text NOT NULL, UNIQUE (client_email,idempotency_key)
);
CREATE INDEX inquiries_client_date ON inquiries(client_email,created_at DESC);
CREATE INDEX inquiries_provider_date ON inquiries(provider_email,created_at DESC);
CREATE TABLE outbox (event_id uuid PRIMARY KEY, inquiry_id uuid NOT NULL REFERENCES inquiries(id), payload jsonb NOT NULL,
 created_at timestamptz NOT NULL DEFAULT now(), published_at timestamptz);
CREATE INDEX outbox_pending ON outbox(created_at) WHERE published_at IS NULL;
