"use client";

import { useEffect, useMemo, useState } from "react";
import { getApiBase, getDocsUrl, getStoredApiBase, setStoredApiBase } from "../lib/api";

export default function IncidentQuickActions() {
  const [service, setService] = useState("payment-service");
  const [message, setMessage] = useState("Database connection timeout");
  const [level, setLevel] = useState<"ERROR" | "WARN" | "INFO">("ERROR");
  const [count, setCount] = useState(5);
  const [busy, setBusy] = useState(false);
  const [result, setResult] = useState<string | null>(null);
  const [apiBaseInput, setApiBaseInput] = useState("");
  const apiBase = useMemo(() => getApiBase(), []);
  const docsUrl = useMemo(() => getDocsUrl(), [apiBase]);
  const [useCustomBase, setUseCustomBase] = useState<boolean>(false);

  useEffect(() => {
    const stored = getStoredApiBase();
    if (stored) {
      setUseCustomBase(true);
      setApiBaseInput(stored);
    } else {
      setApiBaseInput(apiBase);
    }
  }, [apiBase]);

  async function postEvent() {
    setBusy(true);
    setResult(null);
    try {
  const base = getApiBase();
  const res = await fetch(`${base}/api/v1/events`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ service, level, message }),
      });
      const data = await res.json().catch(() => ({}));
      setResult(res.ok ? "Event sent ✅" : `Failed ❌: ${res.status} ${JSON.stringify(data)}`);
    } catch (e: any) {
      setResult(`Error ❌: ${e?.message || e}`);
    } finally {
      setBusy(false);
    }
  }

  async function simulateIncident() {
    setBusy(true);
    setResult(null);
    try {
      const base = getApiBase();
      const sends = Array.from({ length: count }).map((_, i) =>
        fetch(`${base}/api/v1/events`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            service,
            level: "ERROR",
            message: `${message} (#${i + 1})`,
          }),
        })
      );
      const responses = await Promise.all(sends);
      const ok = responses.every((r) => r.ok);
      setResult(ok ? `Simulated ${count} ERROR events ✅` : `Some requests failed ❌`);
    } catch (e: any) {
      setResult(`Error ❌: ${e?.message || e}`);
    } finally {
      setBusy(false);
    }
  }

  return (
    <div className="bg-white rounded-lg shadow border border-gray-200 p-4 space-y-3">
      <div className="flex items-center justify-between">
        <h3 className="font-semibold">Quick Actions</h3>
        <a
          href={docsUrl}
          target="_blank"
          rel="noreferrer"
          className="text-sm text-blue-600 hover:underline"
        >
          API Docs ↗
        </a>
      </div>

      {/* API Base configuration */}
      <div className="flex flex-col md:flex-row md:items-center gap-2 text-sm">
        <label className="text-gray-600">API URL</label>
        <input
          className="border rounded px-3 py-2 flex-1"
          value={apiBaseInput}
          onChange={(e) => setApiBaseInput(e.target.value)}
          placeholder="https://your-backend-domain"
        />
        <button
          className="px-3 py-2 bg-gray-100 rounded border text-gray-800"
          onClick={() => {
            const v = apiBaseInput.replace(/\/+$/, "");
            setStoredApiBase(v);
            setResult(`API base set to ${v}`);
          }}
        >
          Save
        </button>
        <button
          className="px-3 py-2 bg-white rounded border text-gray-600"
          onClick={() => {
            // Clear override to use env default
            setStoredApiBase("");
            try { localStorage.removeItem("opsai_api_base"); } catch {}
            setApiBaseInput(getApiBase());
            setResult("API base reset to default");
          }}
        >
          Use default
        </button>
      </div>
      {typeof window !== 'undefined' && window.location.hostname !== 'localhost' && apiBaseInput.includes('localhost') && (
        <div className="text-xs text-yellow-700 bg-yellow-50 border border-yellow-200 rounded p-2">
          Warning: Your API URL points to localhost, which won't work from a deployed site. Set your live backend URL above.
        </div>
      )}

      <div className="grid grid-cols-1 md:grid-cols-4 gap-3">
        <input
          className="border rounded px-3 py-2"
          value={service}
          onChange={(e) => setService(e.target.value)}
          placeholder="service (e.g., payment-service)"
        />
        <select
          className="border rounded px-3 py-2"
          value={level}
          onChange={(e) => setLevel(e.target.value as any)}
        >
          <option>ERROR</option>
          <option>WARN</option>
          <option>INFO</option>
        </select>
        <input
          className="border rounded px-3 py-2 md:col-span-2"
          value={message}
          onChange={(e) => setMessage(e.target.value)}
          placeholder="message"
        />
      </div>

      <div className="flex items-center gap-3">
        <button
          disabled={busy}
          onClick={postEvent}
          className="bg-gray-900 text-white px-4 py-2 rounded disabled:opacity-50"
        >
          Send Event
        </button>

        <input
          type="number"
          min={1}
          className="border rounded px-3 py-2 w-24"
          value={count}
          onChange={(e) => setCount(parseInt(e.target.value || "1", 10))}
        />
        <button
          disabled={busy}
          onClick={simulateIncident}
          className="bg-indigo-600 text-white px-4 py-2 rounded disabled:opacity-50"
        >
          Simulate Incident
        </button>
      </div>

      {result && <div className="text-sm text-gray-700">{result}</div>}
    </div>
  );
}
