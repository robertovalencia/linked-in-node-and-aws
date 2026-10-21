import { ArrowUpRight, Mail } from "lucide-react";
import { useEffect, useState } from "react";
import { Loading } from "../../components/common/Loading";
import { Modal } from "../../components/common/Modal";
import { inquiryService } from "../../services/marketplace";
import type { Auth, Inquiry } from "../../types/marketplace";
import { date, money } from "../../utils/presentation";
export function Dashboard({
  auth,
  onClose,
  onEdit,
}: {
  auth: Auth;
  onClose: () => void;
  onEdit: () => void;
}) {
  const [items, setItems] = useState<Inquiry[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [busy, setBusy] = useState("");
  const [loadError, setLoadError] = useState("");
  const [reload, setReload] = useState(0);
  useEffect(() => {
    const controller = new AbortController();
    setLoading(true);
    setLoadError("");
    inquiryService
      .list(auth, controller.signal)
      .then((items) => {
        if (!controller.signal.aborted) setItems(items);
      })
      .catch((error) => {
        if (!controller.signal.aborted) setLoadError(error.message);
      })
      .finally(() => {
        if (!controller.signal.aborted) setLoading(false);
      });
    return () => controller.abort();
  }, [auth, reload]);
  return (
    <Modal
      title={auth.role === "PROVIDER" ? "Your workspace" : "Your inquiries"}
      onClose={onClose}
      wide
    >
      <div className="modal-body">
        <div className="dashboard-intro">
          <div>
            <h3>Hello, {auth.name.split(" ")[0]}.</h3>
            <p className="muted">
              {auth.role === "PROVIDER"
                ? "Good work starts with a conversation. Manage your project inquiries here."
                : "Keep track of the connections you’re making."}
            </p>
          </div>
          {auth.role === "PROVIDER" && (
            <button className="button button-outline" onClick={onEdit}>
              Edit my profile <ArrowUpRight size={16} />
            </button>
          )}
        </div>
        {error && (
          <p role="alert" className="form-error">
            {error}
          </p>
        )}
        {loading ? (
          <Loading />
        ) : loadError ? (
          <div className="empty-state compact">
            <p role="alert" className="form-error">
              {loadError}
            </p>
            <button
              className="button button-outline"
              onClick={() => setReload((value) => value + 1)}
            >
              Retry loading inquiries
            </button>
          </div>
        ) : items.length === 0 ? (
          <div className="empty-state compact">
            <Mail size={34} />
            <h3>Your next conversation starts here</h3>
            <p>
              {auth.role === "PROVIDER"
                ? "Service inquiries will appear as clients discover your profile."
                : "Find a professional and send an inquiry to get started."}
            </p>
            <button className="button button-outline" onClick={onClose}>
              Explore professionals
            </button>
          </div>
        ) : (
          <div className="inquiries-list">
            {items.map((i) => (
              <article className="inquiry-item" key={i.id}>
                <div className="inquiry-item-heading">
                  <span className={`status status-${i.status.toLowerCase()}`}>
                    {i.status}
                  </span>
                  <time>{date(i.createdAt)}</time>
                </div>
                <h3>{i.subject}</h3>
                <p className="inquiry-participant">
                  {auth.role === "PROVIDER"
                    ? `From ${i.clientName}`
                    : `To ${i.providerName}`}{" "}
                  · {i.clientType === "COMPANY" ? "Company" : "Individual"} ·
                  Budget {money(i.budget)}
                </p>
                <p className="preserve-lines">{i.message}</p>
                {auth.role === "PROVIDER" &&
                  (i.status === "PENDING" || i.status === "NEW") && (
                    <div className="inquiry-actions">
                      {["ACCEPTED", "DECLINED"].map((status) => (
                        <button
                          key={status}
                          disabled={!!busy}
                          className={`button ${status === "ACCEPTED" ? "button-primary" : "button-outline"}`}
                          onClick={async () => {
                            setBusy(i.id);
                            setError("");
                            try {
                              const updated = await inquiryService.respond(
                                auth,
                                i.id,
                                status,
                              );
                              setItems(
                                items.map((x) => (x.id === i.id ? updated : x)),
                              );
                            } catch (e) {
                              setError((e as Error).message);
                            } finally {
                              setBusy("");
                            }
                          }}
                        >
                          {busy === i.id
                            ? "Updating…"
                            : status === "ACCEPTED"
                              ? "Accept inquiry"
                              : "Decline"}
                        </button>
                      ))}
                    </div>
                  )}
              </article>
            ))}
          </div>
        )}
      </div>
    </Modal>
  );
}
