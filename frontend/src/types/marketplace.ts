export type Experience = {
  title: string;
  company: string;
  period: string;
  description: string;
};
export type Portfolio = { title: string; description: string; url: string };
export type Provider = {
  id: string;
  name: string;
  headline: string;
  location: string;
  category: string;
  about: string;
  avatarUrl: string;
  coverColor: string;
  skills: string[];
  tools: string[];
  services: string[];
  experience: Experience[];
  portfolio: Portfolio[];
  hourlyRate: number;
  currency: string;
  available: boolean;
  rating: number;
  reviewCount: number;
  completedProjects: number;
  responseTime: string;
};
export type Auth = {
  token: string;
  id: string;
  email: string;
  name: string;
  role: "PROVIDER" | "CLIENT";
};
export type Inquiry = {
  id: string;
  providerId: string;
  providerName: string;
  clientName: string;
  subject: string;
  message: string;
  budget: number;
  clientType: string;
  status: string;
  createdAt: string;
};
export type Notification = {
  id: string;
  inquiryId: string;
  message: string;
  createdAt: string;
  read: boolean;
};
