import type { CorpusStats, SignalInput, SnrBreakdown } from "./types.js";

/** Versioned policy weights. They are transparent hypotheses, not trained coefficients. */
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

  const asserted = [...SIGNAL_WEIGHTS, ...NOISE_WEIGHTS]
    .filter((item) => bool(s[item.key]))
    .map((item) => String(item.key));
  const evidenced = asserted.filter((key) => Boolean(s.evidence?.[key]?.trim())).length;
  const evidenceCompleteness = asserted.length === 0 ? 0 : evidenced / asserted.length;
  const policyScore = Math.max(0, Math.min(1, (signal - noise + 1) / 2)) * evidenceCompleteness;
  const median = corpus?.medianPolicyScore ?? 0.5;

  return {
    signalScore: round4(signal),
    noiseScore: round4(noise),
    policyScore: round4(policyScore),
    deltaVsCorpus: round4(policyScore - median),
    evidenceCompleteness: round4(evidenceCompleteness),
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
    medianPolicyScore: 0.5,
    meanSignal: 0,
    meanNoise: 0,
    decisionCounts: {},
    hotReasons: [],
    scoreHistogram: [],
    reasonCounts: {},
  };
}
