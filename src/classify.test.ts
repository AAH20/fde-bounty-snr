import assert from "node:assert/strict";
import { describe, it } from "node:test";
import { classifyBountyLevel, classifyFdeLevel, classifySignal } from "./classify.js";
import { evolveCorpus, loadSignals, runPipeline } from "./corpus.js";
import { decide, decideAll } from "./filter.js";
import { emptyCorpus, scoreSnr } from "./snr.js";
import type { FilterDecision, SignalInput } from "./types.js";
import { A2Z, BOUNTY_LADDER, FDE_LADDER } from "./types.js";
import { resolve } from "node:path";
import { fileURLToPath } from "node:url";
import { dirname, join } from "node:path";

const __dirname = dirname(fileURLToPath(import.meta.url));
const root = resolve(__dirname, "..");

function base(partial: Partial<SignalInput> & Pick<SignalInput, "id">): SignalInput {
  const signal: SignalInput = {
    label: partial.label,
    uniqueValidFinding: false,
    rootCauseAnalysis: false,
    responsibleDisclosure: false,
    chainedOrHighImpact: false,
    productizesWeaknessClass: false,
    episodicHeroTicket: false,
    unauthorizedOrUnsafeDemo: false,
    liveCustomerEnvironment: false,
    gateOrPromoteDiscipline: false,
    actionLedgerOrReceipts: false,
    killSwitchNamedOwner: false,
    remediationRetestLoop: false,
    reusableLeaveBehinds: 0,
    siOrPartnerAttachPath: false,
    walkAwayRatePower: false,
    ungatedAgentDemo: false,
    meteredApiCosplay: false,
    informantOnlyNoFix: false,
    streetSmbMisSale: false,
    claimsCustomerTargetingWithoutEvidence: false,
    ...partial,
  };
  signal.evidence ??= Object.fromEntries(
    Object.entries(signal)
      .filter(([key, value]) => key !== "evidence" && (value === true || (key === "reusableLeaveBehinds" && Number(value) > 0)))
      .map(([key]) => [key, `fixture://${signal.id}/${key}`]),
  );
  return signal;
}

describe("Evidence-policy ladders", () => {
  it("exposes complete ladder copy L0-L4", () => {
    assert.equal(Object.keys(BOUNTY_LADDER).length, 5);
    assert.equal(Object.keys(FDE_LADDER).length, 5);
  });

  it("classifies bounty L0 unsafe noise", () => {
    const r = classifySignal(
      base({ id: "n1", unauthorizedOrUnsafeDemo: true, episodicHeroTicket: true }),
    );
    assert.equal(r.bountyLevel, 0);
    assert.equal(r.track, "noise");
  });

  it("classifies bounty L1 unique only", () => {
    const b = classifyBountyLevel(base({ id: "b1", uniqueValidFinding: true }));
    assert.equal(b.level, 1);
  });

  it("classifies bounty L2 responsible researcher", () => {
    const r = classifySignal(
      base({
        id: "b2",
        uniqueValidFinding: true,
        rootCauseAnalysis: true,
        responsibleDisclosure: true,
      }),
    );
    assert.equal(r.bountyLevel, 2);
    assert.equal(r.track, "bug_bounty");
  });

  it("classifies bounty L3 chained impact", () => {
    const b = classifyBountyLevel(
      base({
        id: "b3",
        uniqueValidFinding: true,
        rootCauseAnalysis: true,
        responsibleDisclosure: true,
        chainedOrHighImpact: true,
      }),
    );
    assert.equal(b.level, 3);
  });

  it("classifies bounty L4 class productizer", () => {
    const b = classifyBountyLevel(
      base({
        id: "b4",
        uniqueValidFinding: true,
        rootCauseAnalysis: true,
        responsibleDisclosure: true,
        chainedOrHighImpact: true,
        productizesWeaknessClass: true,
      }),
    );
    assert.equal(b.level, 4);
  });

  it("classifies an interface without measured outcomes as FDE L0", () => {
    const r = classifySignal(base({ id: "m0", meteredApiCosplay: true }));
    assert.equal(r.fdeLevel, 0);
  });

  it("classifies FDE L1 live without gate spine", () => {
    const f = classifyFdeLevel(base({ id: "f1", liveCustomerEnvironment: true }));
    assert.equal(f.level, 1);
  });

  it("classifies FDE L2 gate spine only", () => {
    const f = classifyFdeLevel(
      base({
        id: "f2",
        liveCustomerEnvironment: true,
        gateOrPromoteDiscipline: true,
        actionLedgerOrReceipts: true,
        killSwitchNamedOwner: true,
      }),
    );
    assert.equal(f.level, 2);
  });

  it("classifies FDE L3 compounding plant", () => {
    const r = classifySignal(
      base({
        id: "f3",
        liveCustomerEnvironment: true,
        gateOrPromoteDiscipline: true,
        actionLedgerOrReceipts: true,
        killSwitchNamedOwner: true,
        remediationRetestLoop: true,
        reusableLeaveBehinds: 2,
      }),
    );
    assert.equal(r.fdeLevel, 3);
    assert.equal(r.track, "ai_fde");
  });

  it("classifies FDE L4 productize attach", () => {
    const r = classifySignal(
      base({
        id: "f4",
        liveCustomerEnvironment: true,
        gateOrPromoteDiscipline: true,
        actionLedgerOrReceipts: true,
        killSwitchNamedOwner: true,
        remediationRetestLoop: true,
        reusableLeaveBehinds: 3,
        siOrPartnerAttachPath: true,
        walkAwayRatePower: true,
      }),
    );
    assert.equal(r.fdeLevel, 4);
  });

  it("marks hybrid when bounty≥2 and fde≥2", () => {
    const r = classifySignal(
      base({
        id: "h",
        uniqueValidFinding: true,
        rootCauseAnalysis: true,
        responsibleDisclosure: true,
        liveCustomerEnvironment: true,
        gateOrPromoteDiscipline: true,
        actionLedgerOrReceipts: true,
        killSwitchNamedOwner: true,
      }),
    );
    assert.equal(r.track, "hybrid");
  });
});

