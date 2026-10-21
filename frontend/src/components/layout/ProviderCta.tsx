import { ArrowRight, ArrowUpRight } from "lucide-react";
import type { MarketplaceState } from "../../hooks/useMarketplace";
export function ProviderCta({
  auth,
  setLoginOpen,
  setEditor,
}: Pick<MarketplaceState, "auth" | "setLoginOpen" | "setEditor">) {
  return (
    <section className="provider-cta content-shell">
      <div>
        <span className="eyebrow subtle">YOUR EXPERTISE BELONGS HERE</span>
        <h2>
          Do great work.
          <br />
          Find people who value it.
        </h2>
        <p>Put your skills in front of your next great client.</p>
        <button
          className="button button-primary"
          onClick={() =>
            auth?.role === "PROVIDER" ? setEditor(true) : setLoginOpen(true)
          }
        >
          {auth?.role === "PROVIDER"
            ? "Manage my services"
            : "Provider sign in"}{" "}
          <ArrowRight size={17} />
        </button>
      </div>
      <div className="cta-mark">
        <span>
          Made for
          <br />
          <em>independents.</em>
        </span>
        <ArrowUpRight size={70} />
      </div>
    </section>
  );
}
