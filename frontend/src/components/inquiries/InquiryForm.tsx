import { ArrowUpRight, ShieldCheck } from "lucide-react";
import { useState } from "react";
import { Avatar } from "../../components/common/Avatar";
import { Modal } from "../../components/common/Modal";
import { useInquiryAttempt } from "../../hooks/useInquiryAttempt";
import type { Auth, Provider } from "../../types/marketplace";
export function InquiryForm({
  provider,
  auth,
  onClose,
  onSent,
}: {
  provider: Provider;
  auth: Auth;
  onClose: () => void;
  onSent: () => void;
}) {
  const { initialAttempt, attempt, busy, error, submit, reconcile } =
    useInquiryAttempt(auth, provider.id, onSent);
  const [subject, setSubject] = useState(initialAttempt?.payload.subject || "");
  const [message, setMessage] = useState(initialAttempt?.payload.message || "");
  const [budget, setBudget] = useState(
    initialAttempt ? String(initialAttempt.payload.budget) : "",
  );
  const [clientType, setClientType] = useState(
    initialAttempt?.payload.clientType ||
      (auth.email.includes("company") ? "COMPANY" : "INDIVIDUAL"),
  );
  return (
    <Modal
      title={`Let’s work with ${provider.name.split(" ")[0]}`}
      onClose={onClose}
    >
      <form
        className="modal-body form"
        onSubmit={async (e) => {
          e.preventDefault();
          await submit({
            providerId: provider.id,
            subject,
            message,
            budget: Number(budget),
            clientType,
          });
        }}
      >
        <div className="inquiry-recipient">
          <Avatar p={provider} size="small" />
          <div>
            <strong>{provider.name}</strong>
            <span>{provider.headline}</span>
          </div>
        </div>
        <label>
          You’re reaching out as
          <select
            disabled={!!attempt}
            value={clientType}
            onChange={(e) => setClientType(e.target.value)}
          >
            <option value="COMPANY">A company</option>
            <option value="INDIVIDUAL">An individual</option>
          </select>
        </label>
        <label>
          Project title
          <input
            disabled={!!attempt}
            required
            minLength={5}
            maxLength={160}
            placeholder="e.g. Build our new customer portal"
            value={subject}
            onChange={(e) => setSubject(e.target.value)}
          />
        </label>
        <label>
          Tell them about your project
          <textarea
            disabled={!!attempt}
            required
            minLength={20}
            maxLength={5000}
            rows={5}
            placeholder="Your goals, timeline, and the kind of help you’re looking for…"
            value={message}
            onChange={(e) => setMessage(e.target.value)}
          />
        </label>
        <label>
          Estimated budget (USD)
          <input
            disabled={!!attempt}
            type="number"
            required
            min="1"
            max="10000000"
            placeholder="2500"
            value={budget}
            onChange={(e) => setBudget(e.target.value)}
          />
        </label>
        {attempt && (
          <p role="status" className="form-hint">
            This submission is saved with its original details. Resolve delivery
            before editing or starting another inquiry. Closing and reopening
            restores the same attempt.
          </p>
        )}
        {error && (
          <p role="alert" className="form-error">
            {error}
          </p>
        )}
        <button
          type="submit"
          className="button button-primary button-full"
          disabled={busy}
        >
          {busy
            ? "Sending inquiry…"
            : attempt
              ? "Retry original inquiry"
              : "Send inquiry"}{" "}
          <ArrowUpRight size={17} />
        </button>
        {attempt && (
          <button
            type="button"
            className="button button-outline button-full"
            disabled={busy}
            onClick={() => void reconcile()}
          >
            Resolve saved inquiry
          </button>
        )}
        <p className="form-hint">
          <ShieldCheck size={14} /> This sends a private inquiry to the
          professional.
        </p>
      </form>
    </Modal>
  );
}
