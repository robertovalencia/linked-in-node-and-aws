import { useEffect, useRef, useState } from "react";
import { ApiError } from "../services/http";
import { inquiryService } from "../services/marketplace";
import type { CreateInquiry } from "../services/marketplace";
import type { Auth } from "../types/marketplace";
type Attempt = { key: string; payload: CreateInquiry };
const storageKey = (auth: Auth, providerId: string) =>
  `expertly-node-aws-inquiry-attempt:${encodeURIComponent(auth.id)}:${encodeURIComponent(providerId)}`;
function readAttempt(key: string, providerId: string): Attempt | null {
  try {
    const value = JSON.parse(
      sessionStorage.getItem(key) || "null",
    ) as Attempt | null;
    const payload = value?.payload;
    if (
      value &&
      typeof value.key === "string" &&
      payload?.providerId === providerId &&
      typeof payload.subject === "string" &&
      typeof payload.message === "string" &&
      typeof payload.budget === "number" &&
      typeof payload.clientType === "string"
    )
      return value;
  } catch {
    /* Corrupt browser storage is not a valid logical attempt. */
  }
  return null;
}
/** A transport retry must preserve both the key and the exact canonical payload. */
export function useInquiryAttempt(
  auth: Auth,
  providerId: string,
  onSent: () => void,
) {
  const key = storageKey(auth, providerId);
  const [initialAttempt] = useState(() => readAttempt(key, providerId));
  const [attempt, setAttempt] = useState(initialAttempt);
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState("");
  const mounted = useRef(true);
  const inFlight = useRef(false);
  useEffect(() => {
    mounted.current = true;
    return () => {
      mounted.current = false;
    };
  }, []);
  const finish = () => {
    sessionStorage.removeItem(key);
    if (mounted.current) {
      setAttempt(null);
      onSent();
    }
  };
  const submit = async (payload: CreateInquiry) => {
    if (inFlight.current) return;
    const canonical = attempt || { key: crypto.randomUUID(), payload };
    // Persist before sending: dismiss/reopen and page reload must resume this attempt.
    sessionStorage.setItem(key, JSON.stringify(canonical));
    setAttempt(canonical);
    inFlight.current = true;
    setBusy(true);
    setError("");
    try {
      await inquiryService.create(auth, canonical.key, canonical.payload);
      finish();
    } catch (failure) {
      // Only a first-transmission rejection rules out an earlier commit. A retry
      // rejected by auth/validation says nothing about the original uncertain request.
      const rejected =
        !attempt &&
        failure instanceof ApiError &&
        [400, 401, 403, 404, 413, 422, 429].includes(failure.status);
      if (rejected) {
        sessionStorage.removeItem(key);
        if (mounted.current) setAttempt(null);
      }
      if (mounted.current)
        setError(
          (failure as Error).message +
            (rejected
              ? " The request was rejected; you can correct the details and submit a new attempt."
              : " Delivery is unconfirmed. Details are frozen; retry the original inquiry safely or resolve the saved inquiry before starting another."),
        );
    } finally {
      inFlight.current = false;
      if (mounted.current) setBusy(false);
    }
  };
  const reconcile = async () => {
    // Only the idempotency endpoint can identify this logical attempt. A historical
    // inquiry with identical content is not evidence that this saved key committed.
    if (attempt) await submit(attempt.payload);
  };
  return { initialAttempt, attempt, busy, error, submit, reconcile };
}
