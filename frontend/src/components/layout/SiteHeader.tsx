import { Bell, LogOut, Menu } from "lucide-react";
import type { MarketplaceState } from "../../hooks/useMarketplace";
export function SiteHeader({
  auth,
  setAuth,
  setLoginOpen,
  setDashboard,
  setEditor,
  setNotificationsOpen,
  notifications,
  setToast,
  mobileMenu,
  setMobileMenu,
  browse,
}: Pick<
  MarketplaceState,
  | "auth"
  | "setAuth"
  | "setLoginOpen"
  | "setDashboard"
  | "setEditor"
  | "setNotificationsOpen"
  | "notifications"
  | "setToast"
  | "mobileMenu"
  | "setMobileMenu"
  | "browse"
>) {
  return (
    <header className="site-header">
      <div className="nav-shell">
        <a
          className="brand"
          href="#"
          onClick={(e) => {
            e.preventDefault();
            window.scrollTo({ top: 0, behavior: "smooth" });
          }}
        >
          expertly<span className="brand-dot">.</span>
          <span className="brand-divider" />
          <span className="brand-sub">SERVICES</span>
        </a>
        <nav
          className={mobileMenu ? "navigation mobile-open" : "navigation"}
          aria-label="Main navigation"
        >
          <button className="nav-link active" onClick={browse}>
            Find a professional
          </button>
          <button
            className="nav-link"
            onClick={() => {
              if (auth?.role === "PROVIDER") setEditor(true);
              else {
                setLoginOpen(true);
                setToast(
                  "Use a provider demo account to manage your services.",
                );
              }
            }}
          >
            {auth?.role === "PROVIDER" ? "Manage services" : "Provider sign in"}
          </button>
          <a className="nav-link how-link" href="#how-it-works">
            How it works
          </a>
        </nav>
        <div className="nav-actions">
          {auth ? (
            <>
              <button
                className="notification-button icon-button"
                aria-label="Notifications"
                onClick={() => setNotificationsOpen(true)}
              >
                <Bell size={20} />
                {notifications.some((n) => !n.read) && (
                  <span className="notification-dot" />
                )}
              </button>
              <button
                className="account-button"
                onClick={() => setDashboard(true)}
              >
                <span className="tiny-avatar">{auth.name[0]}</span>
                <span>{auth.name.split(" ")[0]}</span>
              </button>
              <button
                className="icon-button logout"
                title="Sign out"
                aria-label="Sign out"
                onClick={() => {
                  setAuth(null);
                  setDashboard(false);
                  setToast("You have signed out.");
                }}
              >
                <LogOut size={18} />
              </button>
            </>
          ) : (
            <>
              <button className="join-link" onClick={() => setLoginOpen(true)}>
                Provider sign in
              </button>
              <button
                className="button button-outline sign-in"
                onClick={() => setLoginOpen(true)}
              >
                Sign in
              </button>
            </>
          )}
          <button
            className="icon-button menu-toggle"
            aria-label="Toggle menu"
            onClick={() => setMobileMenu(!mobileMenu)}
          >
            <Menu size={22} />
          </button>
        </div>
      </div>
    </header>
  );
}
