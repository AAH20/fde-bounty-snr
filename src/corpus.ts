import { readFileSync, writeFileSync } from "node:fs";
import { decideAll } from "./filter.js";
import { emptyCorpus, scoreSnr } from "./snr.js";
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
  const snrs = results.map((r) => r.snr.snr);
  const signalsScores = results.map((r) => r.snr.signalScore);
  const noises = results.map((r) => r.snr.noiseScore);

  const decisionCounts: Partial<Record<FilterDecision, number>> = {
    ...base.decisionCounts,
  };
  for (const r of results) {
    decisionCounts[r.decision] = (decisionCounts[r.decision] ?? 0) + 1;
  }

  const reasonFreq = new Map<string, number>();
  for (const r of results) {
    for (const reason of r.level.reasons) {
      reasonFreq.set(reason, (reasonFreq.get(reason) ?? 0) + 1);
    }
  }
  const hotReasons = [...reasonFreq.entries()]
    .sort((a, b) => b[1] - a[1])
    .slice(0, 8)
    .map(([k]) => k);

  // Recompute SNR with previous median for delta education (side-effect free on scoring)
  for (let i = 0; i < signals.length; i++) {
    scoreSnr(signals[i]!, base);
  }

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
    medianSnr: median(snrs.length ? snrs : [base.medianSnr]),
    meanSignal: Math.round(meanSignal * 10000) / 10000,
    meanNoise: Math.round(meanNoise * 10000) / 10000,
    decisionCounts,
    hotReasons,
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
