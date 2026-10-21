import { useState } from "react";
import type { Provider } from "../../types/marketplace";
export function Avatar({
  p,
  size = "normal",
}: {
  p: Pick<Provider, "name" | "avatarUrl">;
  size?: string;
}) {
  const [failed, setFailed] = useState(false);
  return (
    <span className={`avatar avatar-${size}`}>
      {p.avatarUrl && !failed ? (
        <img src={p.avatarUrl} alt={p.name} onError={() => setFailed(true)} />
      ) : (
        <span>
          {p.name
            .split(" ")
            .map((n) => n[0])
            .slice(0, 2)
            .join("")}
        </span>
      )}
    </span>
  );
}
