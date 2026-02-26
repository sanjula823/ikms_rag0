import { useMemo, useRef, useState } from "react";

type CitationInfo = {
  page: number | null;
  snippet: string | null;
  source: string | null;
};

type QAResponse = {
  answer: string;
  context: string;
  citations: Record<string, CitationInfo> | null;
};

type AnswerPart = {
  text: string;
  citationId?: string;
};

const citationRegex = /\[C\d+\]/g;

const parseAnswer = (answer: string): AnswerPart[] => {
  const parts: AnswerPart[] = [];
  let lastIndex = 0;
  const matches = answer.matchAll(citationRegex);

  for (const match of matches) {
    const index = match.index ?? 0;
    if (index > lastIndex) {
      parts.push({ text: answer.slice(lastIndex, index) });
    }
    const raw = match[0];
    parts.push({ text: raw, citationId: raw.slice(1, -1) });
    lastIndex = index + raw.length;
  }

  if (lastIndex < answer.length) {
    parts.push({ text: answer.slice(lastIndex) });
  }

  return parts;
};

export default function App() {
  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState("");
  const [citations, setCitations] = useState<Record<string, CitationInfo> | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [selectedCitation, setSelectedCitation] = useState<string | null>(null);
  const sourceRefs = useRef<Record<string, HTMLDivElement | null>>({});

  const answerParts = useMemo(() => parseAnswer(answer), [answer]);

  const handleSubmit = async () => {
    if (!question.trim()) {
      setError("Please enter a question.");
      return;
    }

    setLoading(true);
    setError(null);
    setAnswer("");
    setCitations(null);
    setSelectedCitation(null);

    const controller = new AbortController();
    const timer = window.setTimeout(() => controller.abort(), 20000);

    try {
      const response = await fetch("/qa", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ question }),
        signal: controller.signal
      });

      if (!response.ok) {
        const message = await response.text();
        throw new Error(message || "Request failed");
      }

      const data = (await response.json()) as QAResponse;
      setAnswer(data.answer || "No answer returned.");
      setCitations(data.citations);
    } catch (err) {
      const message = err instanceof Error ? err.message : "Unknown error";
      setError(message.includes("aborted") ? "Request timed out." : message);
    } finally {
      window.clearTimeout(timer);
      setLoading(false);
    }
  };

  const handleCitationClick = (citationId: string) => {
    setSelectedCitation(citationId);
    const target = sourceRefs.current[citationId];
    if (target) {
      target.scrollIntoView({ behavior: "smooth", block: "center" });
    }
  };

  return (
    <div className="min-h-screen px-6 py-10">
      <div className="mx-auto max-w-6xl grid gap-8 lg:grid-cols-[1.1fr,0.9fr]">
        <section className="rounded-3xl bg-white/10 backdrop-blur-xl p-8 shadow-glow animate-floatIn">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm uppercase tracking-[0.2em] text-sun">Evidence-aware RAG</p>
              <h1 className="text-3xl lg:text-4xl font-display font-semibold mt-2">
                Ask. Verify. Cite.
              </h1>
              <p className="text-mist/70 mt-3 max-w-xl">
                Every answer is grounded in retrieved chunks. Click citations to explore sources.
              </p>
            </div>
          </div>

          <div className="mt-8 space-y-4">
            <textarea
              className="w-full min-h-[140px] rounded-2xl bg-ink/60 border border-mist/10 p-4 text-mist focus:outline-none focus:ring-2 focus:ring-sun/70"
              placeholder="What do you want to know from your indexed PDFs?"
              value={question}
              onChange={(event) => setQuestion(event.target.value)}
            />
            <div className="flex items-center gap-4">
              <button
                className="rounded-full bg-sun text-ink font-semibold px-6 py-2 transition hover:brightness-110"
                onClick={handleSubmit}
                disabled={loading}
              >
                {loading ? "Working..." : "Submit"}
              </button>
              {loading && (
                <span className="text-mist/70 flex items-center gap-2">
                  <span className="h-2 w-2 rounded-full bg-sun animate-pulseSoft" />
                  Retrieving evidence
                </span>
              )}
            </div>
            {error && <p className="text-clay">{error}</p>}
          </div>

          <div className="mt-10">
            <h2 className="text-xl font-display font-semibold">Answer</h2>
            <div className="mt-4 rounded-2xl bg-ink/50 border border-mist/10 p-6 min-h-[160px]">
              {answer ? (
                <p className="text-mist/90 leading-relaxed">
                  {answerParts.map((part, index) =>
                    part.citationId ? (
                      <button
                        key={`${part.citationId}-${index}`}
                        className={`mx-1 inline-flex items-center rounded-full border px-2 py-0.5 text-xs font-semibold transition ${
                          selectedCitation === part.citationId
                            ? "border-sun text-sun"
                            : "border-mist/30 text-mist/70 hover:border-sun hover:text-sun"
                        }`}
                        onClick={() => handleCitationClick(part.citationId!)}
                        title={`Jump to ${part.citationId}`}
                      >
                        {part.text}
                      </button>
                    ) : (
                      <span key={index}>{part.text}</span>
                    )
                  )}
                </p>
              ) : (
                <p className="text-mist/50">Submit a question to see evidence-backed answers.</p>
              )}
            </div>
          </div>
        </section>

        <aside className="rounded-3xl bg-white/5 backdrop-blur-xl p-6 border border-mist/10 animate-floatIn">
          <div className="flex items-center justify-between">
            <h2 className="text-lg font-display font-semibold">Sources</h2>
            <span className="text-xs uppercase tracking-[0.2em] text-mist/60">
              {citations ? Object.keys(citations).length : 0} chunks
            </span>
          </div>

          <div className="mt-6 space-y-4 max-h-[560px] overflow-y-auto pr-2">
            {citations ? (
              Object.entries(citations).map(([id, info]) => (
                <div
                  key={id}
                  ref={(el) => {
                    sourceRefs.current[id] = el;
                  }}
                  className={`rounded-2xl border p-4 transition ${
                    selectedCitation === id
                      ? "border-sun bg-sun/10"
                      : "border-mist/10 bg-ink/40"
                  }`}
                >
                  <div className="flex items-center justify-between">
                    <span className="text-sm font-semibold text-sun">{id}</span>
                    <span className="text-xs text-mist/70">Page {info.page ?? "?"}</span>
                  </div>
                  <p className="text-xs uppercase tracking-[0.2em] text-mist/60 mt-2">
                    {info.source ?? "Unknown source"}
                  </p>
                  <p
                    className="text-sm text-mist/80 mt-3"
                    title={info.snippet ?? "No snippet"}
                  >
                    {info.snippet ?? "Snippet unavailable."}
                  </p>
                </div>
              ))
            ) : (
              <p className="text-mist/50">Sources will appear after a successful query.</p>
            )}
          </div>
        </aside>
      </div>
    </div>
  );
}