describe("SNR + filter compounding", () => {
  it("keeps policy score bounded when noise is zero", () => {
    const s = scoreSnr(
      base({
        id: "cap",
        liveCustomerEnvironment: true,
        gateOrPromoteDiscipline: true,
        actionLedgerOrReceipts: true,
        killSwitchNamedOwner: true,
        remediationRetestLoop: true,
        reusableLeaveBehinds: 5,
        siOrPartnerAttachPath: true,
        walkAwayRatePower: true,
      }),
    );
    assert.ok(s.policyScore <= 1);
    assert.ok(s.signalScore <= 1);
  });

  it("noise has a lower policy score than an evidenced FDE spine", () => {
    const noise = scoreSnr(base({ id: "n", ungatedAgentDemo: true, episodicHeroTicket: true }));
    const signal = scoreSnr(
      base({
        id: "s",
        liveCustomerEnvironment: true,
        gateOrPromoteDiscipline: true,
        actionLedgerOrReceipts: true,
        killSwitchNamedOwner: true,
        remediationRetestLoop: true,
        reusableLeaveBehinds: 2,
      }),
    );
    assert.ok(signal.policyScore > noise.policyScore);
  });

  it("routes FDE L3 to pursue with a2zsoc offers", () => {
    const d = decide(
      base({
        id: "p",
        liveCustomerEnvironment: true,
        gateOrPromoteDiscipline: true,
        actionLedgerOrReceipts: true,
        killSwitchNamedOwner: true,
        remediationRetestLoop: true,
        reusableLeaveBehinds: 2,
      }),
    );
    assert.equal(d.decision, "pursue_fde_compounding");
    assert.ok(d.offers.some((o) => o.url.includes("a2zsoc.com")));
    assert.ok(d.offers.some((o) => o.url.includes("utm_campaign=fde-bounty-snr")));
  });

  it("graduates bounty L2 to FDE path with Instant Audit CTA", () => {
    const d = decide(
      base({
        id: "g",
        uniqueValidFinding: true,
        rootCauseAnalysis: true,
        responsibleDisclosure: true,
        episodicHeroTicket: true,
      }),
    );
    assert.equal(d.decision, "graduate_to_fde_path");
    assert.ok(d.offers.some((o) => o.url.includes("instant-audit") || o.url.includes("consultation")));
  });

  it("parks weak bounty episodic", () => {
    const d = decide(base({ id: "park", uniqueValidFinding: true, episodicHeroTicket: true }));
    assert.equal(d.decision, "park_bounty_episodic");
  });

  it("evolving corpus changes version and hotReasons", () => {
    const signals = [
      base({
        id: "1",
        liveCustomerEnvironment: true,
        gateOrPromoteDiscipline: true,
        actionLedgerOrReceipts: true,
        killSwitchNamedOwner: true,
        remediationRetestLoop: true,
        reusableLeaveBehinds: 1,
      }),
      base({ id: "2", ungatedAgentDemo: true }),
    ];
    const results = decideAll(signals, emptyCorpus());
    const c1 = evolveCorpus(emptyCorpus(), results, signals);
    assert.equal(c1.version, 2);
    assert.ok(c1.sampleCount >= 2);
    assert.ok(c1.hotReasons.length > 0);
    const c2 = evolveCorpus(c1, results, signals);
    assert.equal(c2.version, 3);
    assert.ok(c2.sampleCount > c1.sampleCount);
    assert.equal(c2.scoreHistogram.length, 4);
    assert.ok(Object.keys(c2.reasonCounts).length > 0);
  });

  it("rejects false customer targeting claims", () => {
    const d = decide(
      base({
        id: "apt-lie",
        uniqueValidFinding: true,
        claimsCustomerTargetingWithoutEvidence: true,
      }),
    );
    assert.equal(d.decision, "reject_noise");
  });

  it("warns on ICP-solution mismatch without forcing rejection when evidence is strong", () => {
    const d = decide(
      base({
        id: "street",
        liveCustomerEnvironment: true,
        gateOrPromoteDiscipline: true,
        actionLedgerOrReceipts: true,
        killSwitchNamedOwner: true,
        remediationRetestLoop: true,
        reusableLeaveBehinds: 2,
        streetSmbMisSale: true,
      }),
    );
    assert.equal(d.decision, "pursue_fde_compounding");
    assert.ok(d.rationale.some((x) => x.includes("ICP-solution mismatch")));
  });
});

