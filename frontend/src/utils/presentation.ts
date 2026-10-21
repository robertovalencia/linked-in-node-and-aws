import {
  BriefcaseBusiness,
  ChartNoAxesCombined,
  Code2,
  Palette,
} from "lucide-react";
export const categories = [
  { name: "All services", icon: BriefcaseBusiness },
  { name: "Software Development", label: "Development", icon: Code2 },
  { name: "IT Consulting", label: "IT consulting", icon: BriefcaseBusiness },
  { name: "Design", icon: Palette },
  { name: "Marketing", icon: ChartNoAxesCombined },
];
export const money = (n: number) =>
  new Intl.NumberFormat("en-US", {
    style: "currency",
    currency: "USD",
    maximumFractionDigits: 0,
  }).format(n);
export const date = (s: string) =>
  new Date(s).toLocaleDateString("en-US", {
    month: "short",
    day: "numeric",
    year: "numeric",
  });
