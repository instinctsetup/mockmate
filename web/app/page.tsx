"use client";
import { useEffect, useState } from "react";

const API = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8101";

type Intel = { title: string; url: string; snippet: string; kind: string; source: string; model_written: boolean };
type Q = { id: string; title: string; difficulty: string; topics: string[]; url: string; companies: string[]; model_written: boolean };
type QDetail = Q & { solution: string };

export default function Home() {
  const [company, setCompany] = useState("razorpay");
  const [prep, setPrep] = useState<{ intel: Intel[]; oa_questions: Q[]; provider: string; note: string } | null>(null);
  const [bank, setBank] = useState<Q[]>([]);
  const [topic, setTopic] = useState("");
  const [detail, setDetail] = useState<QDetail | null>(null);
  const [health, setHealth] = useState<{ postgres: boolean; redis: boolean } | null>(null);

  const loadPrep = async () => {
    const r = await fetch(`${API}/api/prep/${encodeURIComponent(company)}`);
    setPrep(await r.json());
  };
  const loadBank = async (t = "") => {
    const r = await fetch(`${API}/api/oa/questions${t ? `?topic=${t}` : ""}`);
    const d = await r.json();
    setBank(d.questions);
  };
  const loadDetail = async (id: string) => {
    const r = await fetch(`${API}/api/oa/questions/${id}`);
    setDetail((await r.json()).question);
  };

  useEffect(() => {
    fetch(`${API}/api/health`).then(r => r.json()).then(setHealth).catch(() => {});
    loadPrep();
    loadBank();
  }, []);

  return (
    <>
      <header>
        <h1>mock<span>mate</span></h1>
        <p>interview prep grounded in sources</p>
        {health && <p>· postgres: {health.postgres ? "on" : "fallback"} · redis: {health.redis ? "on" : "fallback"}</p>}
      </header>
      <main>
        <section className="card">
          <h2>Company prep</h2>
          <div className="row">
            <input value={company} onChange={e => setCompany(e.target.value)} placeholder="company…" />
            <button onClick={loadPrep}>Load prep</button>
          </div>
          {prep && (
            <>
              {prep.intel.map((i, k) => (
                <div className="item" key={k}>
                  <a href={i.url} target="_blank">{i.title}</a>
                  <p>{i.snippet}</p>
                  <span className="badge src">source: {i.source}</span>
                  <span className="badge topic">{i.kind}</span>
                </div>
              ))}
              {prep.oa_questions.length > 0 && (
                <>
                  <h2 style={{ marginTop: 16 }}>Tagged OA questions ({prep.oa_questions.length})</h2>
                  {prep.oa_questions.map(q => (
                    <div className="item q" key={q.id} onClick={() => loadDetail(q.id)}>
                      <a href={q.url} target="_blank" onClick={e => e.stopPropagation()}>{q.title}</a>
                      <div><span className={`badge ${q.difficulty}`}>{q.difficulty}</span>
                        {q.topics.map(t => <span className="badge topic" key={t}>{t}</span>)}</div>
                    </div>
                  ))}
                </>
              )}
              <p className="note">{prep.note}. Provider: {prep.provider}.</p>
            </>
          )}
        </section>

        <section className="card">
          <h2>OA question bank</h2>
          <div className="row">
            <select value={topic} onChange={e => { setTopic(e.target.value); loadBank(e.target.value); }}>
              <option value="">all topics</option>
              <option value="arrays">arrays</option>
              <option value="graphs">graphs</option>
              <option value="dp">dp</option>
              <option value="trees">trees</option>
              <option value="strings">strings</option>
              <option value="design">design</option>
            </select>
          </div>
          {bank.map(q => (
            <div className="item q" key={q.id} onClick={() => loadDetail(q.id)}>
              <a href={q.url} target="_blank" onClick={e => e.stopPropagation()}>{q.title}</a>
              <div>
                <span className={`badge ${q.difficulty}`}>{q.difficulty}</span>
                {q.topics.map(t => <span className="badge topic" key={t}>{t}</span>)}
                {q.companies.slice(0, 3).map(c => <span className="badge src" key={c}>{c}</span>)}
              </div>
            </div>
          ))}
          <p className="note">Company tags are community-reported, not verified. Every question links to its public problem page.</p>
        </section>

        {detail && (
          <section className="card wide">
            <h2>{detail.title}</h2>
            <div className="row">
              <span className={`badge ${detail.difficulty}`}>{detail.difficulty}</span>
              <a href={detail.url} target="_blank" style={{ color: "#6ea8fe", fontSize: 13 }}>{detail.url}</a>
            </div>
            <span className="badge model">model-written answer</span>
            <div className="sol">{detail.solution}</div>
            <p className="note">This solution is written by an AI model and labeled as such. Verify against the linked source.</p>
            <div className="row" style={{ marginTop: 12 }}>
              <button onClick={async () => {
                await fetch(`${API}/api/sessions`, { method: "POST", headers: { "Content-Type": "application/json" },
                  body: JSON.stringify({ company, notes: `practiced ${detail.id}` }) });
                alert("session logged");
              }}>Log practice session</button>
              <button onClick={() => setDetail(null)} style={{ background: "#2a3546", color: "#e6e9ef" }}>Close</button>
            </div>
          </section>
        )}
      </main>
    </>
  );
}