describe("Fixture integration (comprehensive)", () => {
  it("loads demo fixtures and produces expected decision set", () => {
    const signals = loadSignals(join(root, "fixtures/demo-signals.json"));
    assert.equal(signals.length, 5);
    const { results, corpus } = runPipeline(signals, undefined, false);
    const byId = Object.fromEntries(results.map((r) => [r.id, r.decision]));
    const expected: Record<string, FilterDecision> = {
      "noise-ungated-agent": "reject_noise",
      "bounty-l2-researcher": "graduate_to_fde_path",
      "failed-mcp-meter": "reject_noise",
      "fde-l3-gate-prove": "pursue_fde_compounding",
      "fde-l4-si-attach": "productize_attach",
    };
    for (const [id, dec] of Object.entries(expected)) {
      assert.equal(byId[id], dec, `${id} → ${dec}`);
    }
    assert.equal(corpus.sampleCount, 5);
    for (const r of results) {
      if (r.decision !== "reject_noise") {
        assert.ok(r.offers.every((o) => o.url.startsWith("https://a2zsoc.com")));
      }
    }
  });

  it("A2Z CTA constants use campaign utm", () => {
    assert.match(A2Z.productized, /utm_campaign=fde-bounty-snr/);
    assert.match(A2Z.consultation, /utm_campaign=fde-bounty-snr/);
    assert.match(A2Z.instantAudit, /utm_campaign=fde-bounty-snr/);
    assert.match(A2Z.agenticTrustOps, /utm_campaign=fde-bounty-snr/);
  });

  it("corpus median becomes reference for delta on second pass", () => {
    const signals = loadSignals(join(root, "fixtures/demo-signals.json"));
    const first = runPipeline(signals, undefined, false);
    const second = decideAll(signals, first.corpus);
    const fde = second.find((r) => r.id === "fde-l3-gate-prove");
    assert.ok(fde);
    assert.ok(typeof fde!.snr.deltaVsCorpus === "number");
  });

  it("discounts unevidenced self-attestation", () => {
    const claimed = base({
      id: "claimed",
      liveCustomerEnvironment: true,
      gateOrPromoteDiscipline: true,
      actionLedgerOrReceipts: true,
      killSwitchNamedOwner: true,
      remediationRetestLoop: true,
      reusableLeaveBehinds: 2,
      evidence: {},
    });
    const result = decide(claimed);
    assert.equal(result.snr.evidenceCompleteness, 0);
    assert.notEqual(result.decision, "pursue_fde_compounding");
  });
});
