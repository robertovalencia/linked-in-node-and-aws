import { ArrowRight, ArrowUpRight } from "lucide-react";
import { Avatar } from "../../components/common/Avatar";
import { Loading } from "../../components/common/Loading";
import { Modal } from "../../components/common/Modal";
import type { MarketplaceState } from "../../hooks/useMarketplace";
import { money } from "../../utils/presentation";
export function CompareDialog({
  setCompareOpen,
  compareProviders,
  compareError,
  showProvider,
  toggleCompare,
  contact,
}: Pick<
  MarketplaceState,
  | "setCompareOpen"
  | "compareProviders"
  | "compareError"
  | "showProvider"
  | "toggleCompare"
  | "contact"
>) {
  return (
    <Modal
      title="Find your best fit"
      onClose={() => setCompareOpen(false)}
      wide
    >
      <div className="modal-body">
        <p className="muted">
          A closer look at the people behind your next project.
        </p>
        <p className="demo-provenance comparison-provenance">
          Demo profiles · Ratings, reviews and project counts are sample data.
        </p>
        {compareError ? (
          <p className="form-error">{compareError}</p>
        ) : compareProviders.length === 0 ? (
          <Loading />
        ) : (
          <div
            className="comparison-grid"
            style={{
              gridTemplateColumns: `repeat(${compareProviders.length},minmax(220px,1fr))`,
            }}
          >
            {compareProviders.map((p) => (
              <div className="comparison-column" key={p.id}>
                <Avatar p={p} />
                <h3>{p.name}</h3>
                <p>{p.headline}</p>
                <button
                  className="text-link"
                  onClick={() => {
                    setCompareOpen(false);
                    void showProvider(p);
                  }}
                >
                  View profile <ArrowUpRight size={16} />
                </button>
                <dl>
                  <dt>Hourly rate</dt>
                  <dd>{money(p.hourlyRate)} / hr</dd>
                  <dt>Availability</dt>
                  <dd>
                    {p.available ? "Available for work" : "Currently booked"}
                  </dd>
                  <dt>Rating</dt>
                  <dd>
                    ★ {p.rating} · {p.reviewCount} reviews
                  </dd>
                  <dt>Completed projects</dt>
                  <dd>{p.completedProjects}</dd>
                  <dt>Location</dt>
                  <dd>{p.location}</dd>
                  <dt>Response time</dt>
                  <dd>{p.responseTime}</dd>
                  <dt>Skills</dt>
                  <dd>
                    <div className="skill-tags">
                      {p.skills.map((s) => (
                        <span key={s}>{s}</span>
                      ))}
                    </div>
                  </dd>
                  <dt>Tools</dt>
                  <dd>{p.tools.join(", ")}</dd>
                  <dt>Services</dt>
                  <dd>{p.services.join(" · ")}</dd>
                </dl>
                <button
                  className="button button-primary"
                  onClick={() => {
                    setCompareOpen(false);
                    contact(p);
                  }}
                >
                  Send inquiry <ArrowRight size={16} />
                </button>
                <button
                  className="remove-comparison"
                  onClick={() => toggleCompare(p.id)}
                >
                  Remove
                </button>
              </div>
            ))}
          </div>
        )}
      </div>
    </Modal>
  );
}
