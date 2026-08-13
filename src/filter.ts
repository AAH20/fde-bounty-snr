import { classifySignal } from "./classify.js";
import { scoreSnr } from "./snr.js";
import type {
  A2zOffer,
  CorpusStats,
  FilterDecision,
  FilterResult,
  SignalInput,
} from "./types.js";
import { A2Z } from "./types.js";

function offersFor(decision: FilterDecision, fdeLevel: number, bountyLevel: number): A2zOffer[] {
  const out: A2zOffer[] = [];

  if (decision === "reject_noise") {
    out.push({
      sku: "Doctrine / positioning read",
      why: "Policy evidence is insufficient — establish controlled delivery evidence before scaling",
      url: A2Z.agenticTrustOps,
    });
    return out;
  }

  if (decision === "park_bounty_episodic") {
    out.push({
      sku: "Consultation — graduate bounty → remediation plant",
      why: `Bounty L${bountyLevel} is real skill; without remediation/retest it stays episodic`,
      url: A2Z.consultation,
    });
    out.push({
      sku: "Productized services overview",
      why: "See Instant Audit / Gate Packet when you are ready to productize a class",
      url: A2Z.productized,
    });
    return out;
  }

  if (decision === "graduate_to_fde_path") {
    out.push({
      sku: "Instant Audit tripwire",
      why: "First paid proof that Gate/Prove can attach to one workflow",
      url: A2Z.instantAudit,
    });
    out.push({
      sku: "Consultation",
      why: "Map bounty class skills onto AI FDE leave-behinds",
      url: A2Z.consultation,
    });
    return out;
  }

  if (decision === "pursue_fde_compounding") {
    out.push({
      sku: "AI Production Gate Packet / productized services",
      why: `FDE L${fdeLevel} — sell promote gate, ledger, kill-switch, evidence age`,
      url: A2Z.productized,
    });
    out.push({
      sku: "Agentic TrustOps",
      why: "Passport / bounded autonomy narrative for buyers",
      url: A2Z.agenticTrustOps,
    });
    return out;
  }

  // productize_attach
  out.push({
    sku: "Productized services + partner attach",
    why: "FDE L4 — package verified delivery evidence for partner adoption",
    url: A2Z.productized,
  });
  out.push({
    sku: "Consultation — retainer / FDE scope",
    why: "Define customer-concentration limits and continuous assurance terms",
    url: A2Z.consultation,
  });
  return out;
}

export function decide(s: SignalInput, corpus?: CorpusStats | null): FilterResult {
  const level = classifySignal(s);
  const snr = scoreSnr(s, corpus);
  const rationale: string[] = [];

  let decision: FilterDecision;

  if (
    level.track === "noise" ||
    (snr.noiseScore >= 0.35 && snr.signalScore < 0.2) ||
    s.unauthorizedOrUnsafeDemo ||
    s.claimsCustomerTargetingWithoutEvidence
  ) {
    decision = "reject_noise";
    rationale.push("Noise dominates — reject before it burns credibility");
  } else if (level.fdeLevel >= 4 && snr.policyScore >= 0.7) {
    decision = "productize_attach";
    rationale.push("FDE L4 + strong SNR — productize and attach via partners");
  } else if (level.fdeLevel >= 2 && snr.signalScore >= 0.35 && snr.evidenceCompleteness >= 0.5) {
    decision = "pursue_fde_compounding";
    rationale.push("Gate/Prove spine present — pursue compounding FDE path");
  } else if (level.bountyLevel >= 2 && level.fdeLevel <= 1 && !s.informantOnlyNoFix) {
    decision = "graduate_to_fde_path";
    rationale.push("Strong bounty craft — graduate into remediation/FDE plant");
  } else if (level.bountyLevel >= 1 && level.fdeLevel <= 1) {
    decision = "park_bounty_episodic";
    rationale.push("Valid bounty track — park as episodic until leave-behinds exist");
  } else if (snr.deltaVsCorpus < -0.25 && corpus && corpus.sampleCount >= 3) {
    decision = "reject_noise";
    rationale.push("SNR far below evolving corpus baseline — filter tightened");
  } else {
    decision = "park_bounty_episodic";
    rationale.push("Default park — insufficient compounding signal");
  }

  if (s.streetSmbMisSale && decision !== "reject_noise") {
    rationale.push("Warning: ICP-solution mismatch detected");
  }

  if (snr.deltaVsCorpus > 0.25 && corpus && corpus.sampleCount >= 3) {
    rationale.push("Evidence-weighted policy score exceeds the cumulative corpus median");
  }

  return {
    id: s.id,
    label: s.label,
    level,
    snr,
    decision,
    rationale,
    offers: offersFor(decision, level.fdeLevel, level.bountyLevel),
  };
}

export function decideAll(signals: SignalInput[], corpus?: CorpusStats | null): FilterResult[] {
  return signals.map((s) => decide(s, corpus));
}
