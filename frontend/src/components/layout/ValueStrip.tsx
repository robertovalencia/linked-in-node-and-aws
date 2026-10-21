import { Mail, ShieldCheck, User } from "lucide-react";
export function ValueStrip() {
  return (
    <section className="value-strip" aria-label="Marketplace benefits">
      <div>
        <ShieldCheck />
        <span>Expertise you can explore</span>
      </div>
      <div>
        <User />
        <span>People, beyond the profile</span>
      </div>
      <div>
        <Mail />
        <span>Direct conversations. Real connections.</span>
      </div>
    </section>
  );
}
