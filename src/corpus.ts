import { readFileSync, writeFileSync } from "node:fs";
import { decideAll } from "./filter.js";
import { emptyCorpus } from "./snr.js";
import type { CorpusStats, FilterDecision, FilterResult, SignalInput } from "./types.js";

function median(nums: number[]): number {
  if (nums.length === 0) return 1;
  const s = [...nums].sort((a, b) => a - b);
  const mid = Math.floor(s.length / 2);
  return s.length % 2 ? s[mid]! : (s[mid - 1]! + s[mid]!) / 2;
}

/** Ingest scored results → new corpus (compounding leave-behind). */
export function evolveCorpus(
  prev: CorpusStats | null | undefined,
  results: FilterResult[],
  signals: SignalInput[],
): CorpusStats {
  const base = prev ?? emptyCorpus();
  const scores = results.map((r) => r.snr.policyScore);
  const signalsScores = results.map((r) => r.snr.signalScore);
  const noises = results.map((r) => r.snr.noiseScore);

  const decisionCounts: Partial<Record<FilterDecision, number>> = {
    ...base.decisionCounts,
  };
  for (const r of results) {
    decisionCounts[r.decision] = (decisionCounts[r.decision] ?? 0) + 1;
  }

  const reasonCounts = { ...base.reasonCounts };
  for (const r of results) {
    for (const reason of r.level.reasons) {
      reasonCounts[reason] = (reasonCounts[reason] ?? 0) + 1;
    }
  }
  const hotReasons = Object.entries(reasonCounts)
    .sort((a, b) => b[1] - a[1])
    .slice(0, 8)
    .map(([k]) => k);

  const scoreHistogram = [...base.scoreHistogram, ...scores].slice(-1000);

  const n = base.sampleCount + results.length;
  const meanSignal =
    n === 0
      ? 0
      : (base.meanSignal * base.sampleCount +
          signalsScores.reduce((a, b) => a + b, 0)) /
        n;
  const meanNoise =
    n === 0
      ? 0
      : (base.meanNoise * base.sampleCount + noises.reduce((a, b) => a + b, 0)) / n;

  return {
    version: base.version + 1,
    updatedAt: new Date().toISOString(),
    sampleCount: n,
    medianPolicyScore: median(scoreHistogram.length ? scoreHistogram : [base.medianPolicyScore]),
    meanSignal: Math.round(meanSignal * 10000) / 10000,
    meanNoise: Math.round(meanNoise * 10000) / 10000,
    decisionCounts,
    hotReasons,
    scoreHistogram,
    reasonCounts,
  };
}

export function loadCorpus(path: string): CorpusStats {
  try {
    return JSON.parse(readFileSync(path, "utf8")) as CorpusStats;
  } catch {
    return emptyCorpus();
  }
}

export function saveCorpus(path: string, corpus: CorpusStats): void {
  writeFileSync(path, JSON.stringify(corpus, null, 2) + "\n", "utf8");
}

export function loadSignals(path: string): SignalInput[] {
  const raw = JSON.parse(readFileSync(path, "utf8")) as SignalInput[] | { signals: SignalInput[] };
  return Array.isArray(raw) ? raw : raw.signals;
}

export function runPipeline(
  signals: SignalInput[],
  corpusPath?: string,
  persist = false,
): { results: FilterResult[]; corpus: CorpusStats } {
  const prev = corpusPath ? loadCorpus(corpusPath) : emptyCorpus();
  const results = decideAll(signals, prev);
  const corpus = evolveCorpus(prev, results, signals);
  if (persist && corpusPath) saveCorpus(corpusPath, corpus);
  return { results, corpus };
}
