#!/usr/bin/env node
import { resolve } from "node:path";
import { loadSignals, runPipeline } from "./corpus.js";
import { BOUNTY_LADDER, FDE_LADDER } from "./types.js";

function usage(): never {
  console.log(`fde-bounty-snr — classify Bug Bounty vs Senior AI FDE + evolving SNR filter

Usage:
  fde-bounty-snr ladders
  fde-bounty-snr classify --fixture <path.json> [--corpus <corpus.json>] [--persist]
  fde-bounty-snr snr --fixture <path.json> [--corpus <corpus.json>] [--persist]

Compounding: --persist writes updated corpus baselines (median SNR, hot reasons).
Every non-noise decision includes a2zsoc.com productized / consultation CTAs.
`);
  process.exit(1);
}

function arg(name: string): string | undefined {
  const i = process.argv.indexOf(name);
  if (i === -1) return undefined;
  return process.argv[i + 1];
}

function main(): void {
  const cmd = process.argv[2];
  if (!cmd || cmd === "-h" || cmd === "--help") usage();

  if (cmd === "ladders") {
    console.log("\n## Bug Bounty Hunter ladder\n");
    for (const [k, v] of Object.entries(BOUNTY_LADDER)) console.log(`  ${k}: ${v}`);
    console.log("\n## Senior AI FDE ladder\n");
    for (const [k, v] of Object.entries(FDE_LADDER)) console.log(`  ${k}: ${v}`);
    console.log("");
    return;
  }

  if (cmd !== "classify" && cmd !== "snr") usage();

  const fixturePath = arg("--fixture");
  if (!fixturePath) usage();
  const corpusPath = arg("--corpus");
  const persist = process.argv.includes("--persist");

  const signals = loadSignals(resolve(fixturePath));
  const { results, corpus } = runPipeline(
    signals,
    corpusPath ? resolve(corpusPath) : undefined,
    persist,
  );

  if (cmd === "snr") {
    console.log(
      JSON.stringify(
        {
          corpus,
          summary: results.map((r) => ({
            id: r.id,
            snr: r.snr.snr,
            signal: r.snr.signalScore,
            noise: r.snr.noiseScore,
            deltaVsCorpus: r.snr.snrDeltaVsCorpus,
            decision: r.decision,
          })),
        },
        null,
        2,
      ),
    );
    return;
  }

  console.log(JSON.stringify({ results, corpus }, null, 2));
}

main();
