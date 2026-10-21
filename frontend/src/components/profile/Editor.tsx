import { Check, Plus, X } from "lucide-react";
import { useEffect, useState } from "react";
import { Loading } from "../../components/common/Loading";
import { Modal } from "../../components/common/Modal";
import { providerService } from "../../services/marketplace";
import type { Auth, Provider } from "../../types/marketplace";
import { categories } from "../../utils/presentation";
export function Editor({
  auth,
  onClose,
  onSaved,
}: {
  auth: Auth;
  onClose: () => void;
  onSaved: () => void;
}) {
  const [p, setP] = useState<Provider | null>(null);
  const [error, setError] = useState("");
  const [busy, setBusy] = useState(false);
  const [draft, setDraft] = useState<Record<string, string>>({});
  const [loading, setLoading] = useState(true);
  const [reload, setReload] = useState(0);
  useEffect(() => {
    const controller = new AbortController();
    setLoading(true);
    setError("");
    providerService
      .mine(auth, controller.signal)
      .then((v) => {
        if (controller.signal.aborted) return;
        setP(v);
        setDraft({
          skills: v.skills.join(", "),
          tools: v.tools.join(", "),
          services: v.services.join("\n"),
        });
      })
      .catch((e) => {
        if (!controller.signal.aborted) setError(e.message);
      })
      .finally(() => {
        if (!controller.signal.aborted) setLoading(false);
      });
    return () => controller.abort();
  }, [auth, reload]);
  const field = (k: keyof Provider, v: unknown) =>
    setP(p ? { ...p, [k]: v } : p);
  return (
    <Modal title="Make your expertise shine" onClose={onClose} wide>
      <form
        className="modal-body form profile-edit"
        onSubmit={async (e) => {
          e.preventDefault();
          if (!p) return;
          setError("");
          setBusy(true);
          try {
            await providerService.update(auth, {
              ...p,
              skills: draft.skills
                .split(",")
                .map((s) => s.trim())
                .filter(Boolean),
              tools: draft.tools
                .split(",")
                .map((s) => s.trim())
                .filter(Boolean),
              services: draft.services
                .split("\n")
                .map((s) => s.trim())
                .filter(Boolean),
              experience: p.experience,
              portfolio: p.portfolio,
            });
            onSaved();
          } catch (e) {
            setError((e as Error).message);
          } finally {
            setBusy(false);
          }
        }}
      >
        {error && (
          <p role="alert" className="form-error">
            {error}
          </p>
        )}
        {!p ? (
          loading ? (
            <Loading />
          ) : (
            <button
              type="button"
              className="button button-outline"
              onClick={() => setReload((value) => value + 1)}
            >
              Retry loading profile
            </button>
          )
        ) : (
          <>
            <p className="muted">
              Help future clients see the person, skills, and experience behind
              your work.
            </p>
            <div className="form-columns">
              <label>
                Name
                <input
                  required
                  value={p.name}
                  onChange={(e) => field("name", e.target.value)}
                />
              </label>
              <label>
                Location
                <input
                  required
                  value={p.location}
                  onChange={(e) => field("location", e.target.value)}
                />
              </label>
            </div>
            <label>
              Professional headline
              <input
                required
                maxLength={180}
                value={p.headline}
                onChange={(e) => field("headline", e.target.value)}
              />
            </label>
            <label>
              About you
              <textarea
                required
                rows={5}
                value={p.about}
                onChange={(e) => field("about", e.target.value)}
              />
            </label>
            <div className="form-columns">
              <label>
                Service category
                <select
                  value={p.category}
                  onChange={(e) => field("category", e.target.value)}
                >
                  {categories.slice(1).map((c) => (
                    <option key={c.name}>{c.name}</option>
                  ))}
                </select>
              </label>
              <label>
                Hourly rate (USD)
                <input
                  required
                  type="number"
                  min="5"
                  max="1000"
                  value={p.hourlyRate}
                  onChange={(e) => field("hourlyRate", Number(e.target.value))}
                />
              </label>
            </div>
            <label>
              Skills <small>Separate with commas</small>
              <input
                value={draft.skills}
                onChange={(e) => setDraft({ ...draft, skills: e.target.value })}
              />
            </label>
            <label>
              Tools <small>Separate with commas</small>
              <input
                value={draft.tools}
                onChange={(e) => setDraft({ ...draft, tools: e.target.value })}
              />
            </label>
            <label>
              Services <small>One service per line</small>
              <textarea
                rows={4}
                value={draft.services}
                onChange={(e) =>
                  setDraft({ ...draft, services: e.target.value })
                }
              />
            </label>
            <div className="form-columns">
              <label>
                Profile photo URL
                <input
                  type="text"
                  required
                  value={p.avatarUrl}
                  onChange={(e) => field("avatarUrl", e.target.value)}
                />
              </label>
              <label>
                Typical response time
                <input
                  value={p.responseTime}
                  onChange={(e) => field("responseTime", e.target.value)}
                />
              </label>
            </div>
            <label className="checkbox-field">
              <input
                type="checkbox"
                checked={p.available}
                onChange={(e) => field("available", e.target.checked)}
              />{" "}
              Available for new projects
            </label>
            <section className="structured-editor">
              <div className="editor-section-heading">
                <h3>Experience</h3>
                <button
                  type="button"
                  className="text-link"
                  disabled={p.experience.length >= 20}
                  onClick={() =>
                    field("experience", [
                      ...p.experience,
                      { title: "", company: "", period: "", description: "" },
                    ])
                  }
                >
                  <Plus size={14} /> Add experience
                </button>
              </div>
              {p.experience.map((x, i) => (
                <div className="editor-entry" key={i}>
                  <div className="editor-entry-heading">
                    <span>Experience {i + 1}</span>
                    <button
                      type="button"
                      className="icon-button"
                      aria-label={`Remove experience ${i + 1}`}
                      onClick={() =>
                        field(
                          "experience",
                          p.experience.filter((_, j) => j !== i),
                        )
                      }
                    >
                      <X size={16} />
                    </button>
                  </div>
                  <div className="form-columns">
                    <label>
                      Role or title
                      <input
                        required
                        maxLength={120}
                        value={x.title}
                        onChange={(e) =>
                          field(
                            "experience",
                            p.experience.map((v, j) =>
                              j === i ? { ...v, title: e.target.value } : v,
                            ),
                          )
                        }
                      />
                    </label>
                    <label>
                      Company
                      <input
                        required
                        maxLength={120}
                        value={x.company}
                        onChange={(e) =>
                          field(
                            "experience",
                            p.experience.map((v, j) =>
                              j === i ? { ...v, company: e.target.value } : v,
                            ),
                          )
                        }
                      />
                    </label>
                  </div>
                  <label>
                    Time period
                    <input
                      required
                      maxLength={80}
                      placeholder="2022 – Present"
                      value={x.period}
                      onChange={(e) =>
                        field(
                          "experience",
                          p.experience.map((v, j) =>
                            j === i ? { ...v, period: e.target.value } : v,
                          ),
                        )
                      }
                    />
                  </label>
                  <label>
                    What you accomplished
                    <textarea
                      required
                      maxLength={1500}
                      rows={3}
                      value={x.description}
                      onChange={(e) =>
                        field(
                          "experience",
                          p.experience.map((v, j) =>
                            j === i ? { ...v, description: e.target.value } : v,
                          ),
                        )
                      }
                    />
                  </label>
                </div>
              ))}
            </section>
            <section className="structured-editor">
              <div className="editor-section-heading">
                <h3>Portfolio</h3>
                <button
                  type="button"
                  className="text-link"
                  disabled={p.portfolio.length >= 12}
                  onClick={() =>
                    field("portfolio", [
                      ...p.portfolio,
                      { title: "", description: "", url: "" },
                    ])
                  }
                >
                  <Plus size={14} /> Add project
                </button>
              </div>
              {p.portfolio.map((x, i) => (
                <div className="editor-entry" key={i}>
                  <div className="editor-entry-heading">
                    <span>Project {i + 1}</span>
                    <button
                      type="button"
                      className="icon-button"
                      aria-label={`Remove project ${i + 1}`}
                      onClick={() =>
                        field(
                          "portfolio",
                          p.portfolio.filter((_, j) => j !== i),
                        )
                      }
                    >
                      <X size={16} />
                    </button>
                  </div>
                  <label>
                    Project title
                    <input
                      required
                      maxLength={120}
                      value={x.title}
                      onChange={(e) =>
                        field(
                          "portfolio",
                          p.portfolio.map((v, j) =>
                            j === i ? { ...v, title: e.target.value } : v,
                          ),
                        )
                      }
                    />
                  </label>
                  <label>
                    Description
                    <textarea
                      required
                      maxLength={1500}
                      rows={3}
                      value={x.description}
                      onChange={(e) =>
                        field(
                          "portfolio",
                          p.portfolio.map((v, j) =>
                            j === i ? { ...v, description: e.target.value } : v,
                          ),
                        )
                      }
                    />
                  </label>
                  <label>
                    Project link
                    <input
                      type="url"
                      required
                      pattern="https://.*"
                      placeholder="https://example.com"
                      value={x.url}
                      onChange={(e) =>
                        field(
                          "portfolio",
                          p.portfolio.map((v, j) =>
                            j === i ? { ...v, url: e.target.value } : v,
                          ),
                        )
                      }
                    />
                  </label>
                </div>
              ))}
            </section>
            <div className="form-footer">
              <button
                type="button"
                className="button button-outline"
                onClick={onClose}
              >
                Cancel
              </button>
              <button
                type="submit"
                className="button button-primary"
                disabled={busy}
              >
                {busy ? "Saving…" : "Save profile"} <Check size={17} />
              </button>
            </div>
          </>
        )}
      </form>
    </Modal>
  );
}
