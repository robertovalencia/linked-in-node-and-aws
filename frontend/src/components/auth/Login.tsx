import {
  ArrowRight,
  BriefcaseBusiness,
  Building2,
  Code2,
  User,
} from "lucide-react";
import { useEffect, useRef, useState } from "react";
import { Modal } from "../../components/common/Modal";
import { identityService } from "../../services/marketplace";
import type { Auth } from "../../types/marketplace";
export function Login({
  onClose,
  onLogin,
}: {
  onClose: () => void;
  onLogin: (a: Auth) => void;
}) {
  const [email, setEmail] = useState("company@demo.local");
  const [password, setPassword] = useState("DemoPass123!");
  const [error, setError] = useState("");
  const [busy, setBusy] = useState(false);
  const pending = useRef<AbortController | null>(null);
  useEffect(() => () => pending.current?.abort(), []);
  const close = () => {
    pending.current?.abort();
    onClose();
  };
  return (
    <Modal title="Welcome back." onClose={close}>
      <form
        className="modal-body form"
        onSubmit={async (e) => {
          e.preventDefault();
          if (pending.current && !pending.current.signal.aborted && busy)
            return;
          pending.current?.abort();
          const controller = new AbortController();
          pending.current = controller;
          setBusy(true);
          setError("");
          try {
            const auth = await identityService.login(
              email,
              password,
              controller.signal,
            );
            if (!controller.signal.aborted && pending.current === controller)
              onLogin(auth);
          } catch (e) {
            if (!controller.signal.aborted) setError((e as Error).message);
          } finally {
            if (!controller.signal.aborted) setBusy(false);
          }
        }}
      >
        <p className="muted">Sign in to make your next great connection.</p>
        <label>
          Email address
          <input
            type="email"
            autoComplete="username"
            required
            value={email}
            onChange={(e) => setEmail(e.target.value)}
          />
        </label>
        <label>
          Password
          <input
            type="password"
            autoComplete="current-password"
            required
            value={password}
            onChange={(e) => setPassword(e.target.value)}
          />
        </label>
        {error && (
          <p role="alert" className="form-error">
            {error}
          </p>
        )}
        <button
          type="submit"
          className="button button-primary button-full"
          disabled={busy}
        >
          {busy ? "Signing in…" : "Sign in"} <ArrowRight size={17} />
        </button>
        <div className="demo-accounts">
          <h4>Explore the local demo</h4>
          <p>Choose an account. The demo password is prefilled.</p>
          <div>
            {[
              {
                email: "company@demo.local",
                label: "Company",
                icon: Building2,
              },
              {
                email: "individual@demo.local",
                label: "Individual",
                icon: User,
              },
              { email: "ava@demo.local", label: "Ava · Provider", icon: Code2 },
              {
                email: "leo@demo.local",
                label: "Leo · Provider",
                icon: BriefcaseBusiness,
              },
            ].map((a) => (
              <button
                type="button"
                className={
                  email === a.email ? "demo-account selected" : "demo-account"
                }
                key={a.email}
                onClick={() => {
                  setEmail(a.email);
                  setPassword("DemoPass123!");
                }}
              >
                <a.icon size={16} />
                {a.label}
              </button>
            ))}
          </div>
          <small>
            Demo accounts only. Registration is outside this local prototype.
          </small>
        </div>
      </form>
    </Modal>
  );
}
