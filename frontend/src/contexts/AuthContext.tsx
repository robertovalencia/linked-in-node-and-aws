import type { PropsWithChildren } from "react";
import { createContext, useCallback, useEffect, useState } from "react";
import { identityService } from "../services/marketplace";
import type { Auth } from "../types/marketplace";
export const TOKEN_KEY = "expertly-node-aws-token";
export const AuthContext = createContext<{
  auth: Auth | null;
  setAuth: (auth: Auth | null) => void;
  restoring: boolean;
} | null>(null);
export function AuthProvider({ children }: PropsWithChildren) {
  const [auth, updateAuth] = useState<Auth | null>(null);
  const [restoring, setRestoring] = useState(true);
  const setAuth = useCallback((value: Auth | null) => {
    updateAuth(value);
    if (value) localStorage.setItem(TOKEN_KEY, value.token);
    else localStorage.removeItem(TOKEN_KEY);
  }, []);
  useEffect(() => {
    const controller = new AbortController();
    const token = localStorage.getItem(TOKEN_KEY);
    if (!token) {
      setRestoring(false);
      return;
    }
    identityService
      .me(token, controller.signal)
      .then((me) => {
        if (
          !controller.signal.aborted &&
          localStorage.getItem(TOKEN_KEY) === token
        )
          updateAuth({ ...me, token });
      })
      .catch((error) => {
        if (
          error.name !== "AbortError" &&
          localStorage.getItem(TOKEN_KEY) === token
        )
          localStorage.removeItem(TOKEN_KEY);
      })
      .finally(() => {
        if (!controller.signal.aborted) setRestoring(false);
      });
    return () => controller.abort();
  }, []);
  return (
    <AuthContext.Provider value={{ auth, setAuth, restoring }}>
      {children}
    </AuthContext.Provider>
  );
}
