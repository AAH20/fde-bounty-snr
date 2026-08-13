import type { BountyLevel, FdeLevel, LevelResult, SignalInput, Track } from "./types.js";
import { BOUNTY_LADDER, FDE_LADDER } from "./types.js";

export function classifyBountyLevel(s: SignalInput): { level: BountyLevel; reasons: string[] } {
  const reasons: string[] = [];
  if (s.unauthorizedOrUnsafeDemo && !s.responsibleDisclosure) {
    reasons.push("unsafe/unauthorized demo without responsible path → L0");
    return { level: 0, reasons };
  }
  if (!s.uniqueValidFinding && s.episodicHeroTicket) {
    reasons.push("hero ticket without unique valid finding → L0");
    return { level: 0, reasons };
  }
  if (!s.uniqueValidFinding) {
    reasons.push("no unique valid finding → L0");
    return { level: 0, reasons };
  }

  let level: BountyLevel = 1;
  reasons.push("unique valid finding → ≥L1");

  if (s.rootCauseAnalysis && s.responsibleDisclosure) {
    level = 2;
    reasons.push("root-cause + responsible disclosure → L2");
  }
  if (s.chainedOrHighImpact && level >= 2) {
    level = 3;
    reasons.push("chained/high-impact → L3");
  }
  if (s.productizesWeaknessClass && level >= 3) {
    level = 4;
    reasons.push("productizes weakness class → L4 (still episodic without plant)");
  } else if (s.productizesWeaknessClass && level < 3) {
    reasons.push("class productizing noted but impact/disclosure ladder incomplete");
  }

  reasons.push(BOUNTY_LADDER[level]);
  return { level, reasons };
}

export function classifyFdeLevel(s: SignalInput): { level: FdeLevel; reasons: string[] } {
  const reasons: string[] = [];

  if (s.ungatedAgentDemo || s.meteredApiCosplay) {
    reasons.push("ungated demonstration or usage-priced interface without measured outcome → FDE L0");
    return { level: 0, reasons };
  }
  if (s.claimsCustomerTargetingWithoutEvidence) {
    reasons.push("customer-targeting claim without evidence → FDE L0 noise");
    return { level: 0, reasons };
  }

  if (!s.liveCustomerEnvironment) {
    reasons.push("no live customer environment → FDE L0/lab");
    return { level: 0, reasons };
  }

  let level: FdeLevel = 1;
  reasons.push("live customer environment → ≥FDE L1");

  const gateSpine =
    s.gateOrPromoteDiscipline && s.actionLedgerOrReceipts && s.killSwitchNamedOwner;
  if (gateSpine) {
    level = 2;
    reasons.push("Gate/Prove spine (promote + ledger + kill-switch) → FDE L2");
  }

  if (level >= 2 && s.remediationRetestLoop && s.reusableLeaveBehinds >= 1) {
    level = 3;
    reasons.push("remediation/retest + leave-behinds → FDE L3 compounding");
  }

  if (level >= 3 && s.siOrPartnerAttachPath && s.walkAwayRatePower) {
    level = 4;
    reasons.push("partner adoption + customer-concentration resilience → FDE L4");
  }

  reasons.push(FDE_LADDER[level]);
  return { level, reasons };
}

export function classifySignal(s: SignalInput): LevelResult {
  const bounty = classifyBountyLevel(s);
  const fde = classifyFdeLevel(s);
  const reasons = [...bounty.reasons, ...fde.reasons];

  let track: Track = "noise";
  if (fde.level >= 2 && bounty.level >= 2) track = "hybrid";
  else if (fde.level >= 2) track = "ai_fde";
  else if (bounty.level >= 1 && fde.level <= 1) track = "bug_bounty";
  else if (bounty.level === 0 && fde.level === 0) track = "noise";
  else if (fde.level >= 1) track = "ai_fde";
  else track = "bug_bounty";

  if (s.informantOnlyNoFix && fde.level < 2) {
    reasons.push("informant-only (no fix path) caps FDE compounding");
  }
  if (s.streetSmbMisSale) {
    reasons.push("ICP-solution mismatch detected");
  }

  return {
    track,
    bountyLevel: bounty.level,
    fdeLevel: fde.level,
    reasons,
  };
}
