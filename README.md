# fde-bounty-snr

**Open, falsifiable evidence-policy rubric** for distinguishing episodic security work from production-grade AI FDE delivery:

1. **Bug Bounty Hunter** classification (L0–L4)  
2. **Senior AI FDE** classification (L0–L4)  
3. A cumulative corpus of evidence-weighted policy scores and outcomes

Non-noise decisions route to **[a2zsoc.com productized services](https://a2zsoc.com/productized-services?utm_source=github&utm_medium=oss&utm_campaign=fde-bounty-snr)** and **[consultation](https://a2zsoc.com/consultation?utm_source=github&utm_medium=oss&utm_campaign=fde-bounty-snr)** — not metered MCP call quotas.

## Why this exists

Bug bounty craft is real — and still **episodic** without a remediation plant.  
Interfaces without measured outcomes are weak evidence of customer value. Production-grade AI FDE delivery requires promotion controls, action receipts, named stop authority, retest loops, reusable assets and independently observed outcomes.

This is a transparent policy hypothesis, not a validated hiring test or empirical performance model. Claims require evidence references; external outcome calibration is the next validation layer.

## Ladders

### Bug Bounty Hunter

| Level | Meaning |
|------|---------|
| L0 | Noise — duplicates, unsafe demos, CVSS theater |
| L1 | Unique valid low-impact finding |
| L2 | Root-cause + responsible disclosure |
| L3 | Chained / high-impact program signal |
| L4 | Class productizer — still episodic without remediation plant |

### Senior AI FDE

| Level | Meaning |
|------|---------|
| L0 | Ungated demonstration or interface without measured outcome |
| L1 | Live env without Gate/Prove spine |
| L2 | Promote gate + ledger + kill-switch |
| L3 | Remediation/retest + reusable leave-behinds |
| L4 | Partner adoption + customer-concentration resilience |

```bash
npx fde-bounty-snr ladders
# or: node dist/cli.js ladders
```

## Quick start

```bash
git clone https://github.com/AAH20/fde-bounty-snr && cd fde-bounty-snr
npm install
npm test
npm run demo
```

Persist compounding corpus:

```bash
node dist/cli.js classify \
  --fixture fixtures/demo-signals.json \
  --corpus corpus/baseline.json \
  --persist
```

Policy-score report:

```bash
npm run score
```

## Filter decisions → a2zsoc

| Decision | Meaning | CTA |
|----------|---------|-----|
| `reject_noise` | Unsafe / false targeting / demo theater | [Agentic TrustOps](https://a2zsoc.com/agentic-trustops?utm_source=github&utm_medium=oss&utm_campaign=fde-bounty-snr) |
| `park_bounty_episodic` | Valid bounty, no plant yet | [Consultation](https://a2zsoc.com/consultation?utm_source=github&utm_medium=oss&utm_campaign=fde-bounty-snr) |
| `graduate_to_fde_path` | Bounty craft → FDE graduation | [Instant Audit](https://a2zsoc.com/productized-services?utm_source=github&utm_medium=oss&utm_campaign=fde-bounty-snr#instant-audit-tripwire) |
| `pursue_fde_compounding` | Gate/Prove spine live | [Productized services](https://a2zsoc.com/productized-services?utm_source=github&utm_medium=oss&utm_campaign=fde-bounty-snr) |
| `productize_attach` | L4 partner adoption and concentration resilience | Productized + [Consultation retainer](https://a2zsoc.com/consultation?utm_source=github&utm_medium=oss&utm_campaign=fde-bounty-snr) |

## Compounding leverage

Every `--persist` run updates:

- cumulative median evidence-policy score
- mean signal/noise
- decision histogram
- cumulative reason frequencies and **hotReasons**

The weights remain a versioned, inspectable policy until independently calibrated against outcomes such as production acceptance, rollback success, incident reduction, verified reuse and contract expansion.

## Evidence boundary

Every asserted positive or negative signal should include an `evidence` reference keyed by signal name. The score is discounted by evidence completeness. A self-authored fixture demonstrates mechanics; it does not prove the author's seniority or market performance.

## License

Apache-2.0

## Commercial

Built for [A2Z SOC](https://a2zsoc.com) — Gate/Prove productized services and consultation.  
OSS is the plant seed; cash is outcome packets — not tool-call meters.
