import { ArrowRight, ArrowUpRight, Check, Code2, Search } from "lucide-react";
import type { MarketplaceState } from "../../hooks/useMarketplace";
export function Hero({
  query,
  setQuery,
  setSearch,
  setPage,
  browse,
}: Pick<
  MarketplaceState,
  "query" | "setQuery" | "setSearch" | "setPage" | "browse"
>) {
  return (
    <section className="hero">
      <div className="hero-inner">
        <div className="hero-copy">
          <span className="eyebrow">
            <span /> INDEPENDENT EXPERTISE. SHARED AMBITION.
          </span>
          <h1>
            Great work starts
            <br />
            with the <em>right people.</em>
          </h1>
          <p>
            Find trusted professionals who bring your ideas to life.
            <br className="desktop-break" /> From the first conversation to your
            next big thing.
          </p>
          <form
            className="hero-search"
            onSubmit={(e) => {
              e.preventDefault();
              setSearch(query);
              setPage(0);
              browse();
            }}
          >
            <Search size={23} />
            <input
              aria-label="Search services or skills"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              placeholder="What do you need help with?"
            />
            <button className="button button-primary" type="submit">
              Find an expert <ArrowRight size={18} />
            </button>
          </form>
          <div className="popular">
            <span>Popular:</span>
            {["Web development", "DevOps", "Brand design"].map((s) => (
              <button
                key={s}
                onClick={() => {
                  setQuery(
                    s === "Web development"
                      ? "React"
                      : s === "Brand design"
                        ? "Design"
                        : s,
                  );
                  setSearch(
                    s === "Web development"
                      ? "React"
                      : s === "Brand design"
                        ? "Design"
                        : s,
                  );
                  setPage(0);
                  browse();
                }}
              >
                {s}
              </button>
            ))}
          </div>
          <div className="hero-proof">
            <div className="proof-avatars">
              <img alt="" src="/assets/ava-martinez.jpg" />
              <img alt="" src="/assets/leo-chen.jpg" />
              <img alt="" src="/assets/james-okafor.jpg" />
            </div>
            <span>
              <strong>Good people. Great possibilities.</strong>
              <br />A better way to find your next collaborator.
            </span>
          </div>
        </div>
        <div
          className="hero-art"
          aria-label="Independent professionals collaborating"
        >
          <div className="orbit orbit-one" />
          <div className="orbit orbit-two" />
          <span className="art-spark">✳</span>
          <div className="portrait portrait-main">
            <img
              src="/assets/ava-martinez.jpg"
              alt="Creative professional smiling"
            />
          </div>
          <div className="portrait portrait-secondary">
            <img
              src="/assets/leo-chen.jpg"
              alt="Independent technology consultant"
            />
          </div>
          <div className="floating-card expert-label">
            <span className="status-dot" />
            <span>OPEN TO POSSIBILITIES</span>
          </div>
          <div className="floating-card project-card">
            <span className="project-icon">
              <Check size={22} />
            </span>
            <div>
              <strong>Your next great project</strong>
              <span>starts with a connection.</span>
            </div>
            <ArrowUpRight size={20} />
          </div>
          <div className="skill-bubble">
            <Code2 size={18} /> Ideas → impact
          </div>
          <span className="art-caption">
            THE RIGHT EXPERTISE CHANGES EVERYTHING.
          </span>
        </div>
      </div>
    </section>
  );
}
