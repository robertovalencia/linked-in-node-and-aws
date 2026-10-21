import {
  ArrowUpRight,
  BriefcaseBusiness,
  ChevronDown,
  ChevronLeft,
  ChevronRight,
  Search,
  ShieldCheck,
  SlidersHorizontal,
} from "lucide-react";
import type { MarketplaceState } from "../../hooks/useMarketplace";
import { categories } from "../../utils/presentation";
import { ProviderCard } from "./ProviderCard";
export function Discovery({
  providers,
  total,
  loading,
  error,
  search,
  category,
  setCategory,
  skill,
  setSkill,
  maxRate,
  setMaxRate,
  available,
  setAvailable,
  sort,
  setSort,
  page,
  setPage,
  filters,
  setFilters,
  compare,
  reload,
  setReload,
  showProvider,
  toggleCompare,
  resetFilters,
}: Pick<
  MarketplaceState,
  | "providers"
  | "total"
  | "loading"
  | "error"
  | "search"
  | "category"
  | "setCategory"
  | "skill"
  | "setSkill"
  | "maxRate"
  | "setMaxRate"
  | "available"
  | "setAvailable"
  | "sort"
  | "setSort"
  | "page"
  | "setPage"
  | "filters"
  | "setFilters"
  | "compare"
  | "reload"
  | "setReload"
  | "showProvider"
  | "toggleCompare"
  | "resetFilters"
>) {
  return (
    <section id="discover" className="discovery content-shell">
      <div className="section-heading">
        <div>
          <span className="eyebrow subtle">FIND YOUR NEXT COLLABORATOR</span>
          <h2>Expertise for what’s next.</h2>
          <p>Big ambitions. Everyday challenges. There’s an expert for that.</p>
        </div>
        <a className="text-link" href="#how-it-works">
          How it works <ArrowUpRight size={17} />
        </a>
      </div>
      <div
        className="category-tabs"
        role="group"
        aria-label="Service categories"
      >
        {categories.map((c) => (
          <button
            className={
              category === c.name ? "category-tab selected" : "category-tab"
            }
            key={c.name}
            onClick={() => {
              setCategory(c.name);
              setPage(0);
            }}
          >
            <c.icon size={19} />
            {c.label || c.name}
          </button>
        ))}
      </div>
      <div className="results-toolbar">
        <div className="results-count">
          {loading ? (
            "Finding professionals…"
          ) : (
            <>
              <strong>{total} professionals</strong>
              <span>
                {search ? ` for “${search}”` : " ready for your next project"}
              </span>
            </>
          )}
        </div>
        <div className="toolbar-actions">
          <button
            className={`filter-button ${filters ? "filter-active" : ""}`}
            onClick={() => setFilters(!filters)}
            aria-expanded={filters}
          >
            <SlidersHorizontal size={16} /> Filters{" "}
            {(skill || maxRate || available) && <span className="filter-dot" />}
          </button>
          <label className="sort-label">
            Sort by{" "}
            <select
              aria-label="Sort providers"
              value={sort}
              onChange={(e) => {
                setSort(e.target.value);
                setPage(0);
              }}
            >
              <option value="recommended">Recommended</option>
              <option value="rate-asc">Hourly rate: low to high</option>
              <option value="rating">Highest rated</option>
            </select>
            <ChevronDown size={15} />
          </label>
        </div>
      </div>
      <p className="demo-provenance">
        Demo profiles · Ratings, reviews and project counts are sample data.
      </p>
      {filters && (
        <div className="filters-panel">
          <label>
            Tool or skill
            <input
              placeholder="e.g. Java, Kubernetes"
              value={skill}
              onChange={(e) => {
                setSkill(e.target.value);
                setPage(0);
              }}
            />
          </label>
          <label>
            Maximum hourly rate
            <select
              value={maxRate}
              onChange={(e) => {
                setMaxRate(e.target.value);
                setPage(0);
              }}
            >
              <option value="">Any budget</option>
              <option value="75">Up to $75 / hr</option>
              <option value="100">Up to $100 / hr</option>
              <option value="150">Up to $150 / hr</option>
              <option value="200">Up to $200 / hr</option>
            </select>
          </label>
          <label className="checkbox-field">
            <input
              type="checkbox"
              checked={available}
              onChange={(e) => {
                setAvailable(e.target.checked);
                setPage(0);
              }}
            />{" "}
            Available for new projects
          </label>
          <button className="text-link" onClick={resetFilters}>
            Clear all
          </button>
        </div>
      )}
      {error ? (
        <div className="empty-state">
          <BriefcaseBusiness size={34} />
          <h3>We couldn’t load professionals</h3>
          <p>{error}</p>
          <button
            className="button button-outline"
            onClick={() => setReload(reload + 1)}
          >
            Try again
          </button>
        </div>
      ) : loading ? (
        <div className="provider-grid" aria-busy="true">
          {[1, 2, 3, 4, 5, 6].map((i) => (
            <div className="skeleton-card" key={i}>
              <div className="skeleton-cover" />
              <div className="skeleton-avatar" />
              <div className="skeleton-line" />
              <div className="skeleton-line short" />
              <div className="skeleton-line" />
            </div>
          ))}
        </div>
      ) : providers.length === 0 ? (
        <div className="empty-state">
          <Search size={34} />
          <h3>A fresh search could open new doors.</h3>
          <p>
            No professionals match these filters. Try a broader skill or
            category.
          </p>
          <button className="button button-outline" onClick={resetFilters}>
            Clear search & filters
          </button>
        </div>
      ) : (
        <div className="provider-grid">
          {providers.map((p, i) => (
            <ProviderCard
              key={p.id}
              p={p}
              i={i}
              compare={compare}
              showProvider={showProvider}
              toggleCompare={toggleCompare}
            />
          ))}
        </div>
      )}
      {!loading && !error && total > 6 && (
        <div className="pagination">
          <button
            className="button button-outline"
            disabled={page === 0}
            onClick={() => setPage(page - 1)}
          >
            <ChevronLeft size={16} /> Previous
          </button>
          <span>
            Page {page + 1} of {Math.ceil(total / 6)}
          </span>
          <button
            className="button button-outline"
            disabled={(page + 1) * 6 >= total}
            onClick={() => setPage(page + 1)}
          >
            Next <ChevronRight size={16} />
          </button>
        </div>
      )}
      <div className="discovery-note">
        <ShieldCheck size={17} />
        <span>Explore their work. Start a conversation. Find your fit.</span>
      </div>
    </section>
  );
}
