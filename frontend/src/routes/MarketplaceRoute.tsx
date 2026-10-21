import { ArrowRight, CheckCircle2, GitCompareArrows, X } from "lucide-react";
import { Login } from "../components/auth/Login";
import { CompareDialog } from "../components/discovery/CompareDialog";
import { Discovery } from "../components/discovery/Discovery";
import { Hero } from "../components/discovery/Hero";
import { Dashboard } from "../components/inquiries/Dashboard";
import { InquiryForm } from "../components/inquiries/InquiryForm";
import { HowItWorks } from "../components/layout/HowItWorks";
import { ProviderCta } from "../components/layout/ProviderCta";
import { SiteFooter } from "../components/layout/SiteFooter";
import { SiteHeader } from "../components/layout/SiteHeader";
import { ValueStrip } from "../components/layout/ValueStrip";
import { NotificationsDialog } from "../components/notifications/NotificationsDialog";
import { Editor } from "../components/profile/Editor";
import { ProfileDialog } from "../components/profile/ProfileDialog";
import { useMarketplace } from "../hooks/useMarketplace";
export function MarketplaceRoute() {
  const state = useMarketplace();
  const {
    auth,
    setAuth,
    selected,
    compare,
    setCompare,
    compareOpen,
    setCompareOpen,
    loginOpen,
    setLoginOpen,
    inquiryTarget,
    setInquiryTarget,
    dashboard,
    setDashboard,
    editor,
    setEditor,
    notificationsOpen,
    toast,
    setToast,
    reload,
    setReload,
  } = state;
  return (
    <>
      <SiteHeader {...state} />
      <main>
        <Hero {...state} />
        <ValueStrip />
        <Discovery {...state} />
        <HowItWorks />
        <ProviderCta {...state} />
      </main>
      <SiteFooter />
      {compare.length > 0 && (
        <div className="compare-bar">
          <div>
            <GitCompareArrows size={19} />
            <strong>
              {compare.length} professional{compare.length > 1 ? "s" : ""}{" "}
              selected
            </strong>
            <span>Compare up to 3</span>
          </div>
          <button className="text-link" onClick={() => setCompare([])}>
            Clear
          </button>
          <button
            className="button button-primary"
            onClick={() => setCompareOpen(true)}
          >
            Compare <ArrowRight size={17} />
          </button>
        </div>
      )}
      {toast && (
        <div className="toast" role="status">
          <CheckCircle2 size={19} />
          {toast}
          <button
            className="icon-button"
            aria-label="Dismiss notification"
            onClick={() => setToast("")}
          >
            <X size={16} />
          </button>
        </div>
      )}
      {selected && <ProfileDialog {...state} />}
      {loginOpen && (
        <Login
          onClose={() => {
            setLoginOpen(false);
            if (!auth) setInquiryTarget(null);
          }}
          onLogin={(a) => {
            setAuth(a);
            setLoginOpen(false);
            setToast(`Welcome back, ${a.name.split(" ")[0]}.`);
            if (a.role !== "CLIENT") setInquiryTarget(null);
          }}
        />
      )}
      {inquiryTarget && auth?.role === "CLIENT" && !loginOpen && (
        <InquiryForm
          provider={inquiryTarget}
          auth={auth}
          onClose={() => setInquiryTarget(null)}
          onSent={() => {
            setInquiryTarget(null);
            setToast("Your inquiry was sent. Follow its status in your inbox.");
            setReload(reload + 1);
          }}
        />
      )}
      {dashboard && auth && (
        <Dashboard
          auth={auth}
          onClose={() => setDashboard(false)}
          onEdit={() => {
            setDashboard(false);
            setEditor(true);
          }}
        />
      )}
      {editor && auth?.role === "PROVIDER" && (
        <Editor
          auth={auth}
          onClose={() => setEditor(false)}
          onSaved={() => {
            setEditor(false);
            setReload(reload + 1);
            setToast("Your profile has been saved.");
          }}
        />
      )}
      {notificationsOpen && <NotificationsDialog {...state} />}
      {compareOpen && <CompareDialog {...state} />}
    </>
  );
}
