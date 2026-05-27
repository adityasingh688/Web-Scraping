import React from "react";
import { useEffect, useMemo, useState } from "react";
import { BarChart3, Building2, Database, RefreshCw } from "lucide-react";
import {
  Bar,
  BarChart,
  CartesianGrid,
  Cell,
  Legend,
  Pie,
  PieChart,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";
import { fetchDashboardSummary } from "./api";

const COLORS = ["#2563eb", "#16a34a", "#dc2626", "#9333ea", "#f59e0b", "#0891b2", "#be185d", "#4d7c0f"];

function StatCard({ icon: Icon, label, value }) {
  return (
    <section className="stat-card">
      <div className="stat-icon">
        <Icon size={20} />
      </div>
      <div>
        <p>{label}</p>
        <strong>{value}</strong>
      </div>
    </section>
  );
}

function ChartPanel({ title, children }) {
  return (
    <section className="chart-panel">
      <h2>{title}</h2>
      <div className="chart-wrap">{children}</div>
    </section>
  );
}

export default function App() {
  const [summary, setSummary] = useState(null);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(true);

  async function loadSummary() {
    setLoading(true);
    setError("");
    try {
      setSummary(await fetchDashboardSummary());
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    loadSummary();
  }, []);

  const totals = useMemo(() => {
    if (!summary) {
      return { listings: 0, cities: 0, categories: 0, sources: 0 };
    }
    return {
      listings: summary.city_wise.reduce((sum, item) => sum + item.count, 0),
      cities: summary.city_wise.length,
      categories: summary.category_wise.length,
      sources: summary.source_wise.length,
    };
  }, [summary]);

  return (
    <main>
      <header className="topbar">
        <div>
          <span className="eyebrow">Business intelligence</span>
          <h1>Business Listings Dashboard</h1>
        </div>
        <button type="button" onClick={loadSummary} aria-label="Refresh dashboard data">
          <RefreshCw size={18} />
          Refresh
        </button>
      </header>

      {error && <div className="alert">{error}</div>}

      <section className="stats-grid">
        <StatCard icon={Building2} label="Total listings" value={totals.listings} />
        <StatCard icon={BarChart3} label="Cities" value={totals.cities} />
        <StatCard icon={Database} label="Categories" value={totals.categories} />
        <StatCard icon={Database} label="Sources" value={totals.sources} />
      </section>

      {loading && <div className="loading">Loading dashboard data...</div>}

      {summary && !loading && (
        <section className="dashboard-grid">
          <ChartPanel title="City-wise Business Count">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={summary.city_wise}>
                <CartesianGrid strokeDasharray="3 3" vertical={false} />
                <XAxis dataKey="name" tickLine={false} axisLine={false} />
                <YAxis allowDecimals={false} tickLine={false} axisLine={false} />
                <Tooltip />
                <Bar dataKey="count" fill="#2563eb" radius={[6, 6, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </ChartPanel>

          <ChartPanel title="Category-wise Business Count">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={summary.category_wise} layout="vertical" margin={{ left: 28 }}>
                <CartesianGrid strokeDasharray="3 3" horizontal={false} />
                <XAxis type="number" allowDecimals={false} tickLine={false} axisLine={false} />
                <YAxis dataKey="name" type="category" width={120} tickLine={false} axisLine={false} />
                <Tooltip />
                <Bar dataKey="count" fill="#16a34a" radius={[0, 6, 6, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </ChartPanel>

          <ChartPanel title="Source-wise Business Count">
            <ResponsiveContainer width="100%" height="100%">
              <PieChart>
                <Pie data={summary.source_wise} dataKey="count" nameKey="name" outerRadius={105} label>
                  {summary.source_wise.map((entry, index) => (
                    <Cell key={entry.name} fill={COLORS[index % COLORS.length]} />
                  ))}
                </Pie>
                <Tooltip />
                <Legend />
              </PieChart>
            </ResponsiveContainer>
          </ChartPanel>
        </section>
      )}
    </main>
  );
}
