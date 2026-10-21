CREATE TABLE providers (id text PRIMARY KEY, owner_email text UNIQUE NOT NULL, document jsonb NOT NULL,
 CHECK (document->>'id' = id));
