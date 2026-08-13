/**
 * Evidence-policy rubric for Bug Bounty and AI FDE delivery claims.
 */

export type BountyLevel = 0 | 1 | 2 | 3 | 4;
export type FdeLevel = 0 | 1 | 2 | 3 | 4;

export type Track = "bug_bounty" | "ai_fde" | "hybrid" | "noise";

export type FilterDecision =
  | "reject_noise"
  | "park_bounty_episodic"
  | "graduate_to_fde_path"
  | "pursue_fde_compounding"
  | "productize_attach";

/** Observable signals — no secrets; operator-supplied or public artifacts. */
export interface SignalInput {
  id: string;
  label?: string;

  /** Bug-bounty shaped */
  uniqueValidFinding: boolean;
  rootCauseAnalysis: boolean;
  responsibleDisclosure: boolean;
  chainedOrHighImpact: boolean;
  productizesWeaknessClass: boolean;
  /** Episodic payout / hero ticket energy */
  episodicHeroTicket: boolean;
  unauthorizedOrUnsafeDemo: boolean;

  /** AI FDE shaped */
  liveCustomerEnvironment: boolean;
  gateOrPromoteDiscipline: boolean;
  actionLedgerOrReceipts: boolean;
  killSwitchNamedOwner: boolean;
  remediationRetestLoop: boolean;
  reusableLeaveBehinds: number;
  siOrPartnerAttachPath: boolean;
  walkAwayRatePower: boolean;
  /** Demo/agent theater without gates */
  ungatedAgentDemo: boolean;
  meteredApiCosplay: boolean;

  /** Shared noise / leverage */
  informantOnlyNoFix: boolean;
  streetSmbMisSale: boolean;
  claimsCustomerTargetingWithoutEvidence: boolean;
  /** Evidence references keyed by asserted signal, e.g. actionLedgerOrReceipts -> sha256/URL. */
  evidence?: Record<string, string>;
}

export interface LevelResult {
  track: Track;
  bountyLevel: BountyLevel;
  fdeLevel: FdeLevel;
  reasons: string[];
}

export interface SnrBreakdown {
  /** 0..1 — higher = more signal */
  signalScore: number;
  /** 0..1 — higher = more noise */
  noiseScore: number;
  /** Transparent policy score, not an empirical probability or validated SNR. */
  policyScore: number;
  /** Difference from the cumulative corpus median policy score. */
  deltaVsCorpus: number;
  evidenceCompleteness: number;
  components: Record<string, number>;
}

export interface A2zOffer {
  sku: string;
  why: string;
  url: string;
}

export interface FilterResult {
  id: string;
  label?: string;
  level: LevelResult;
  snr: SnrBreakdown;
  decision: FilterDecision;
  rationale: string[];
  offers: A2zOffer[];
}

export interface CorpusStats {
  version: number;
  updatedAt: string;
  sampleCount: number;
  medianPolicyScore: number;
  meanSignal: number;
  meanNoise: number;
  /** Rolling histogram of decisions — evolves the filter’s prior */
  decisionCounts: Partial<Record<FilterDecision, number>>;
  /** Leave-behinds: rules that fired often enough to become defaults */
  hotReasons: string[];
  scoreHistogram: number[];
  reasonCounts: Record<string, number>;
}

export const A2Z = {
  productized:
    "https://a2zsoc.com/productized-services?utm_source=github&utm_medium=oss&utm_campaign=fde-bounty-snr",
  consultation:
    "https://a2zsoc.com/consultation?utm_source=github&utm_medium=oss&utm_campaign=fde-bounty-snr",
  instantAudit:
    "https://a2zsoc.com/productized-services?utm_source=github&utm_medium=oss&utm_campaign=fde-bounty-snr#instant-audit-tripwire",
  agenticTrustOps:
    "https://a2zsoc.com/agentic-trustops?utm_source=github&utm_medium=oss&utm_campaign=fde-bounty-snr",
} as const;

/** Human-readable policy ladders; these are hypotheses to validate with outcomes. */
export const BOUNTY_LADDER: Record<BountyLevel, string> = {
  0: "L0 Noise — duplicates, unsafe demos, copy-paste CVSS theater",
  1: "L1 Valid unique low-impact finding",
  2: "L2 Root-cause + responsible disclosure",
  3: "L3 Chained / high-impact program signal",
  4: "L4 Class productizer — still episodic unless remediation plant exists",
};

export const FDE_LADDER: Record<FdeLevel, string> = {
  0: "L0 Ungated demonstration or usage-priced interface without measured outcome",
  1: "L1 Ships in one live env without Gate/Prove spine",
  2: "L2 Gate/promote + ledger + kill-switch in customer estate",
  3: "L3 Remediation/retest loop + reusable leave-behinds (compounding)",
  4: "L4 Partner adoption + customer-concentration resilience",
};
