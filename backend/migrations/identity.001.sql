CREATE TABLE accounts (
 email text PRIMARY KEY, name text NOT NULL, role text NOT NULL CHECK (role IN ('CLIENT','PROVIDER')),
 password_hash text NOT NULL, created_at timestamptz NOT NULL DEFAULT now()
);
