import { useEffect, useState } from "react";
import { notificationService, providerService } from "../services/marketplace";
import type { Notification, Provider } from "../types/marketplace";
import { useAuth } from "./useAuth";
export function useMarketplace() {
  const { auth, setAuth } = useAuth();
  const [providers, setProviders] = useState<Provider[]>([]);
  const [total, setTotal] = useState(0);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [query, setQuery] = useState("");
  const [search, setSearch] = useState("");
  const [category, setCategory] = useState("All services");
  const [skill, setSkill] = useState("");
  const [maxRate, setMaxRate] = useState("");
  const [available, setAvailable] = useState(false);
  const [sort, setSort] = useState("recommended");
  const [page, setPage] = useState(0);
  const [filters, setFilters] = useState(false);
  const [selected, setSelected] = useState<Provider | null>(null);
  const [detailLoading, setDetailLoading] = useState(false);
  const [compare, setCompare] = useState<string[]>(() => {
    try {
      const saved: unknown = JSON.parse(
        localStorage.getItem("expertly-node-aws-compare") || "[]",
      );
      return Array.isArray(saved)
        ? [
            ...new Set(
              saved.filter((id): id is string => typeof id === "string"),
            ),
          ].slice(0, 3)
        : [];
    } catch {
      return [];
    }
  });
  const [compareOpen, setCompareOpen] = useState(false);
  const [compareProviders, setCompareProviders] = useState<Provider[]>([]);
  const [compareError, setCompareError] = useState("");
  const [loginOpen, setLoginOpen] = useState(false);
  const [inquiryTarget, setInquiryTarget] = useState<Provider | null>(null);
  const [dashboard, setDashboard] = useState(false);
  const [editor, setEditor] = useState(false);
  const [notificationsOpen, setNotificationsOpen] = useState(false);
  const [notifications, setNotifications] = useState<Notification[]>([]);
  const [notificationsLoading, setNotificationsLoading] = useState(false);
  const [notificationsError, setNotificationsError] = useState("");
  const [notificationsReload, setNotificationsReload] = useState(0);
  const [toast, setToast] = useState("");
  const [mobileMenu, setMobileMenu] = useState(false);
  const [reload, setReload] = useState(0);
  useEffect(() => {
    localStorage.setItem("expertly-node-aws-compare", JSON.stringify(compare));
  }, [compare]);
  useEffect(() => {
    const controller = new AbortController();
    setLoading(true);
    setError("");
    const params = new URLSearchParams({
      q: search,
      sort,
      page: String(page),
      size: "6",
    });
    if (category !== "All services") params.set("category", category);
    if (skill) params.set("skill", skill);
    if (maxRate) params.set("maxRate", maxRate);
    if (available) params.set("available", "true");
    providerService
      .list(params, controller.signal)
      .then((r) => {
        if (controller.signal.aborted) return;
        setProviders(r.items);
        setTotal(r.total);
      })
      .catch((e) => {
        if (!controller.signal.aborted) setError(e.message);
      })
      .finally(() => {
        if (!controller.signal.aborted) setLoading(false);
      });
    return () => controller.abort();
  }, [search, category, skill, maxRate, available, sort, page, reload]);
  useEffect(() => {
    if (!auth) {
      setNotifications([]);
      setNotificationsError("");
      setNotificationsLoading(false);
      return;
    }
    const controller = new AbortController();
    setNotificationsLoading(true);
    setNotificationsError("");
    notificationService
      .list(auth, controller.signal)
      .then((items) => {
        if (!controller.signal.aborted) setNotifications(items);
      })
      .catch((error) => {
        if (!controller.signal.aborted) setNotificationsError(error.message);
      })
      .finally(() => {
        if (!controller.signal.aborted) setNotificationsLoading(false);
      });
    return () => controller.abort();
  }, [auth, reload, notificationsOpen, notificationsReload]);
  useEffect(() => {
    if (toast) {
      const t = setTimeout(() => setToast(""), 6000);
      return () => clearTimeout(t);
    }
  }, [toast]);
  useEffect(() => {
    if (compareOpen && compare.length === 0) {
      setCompareOpen(false);
      return;
    }
    if (!compareOpen) return;
    const controller = new AbortController();
    setCompareError("");
    setCompareProviders([]);
    Promise.all(compare.map((id) => providerService.get(id, controller.signal)))
      .then((items) => {
        if (!controller.signal.aborted) setCompareProviders(items);
      })
      .catch((error) => {
        if (!controller.signal.aborted) setCompareError(error.message);
      });
    return () => controller.abort();
  }, [compareOpen, compare]);
  const selectedId = selected?.id;
  useEffect(() => {
    if (!selectedId) return;
    const controller = new AbortController();
    setDetailLoading(true);
    providerService
      .get(selectedId, controller.signal)
      .then((provider) => {
        if (!controller.signal.aborted) setSelected(provider);
      })
      .catch((error) => {
        if (!controller.signal.aborted) setToast(error.message);
      })
      .finally(() => {
        if (!controller.signal.aborted) setDetailLoading(false);
      });
    return () => controller.abort();
  }, [selectedId]);
  const showProvider = (provider: Provider) => setSelected(provider);
  const toggleCompare = (id: string) => {
    if (compare.includes(id)) setCompare(compare.filter((x) => x !== id));
    else if (compare.length < 3) setCompare([...compare, id]);
    else setToast("You can compare up to three professionals at a time.");
  };
  const contact = (p: Provider) => {
    if (!auth) {
      setInquiryTarget(p);
      setLoginOpen(true);
    } else if (auth.role === "CLIENT") setInquiryTarget(p);
    else
      setToast(
        "Sign in with a company or individual account to send an inquiry.",
      );
  };
  const resetFilters = () => {
    setCategory("All services");
    setSkill("");
    setMaxRate("");
    setAvailable(false);
    setQuery("");
    setSearch("");
    setPage(0);
  };
  const browse = () =>
    document
      .getElementById("discover")
      ?.scrollIntoView({ behavior: "smooth", block: "start" });
  return {
    auth,
    setAuth,
    providers,
    setProviders,
    total,
    setTotal,
    loading,
    setLoading,
    error,
    setError,
    query,
    setQuery,
    search,
    setSearch,
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
    selected,
    setSelected,
    detailLoading,
    setDetailLoading,
    compare,
    setCompare,
    compareOpen,
    setCompareOpen,
    compareProviders,
    setCompareProviders,
    compareError,
    setCompareError,
    loginOpen,
    setLoginOpen,
    inquiryTarget,
    setInquiryTarget,
    dashboard,
    setDashboard,
    editor,
    setEditor,
    notificationsOpen,
    setNotificationsOpen,
    notifications,
    setNotifications,
    notificationsLoading,
    notificationsError,
    setNotificationsReload,
    toast,
    setToast,
    mobileMenu,
    setMobileMenu,
    reload,
    setReload,
    showProvider,
    toggleCompare,
    contact,
    resetFilters,
    browse,
  };
}
export type MarketplaceState = ReturnType<typeof useMarketplace>;
