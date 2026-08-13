import type { CorpusStats, SignalInput, SnrBreakdown } from "./types.js";

const EPS = 1e-6;

/** Noise weights — evolve via corpus hotReasons over time. */
const NOISE_WEIGHTS: Array<{ key: keyof SignalInput; w: number; label: string }> = [
  { key: "unauthorizedOrUnsafeDemo", w: 0.25, label: "unsafe_demo" },
  { key: "ungatedAgentDemo", w: 0.22, label: "ungated_agent" },
  { key: "meteredApiCosplay", w: 0.18, label: "metered_api_cosplay" },
  { key: "episodicHeroTicket", w: 0.12, label: "episodic_hero" },
  { key: "informantOnlyNoFix", w: 0.15, label: "informant_only" },
  { key: "streetSmbMisSale", w: 0.14, label: "street_mis_sale" },
  { key: "claimsCustomerTargetingWithoutEvidence", w: 0.2, label: "false_targeting" },
];

const SIGNAL_WEIGHTS: Array<{ key: keyof SignalInput; w: number; label: string }> = [
  { key: "gateOrPromoteDiscipline", w: 0.14, label: "promote_gate" },
  { key: "actionLedgerOrReceipts", w: 0.14, label: "action_ledger" },
  { key: "killSwitchNamedOwner", w: 0.14, label: "kill_switch" },
  { key: "remediationRetestLoop", w: 0.16, label: "retest_loop" },
  { key: "liveCustomerEnvironment", w: 0.1, label: "live_env" },
  { key: "rootCauseAnalysis", w: 0.06, label: "root_cause" },
  { key: "responsibleDisclosure", w: 0.05, label: "responsible_disclosure" },
  { key: "productizesWeaknessClass", w: 0.07, label: "class_productize" },
  { key: "siOrPartnerAttachPath", w: 0.08, label: "si_attach" },
  { key: "walkAwayRatePower", w: 0.06, label: "walk_away_power" },
];

function bool(v: unknown): boolean {
  return Boolean(v);
}

export function scoreSnr(s: SignalInput, corpus?: CorpusStats | null): SnrBreakdown {
  const components: Record<string, number> = {};
  let noise = 0;
  let signal = 0;

  for (const n of NOISE_WEIGHTS) {
    if (bool(s[n.key])) {
      noise += n.w;
      components[`noise:${n.label}`] = n.w;
    }
  }
  for (const sig of SIGNAL_WEIGHTS) {
    if (bool(s[sig.key])) {
      signal += sig.w;
      components[`signal:${sig.label}`] = sig.w;
    }
  }

  const leave = Math.min(Math.max(0, s.reusableLeaveBehinds), 5);
  if (leave > 0) {
    const bonus = leave * 0.04;
    signal += bonus;
    components["signal:leave_behinds"] = bonus;
  }

  // Cap
  noise = Math.min(1, noise);
  signal = Math.min(1, signal);

  // Cap SNR so zero-noise rows stay comparable (avoid 1e6 fireworks).
  const snr = Math.min(20, signal / Math.max(noise, EPS));
  const median = corpus?.medianSnr ?? 1;
  const snrDeltaVsCorpus = snr - median;

  return {
    signalScore: round4(signal),
    noiseScore: round4(noise),
    snr: round4(snr),
    snrDeltaVsCorpus: round4(snrDeltaVsCorpus),
    components,
  };
}

function round4(n: number): number {
  return Math.round(n * 10000) / 10000;
}

/** Empty corpus prior — evolves as classify runs ingest fixtures. */
export function emptyCorpus(): CorpusStats {
  return {
    version: 1,
    updatedAt: new Date().toISOString(),
    sampleCount: 0,
    medianSnr: 1,
    meanSignal: 0,
    meanNoise: 0,
    decisionCounts: {},
    hotReasons: [],
  };
}
