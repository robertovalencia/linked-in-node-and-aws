import {
  ArrowRight,
  ArrowUpRight,
  BriefcaseBusiness,
  Check,
  CheckCircle2,
  Clock,
  Code2,
  ExternalLink,
  Mail,
  MapPin,
  Plus,
  Star,
} from "lucide-react";
import { Avatar } from "../../components/common/Avatar";
import { Modal } from "../../components/common/Modal";
import type { MarketplaceState } from "../../hooks/useMarketplace";
import { money } from "../../utils/presentation";
export function ProfileDialog({
  selected,
  setSelected,
  detailLoading,
  compare,
  toggleCompare,
  contact,
}: Pick<
  MarketplaceState,
  | "selected"
  | "setSelected"
  | "detailLoading"
  | "compare"
  | "toggleCompare"
  | "contact"
>) {
  if (!selected) return null;
  return (
    <Modal title="Professional profile" onClose={() => setSelected(null)} wide>
      <div
        className="profile-cover"
        style={{ backgroundColor: selected.coverColor || "#dce9e5" }}
      >
        <span>{selected.category}</span>
      </div>
      <div className="profile-content">
        <div className="profile-top">
          <Avatar p={selected} size="large" />
          <div className="profile-top-actions">
            <button
              className="button button-outline"
              onClick={() => toggleCompare(selected.id)}
            >
              {compare.includes(selected.id) ? (
                <Check size={17} />
              ) : (
                <Plus size={17} />
              )}{" "}
              Compare
            </button>
            <button
              className="button button-primary"
              onClick={() => contact(selected)}
            >
              Send inquiry <ArrowUpRight size={16} />
            </button>
          </div>
        </div>
        <div className="profile-title">
          <h2>{selected.name}</h2>
          <p>{selected.headline}</p>
          <span className="location">
            <MapPin size={14} />
            {selected.location}
            <span>·</span>
            {selected.available
              ? "Available for new projects"
              : "Currently booked"}
          </span>
        </div>
        <div className="profile-stats">
          <div>
            <strong>
              <Star size={16} fill="currentColor" />
              {selected.rating.toFixed(1)}
            </strong>
            <span>{selected.reviewCount} reviews</span>
          </div>
          <div>
            <strong>{selected.completedProjects}</strong>
            <span>Completed projects</span>
          </div>
          <div>
            <strong>
              {money(selected.hourlyRate)} <small>/ hr</small>
            </strong>
            <span>Hourly rate</span>
          </div>
          <div>
            <strong>
              <Clock size={16} />
              {selected.responseTime}
            </strong>
            <span>Response time</span>
          </div>
        </div>
        <p className="demo-provenance profile-provenance">
          Demo profile · Ratings, reviews and project counts are sample data.
        </p>
        {detailLoading && <p className="muted">Updating profile…</p>}
        <div className="profile-columns">
          <div>
            <section className="profile-section">
              <h3>About</h3>
              <p className="preserve-lines">{selected.about}</p>
            </section>
            <section className="profile-section">
              <h3>How I can help</h3>
              <div className="service-list">
                {selected.services.map((s) => (
                  <div key={s}>
                    <CheckCircle2 size={18} />
                    {s}
                  </div>
                ))}
              </div>
            </section>
            <section className="profile-section">
              <h3>Experience</h3>
              {selected.experience.map((x, i) => (
                <div className="experience" key={i}>
                  <BriefcaseBusiness size={20} />
                  <div>
                    <h4>{x.title}</h4>
                    <span>
                      {x.company} · {x.period}
                    </span>
                    <p>{x.description}</p>
                  </div>
                </div>
              ))}
            </section>
            <section className="profile-section">
              <h3>Selected work</h3>
              {selected.portfolio.map((x, i) => (
                <div className="portfolio-item" key={i}>
                  <div className={`portfolio-art cover-${i % 4}`}>
                    <Code2 size={32} />
                  </div>
                  <div>
                    <h4>{x.title}</h4>
                    <p>{x.description}</p>
                    {/^https?:\/\//.test(x.url) && (
                      <a
                        href={x.url}
                        target="_blank"
                        rel="noreferrer"
                        className="text-link"
                      >
                        View project <ExternalLink size={13} />
                      </a>
                    )}
                  </div>
                </div>
              ))}
            </section>
          </div>
          <aside>
            <section className="profile-aside">
              <h3>Skills & expertise</h3>
              <div className="skill-tags">
                {selected.skills.map((s) => (
                  <span key={s}>{s}</span>
                ))}
              </div>
              <h3>Tools I work with</h3>
              <div className="tools-list">
                {selected.tools.map((s) => (
                  <div key={s}>
                    <Check size={14} />
                    {s}
                  </div>
                ))}
              </div>
            </section>
            <div className="inquiry-prompt">
              <Mail size={25} />
              <h3>Have something in mind?</h3>
              <p>Share your project and see if you’re a good fit.</p>
              <button
                className="button button-primary"
                onClick={() => contact(selected)}
              >
                Let’s talk <ArrowRight size={16} />
              </button>
            </div>
          </aside>
        </div>
      </div>
    </Modal>
  );
}
