import { LoaderCircle } from "lucide-react";
export function Loading() {
  return (
    <div className="loading">
      <LoaderCircle className="spin" size={25} /> Loading…
    </div>
  );
}
