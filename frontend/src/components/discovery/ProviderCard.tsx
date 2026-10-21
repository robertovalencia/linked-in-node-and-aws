import { ArrowUpRight, Check, MapPin, Plus, Star } from "lucide-react";
import { Avatar } from "../../components/common/Avatar";
import type { MarketplaceState } from "../../hooks/useMarketplace";
import type { Provider } from "../../types/marketplace";
import { money } from "../../utils/presentation";
export function ProviderCard({
  p,
  i,
  compare,
  showProvider,
  toggleCompare,
}: { p: Provider; i: number } & Pick<
  MarketplaceState,
  "compare" | "showProvider" | "toggleCompare"
>) {
  return (
    <article className="provider-card">
      <div
        className={`card-cover cover-${i % 4}`}
        style={p.coverColor ? { backgroundColor: p.coverColor } : undefined}
      >
        <span>{p.category}</span>
        <button
          className={`compare-toggle ${compare.includes(p.id) ? "checked" : ""}`}
          aria-label={`${compare.includes(p.id) ? "Remove" : "Add"} ${p.name} ${compare.includes(p.id) ? "from" : "to"} comparison`}
          onClick={() => toggleCompare(p.id)}
        >
          {compare.includes(p.id) ? <Check size={16} /> : <Plus size={16} />}
        </button>
        <div className="cover-shape" />
      </div>
      <div className="card-body">
        <div className="card-person">
          <button
            className="avatar-button"
            aria-label={`View ${p.name} profile`}
            onClick={() => showProvider(p)}
          >
            <Avatar p={p} />
          </button>
          {p.available ? (
            <span className="available">
              <span />
              Available for work
            </span>
          ) : (
            <span className="unavailable">Currently booked</span>
          )}
        </div>
        <button className="card-title" onClick={() => showProvider(p)}>
          {p.name}
        </button>
        <p className="headline">{p.headline}</p>
        <span className="location">
          <MapPin size={13} />
          {p.location}
        </span>
        <div className="card-rating">
          <Star size={14} fill="currentColor" />
          <strong>{p.rating.toFixed(1)}</strong>
          <span>({p.reviewCount} reviews)</span>
          <span className="rating-divider">·</span>
          <span>{p.completedProjects} projects</span>
        </div>
        <div className="skill-tags">
          {p.skills.slice(0, 3).map((s) => (
            <span key={s}>{s}</span>
          ))}
          {p.skills.length > 3 && (
            <span className="extra-skill">+{p.skills.length - 3}</span>
          )}
        </div>
        <div className="card-footer">
          <div className="card-price">
            <strong>{money(p.hourlyRate)}</strong>
            <span> / hr</span>
          </div>
          <button className="profile-link" onClick={() => showProvider(p)}>
            View profile <ArrowUpRight size={17} />
          </button>
        </div>
      </div>
    </article>
  );
}
