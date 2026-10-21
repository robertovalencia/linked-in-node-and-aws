CREATE TABLE notifications (id uuid PRIMARY KEY, event_id uuid UNIQUE NOT NULL, inquiry_id uuid NOT NULL,
 recipient_email text NOT NULL, message text NOT NULL, created_at timestamptz NOT NULL, read boolean NOT NULL DEFAULT false);
CREATE INDEX notifications_recipient_date ON notifications(recipient_email,created_at DESC);
