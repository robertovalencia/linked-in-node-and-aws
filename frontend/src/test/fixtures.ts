import type { Provider } from "../types/marketplace";
export const ava: Provider = {
  id: "ava",
  name: "Ava Martinez",
  headline: "React product engineer",
  location: "Austin, TX",
  category: "Software Development",
  about: "I help teams ship useful products.",
  avatarUrl: "/assets/ava-martinez.jpg",
  coverColor: "#dce9e5",
  skills: ["React", "Node.js", "TypeScript"],
  tools: ["VS Code"],
  services: ["Web applications"],
  experience: [
    {
      title: "Engineer",
      company: "Studio",
      period: "2022–present",
      description: "Build applications.",
    },
  ],
  portfolio: [
    {
      title: "Portal",
      description: "A customer portal.",
      url: "https://example.com",
    },
  ],
  hourlyRate: 95,
  currency: "USD",
  available: true,
  rating: 4.9,
  reviewCount: 15,
  completedProjects: 20,
  responseTime: "Within one day",
};
export const leo: Provider = {
  ...ava,
  id: "leo",
  name: "Leo Chen",
  headline: "DevOps engineer",
};
export const reply = (data: unknown, status = 200) =>
  new Response(status === 204 ? null : JSON.stringify(data), {
    status,
    headers: { "Content-Type": "application/json" },
  });
