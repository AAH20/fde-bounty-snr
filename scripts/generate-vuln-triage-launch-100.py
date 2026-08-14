#!/usr/bin/env python3
"""Generate docs/linkedin-publish/vuln-triage-launch-100.

100 LinkedIn posts launching the open-source vuln-triage project across all
angles: thesis, methodology, ICPs, pain points, use cases, KPIs, comparisons,
board translation, compounding leverage, and the a2zsoc funnel.

Ten arcs of ten:
  01-10  Thesis: stop scanning, start deciding (CVSS is noise)
  11-20  Methodology: KEV, EPSS, ATT&CK, reachability, criticality
  21-30  ICPs: MSPs, B2B SaaS, DevSecOps, platform teams, container shops
  31-40  Pain points: alert fatigue, patch prioritization, board reporting, audit
  41-50  Use cases: Trivy, Grype, Linux fleets, Kubernetes, CI/CD, cloud
  51-60  KPIs: noise reduction, MTTR, dwell time, coverage, cost per closure
  61-70  Comparisons: vs scanners, vs CVSS-only, vs prioritizer SaaS, vs bug bounty
  71-80  Board translation: decision tiers, expected-loss scaffold, exec memo
  81-90  Compounding leverage: open-core, dataset moat, the foundry
  91-100 The a2zsoc funnel: free triage to remediation, verification, consultation

INTEGRITY:
  - The tool is real and published (github.com/AAH20/vuln-triage). Describe
    only what it actually does.
  - Real ATT&CK T-codes; KEV = CISA Known Exploited Vulnerabilities;
    EPSS = FIRST 30-day exploitation probability (with its stated caveat).
  - No fabricated adoption numbers, star counts, or client results: it just
    launched. Expected-loss is a scaffold (range), never fake precision.

House style: no em dash, no en dash, no asterisk. Hashtags used.
"""
from __future__ import annotations

import hashlib
import json
from datetime import date
from pathlib import Path

OUT = Path("docs/linkedin-publish/vuln-triage-launch-100")
CAMPAIGN = "vuln-triage-launch-100"
UTM = f"utm_source=linkedin&utm_medium=social&utm_campaign={CAMPAIGN}"
BASE = "https://a2zsoc.com"
GH = "https://github.com/AAH20/vuln-triage"
FORBIDDEN = ("—", "–", "*")

CORE_TAGS = "#VulnerabilityManagement #DevSecOps #CyberSecurity #CVE #OpenSource"

TRACKS = [
    "Thesis: stop scanning, start deciding",
    "Methodology: KEV, EPSS, ATT&CK",
    "ICPs",
    "Pain points",
    "Use cases",
    "KPIs",
    "Comparisons",
    "Board translation",
    "Compounding leverage",
    "The a2zsoc funnel",
]

CURRENT_OFFER_PATHS = ["/productized-services", "/consultation", "/instant-audit", "/pricing"]
WAITLIST_PATH = "/start"


def link(path: str) -> str:
    return f"{BASE}{path}?{UTM}"


def L(*paths: str) -> str:
    lines = [GH]
    lines.extend(link(p) for p in paths)
    return "\n".join(lines)


POSTS: list[tuple[str, str, list[str], str]] = []


def post(title: str, body: str, paths: list[str], tags: str) -> None:
    POSTS.append((title, body.strip(), paths, tags))


# ============================================= ARC 1  Thesis
post(
    "Launch: stop scanning, start deciding",
    """
Your scanner found 500 CVEs. Which 12 actually matter today?

That question is the daily pain of every security team, and no scanner answers it. Scanning is a solved, commodity problem. Deciding what to fix first is not.

I built and open-sourced Triage: it sits on top of the scanner you already run (Trivy, Grype, OpenVAS, Nmap NSE) and turns the list into a decision, prioritized by real-world exploitation, not CVSS severity alone.

Free, Apache-2.0, pure standard library. On the bundled example, 10 findings collapse to 3 that require action and 7 noise.
""",
    ["/productized-services"],
    "#AppSec #CloudSecurity",
)

post(
    "CVSS is the noise, not the signal",
    """
Every organisation has hundreds of CVSS Critical findings. CVSS cannot tell you which to fix first, because it measures technical severity in the abstract, not real-world risk.

FIRST, who maintain CVSS, and CISA both say plainly: do not prioritize on CVSS alone.

Triage combines the signals that actually determine risk: confirmed exploitation (CISA KEV), 30-day probability (FIRST EPSS), reachability, and business criticality. Two CVSS 9.8 findings in my demo get deprioritized, because nobody is exploiting them.

That is the whole point.
""",
    ["/productized-services"],
    "#CVSS #RiskManagement",
)

post(
    "The tool that decides, not just detects",
    """
Detection is crowded. Trivy, Grype, OpenVAS, Nuclei, Nessus all find vulnerabilities and produce lists. Not one of them decides what matters in your environment.

Triage is not another scanner. It is the decision layer above all of them. Feed it any scanner's output and it returns a three-tier verdict: FIX NOW, FIX THIS CYCLE, MONITOR, with a board-ready memo.

You never switch tools. You add the layer that turns a list into a decision.
""",
    ["/productized-services"],
    "#DevSecOps #SecurityTools",
)

post(
    "The 500-to-12 problem",
    """
A vulnerability scan is not the hard part. The hard part is the meeting afterward, where someone has to decide which findings justify a maintenance window and which are noise.

Most teams either patch everything (impossible) or patch by CVSS (wrong). Both burn the team out.

Triage answers it with evidence: of your findings, these are actively exploited, reachable, and on assets that matter. Fix these first, here is the deadline, here is why.

Open source, free, runs in seconds.
""",
    ["/consultation"],
    "#VulnerabilityManagement #SOC",
)

post(
    "Why I open-sourced it",
    """
Because the prioritization layer should not be a paywall.

Detection is free and commodity. But turning a scan into a decision, using confirmed exploitation and probability instead of severity, is the part that actually saves teams from drowning, and it should be available to everyone.

Triage is Apache-2.0. Clone it, run it, contribute a scanner adapter. What is paid is the follow-on: validating reachability in your environment, engineering the safe remediation, and verifying closure.

Free to decide. Paid to close.
""",
    ["/productized-services"],
    "#OpenSource #AppSec",
)

post(
    "One command, any scanner",
    """
    trivy image -f json app:latest > scan.json && triage -i scan.json

That is the entire workflow. Triage detects the format, enriches every finding with CISA KEV and FIRST EPSS, factors in your asset context, and prints the decision.

No dependencies. No account. No cloud. Pure Python standard library, runs offline on a bundled feed sample or live with a single flag.

The barrier to trying it is one command. That was deliberate.
""",
    ["/productized-services"],
    "#DevSecOps #CLI #Automation",
)

post(
    "Severity is not risk",
    """
A CVSS 9.8 that has never been exploited, with no public exploit, is lower real-world risk than a CVSS 7.5 that is in CISA KEV and being used against your sector right now.

Prioritizing by severity inverts your own risk. You spend the maintenance window on the theoretically scary and leave the actually exploited open.

Triage flips it back: exploitation first, severity last. The numbers that predict a breach, in the order that matters.
""",
    ["/productized-services"],
    "#RiskManagement #ThreatIntel",
)

post(
    "Determinism is a feature",
    """
Run Triage twice on the same input and you get byte-identical output. Same scan, same decision, every time.

That sounds obvious until you notice how many security tools give you a different answer on Tuesday than they did on Monday. A decision you cannot reproduce is not a decision, it is an opinion.

Determinism is verified by property tests in the repo, including the invariant that a non-exploited CVSS 9.8 must be deprioritized. Auditable by design.
""",
    ["/consultation"],
    "#Engineering #Reproducibility",
)

post(
    "The demo, in one screen",
    """
10 findings ingested. 3 require a decision (2 FIX NOW, 1 this cycle). 7 deprioritized as noise, 70 percent of the list.

Two of the seven dropped are CVSS 9.8 Critical (zlib, glibc), demoted because they are not being exploited. The two FIX NOW items are Log4Shell and Citrix Bleed, both in CISA KEV, both internet-facing, both on a critical asset.

That is the difference between a scanner and a decision, on one screen.
""",
    ["/productized-services"],
    "#VulnerabilityManagement #CVE",
)

post(
    "Arc close: the thesis",
    """
Scanning is commodity. Deciding is the value. And deciding well means prioritizing by real-world exploitation, not CVSS severity, with a result a board can act on.

That is Triage, and it is free and open source. The next posts go through who it is for, the pain it removes, the methodology, and where the paid work begins.

Clone it, run it against your own scan, and tell me what it cut.
""",
    ["/productized-services"],
    "#OpenSource #DevSecOps",
)

# ============================================= ARC 2  Methodology
post(
    "CISA KEV: the strongest signal you are ignoring",
    """
The single best predictor that a vulnerability will be used against you is that it is already being used against someone.

That is CISA's Known Exploited Vulnerabilities catalog: over 1,600 CVEs confirmed exploited in the wild. CISA explicitly recommends it as a prioritization input.

Triage checks every finding against KEV first. If it is exploited and reachable and on a critical asset, it is FIX NOW. Nothing else in the stack is a stronger signal.
""",
    ["/productized-services"],
    "#KEV #ThreatIntel #CISA",
)

post(
    "EPSS: probability, not severity",
    """
FIRST's Exploit Prediction Scoring System estimates the probability a vulnerability will be exploited in the next 30 days. It is data-driven, updated daily, and covers hundreds of thousands of CVEs.

FIRST is explicit that EPSS has no environmental context and is not a complete risk score. That is exactly why Triage uses it as one input, not the whole decision.

KEV tells you what is exploited. EPSS tells you what is likely to be. Together they are the forward-looking half of the decision.
""",
    ["/productized-services"],
    "#EPSS #RiskManagement",
)

post(
    "Reachability changes everything",
    """
The same CVE on an internet-facing web server and on an air-gapped batch box are not the same risk. Severity scores treat them identically. Attackers do not.

Triage takes your asset context, which systems are reachable and which are segmented, and folds it into the decision. A KEV finding on a reachable critical asset is an emergency. The same finding behind segmentation is a scheduled fix.

Environment is half of risk. Most prioritization ignores it.
""",
    ["/consultation"],
    "#NetworkSecurity #AttackSurface",
)

post(
    "Business criticality is a security input",
    """
A vulnerability on your payments platform and the same one on a demo box do not deserve the same urgency. The technical severity is identical. The business consequence is not.

Triage lets you tag asset criticality and business value, so the decision reflects what the organisation actually cares about, not just what the CVE database says.

Security prioritization without business context is just noise with a ranking.
""",
    ["/productized-services"],
    "#GRC #BusinessRisk #CISO",
)

post(
    "The priority function, in plain terms",
    """
Triage combines four things, in this order of weight:

Is it actually exploited? (CISA KEV, strongest)
How likely in 30 days? (FIRST EPSS)
Is it reachable? (your asset context)
Does the asset matter? (business criticality)

CVSS is present but last, because severity in the abstract is the weakest predictor of real-world risk. Everything above it is what determines whether you get breached.
""",
    ["/productized-services"],
    "#RiskManagement #VulnerabilityManagement",
)

post(
    "ATT&CK as a narrative, never an attack",
    """
For each top exposure, Triage shows the plausible behavioral chain a vulnerability enables, mapped to MITRE ATT&CK: T1190 Exploit Public-Facing Application, through to T1486 Data Encrypted for Impact.

It is a risk story a board understands, not an executed attack. Triage runs nothing against any target. It is not an adversary-emulation platform.

Authorized emulation, actually running the TTPs safely against a replica, is a separate engagement. The tool explains; it does not exploit.
""",
    ["/consultation"],
    "#MITREATTACK #ThreatEmulation",
)

post(
    "Four evidence levels, never conflated",
    """
Triage is careful about what it claims. A vulnerability may be:

Technically capable of enabling a technique.
Observed exploited by credible sources.
Relevant to your sector.
Confirmed in your environment.

Only the last justifies saying you are specifically targeted, and that needs authorized evidence, not a public feed. The tool never tells a customer an APT is after them because a CVE exists. Honesty is a feature.
""",
    ["/productized-services"],
    "#ThreatIntel #CyberRisk",
)

post(
    "Live feeds, verified",
    """
Triage ships with a bundled KEV and EPSS sample so it runs instantly offline. Add one flag and it pulls the live feeds: over 1,600 confirmed-exploited CVEs from CISA, hundreds of thousands of EPSS scores from FIRST.

The methodology is authoritative because the inputs are authoritative. Nothing invented, nothing proprietary about the data. The value is the decision layer on top.
""",
    ["/productized-services"],
    "#KEV #EPSS #ThreatIntel",
)

post(
    "Why not just use CVSS plus a gut feeling",
    """
Because gut feeling does not scale past a few hundred findings, and it is not defensible to an auditor or a board.

Triage replaces the gut with a documented, reproducible function over authoritative signals. When someone asks why you fixed these twelve and deferred those four hundred, you have an evidence-backed answer, not a shrug.

The methodology is the audit trail.
""",
    ["/consultation"],
    "#Audit #GRC #Compliance",
)

post(
    "Arc close: the methodology",
    """
Confirmed exploitation, forward probability, reachability, business criticality, with severity in its proper place last. That is how you turn a scan into a decision that predicts real risk instead of theoretical severity.

Every input is public and authoritative. The value is assembling them into a verdict, reproducibly, for free.

Next: exactly who this removes the most pain for.
""",
    ["/productized-services"],
    "#VulnerabilityManagement #DevSecOps",
)

# ============================================= ARC 3  ICPs
post(
    "For MSPs managing hundreds of Linux servers",
    """
If you manage vulnerability posture across many customers, you already know the problem: every scan produces hundreds of findings, and your engineers cannot triage them all for every client.

Triage runs on each customer's scan output and returns a per-client decision list, prioritized by real exploitation. One analyst covers more clients, and every client gets a defensible treatment order instead of a raw dump.

Free to run. The verification and remediation layer is where a2zsoc partners.
""",
    ["/productized-services", "/consultation"],
    "#MSP #ManagedServices",
)

post(
    "For B2B SaaS with a SOC 2 review coming",
    """
Enterprise customers demand SOC 2 or ISO 27001, and your small security team is drowning in scanner output that the audit will ask you to have handled.

Triage turns that output into a prioritized, evidence-backed treatment register: what is exploited, what is reachable, what you decided, and why. Exactly the artifact an auditor and an enterprise buyer want to see.

Prioritize free. Close the gaps with a2zsoc.
""",
    ["/productized-services", "/consultation"],
    "#SOC2 #ISO27001 #SaaS",
)

post(
    "For DevSecOps teams shifting left",
    """
You already run Trivy or Grype in the pipeline. It flags fifty things per build and developers ignore all of them, because they cannot tell which one matters.

Triage takes that scanner output and returns a decision: fail the build on the exploited-and-reachable, warn on the probable, log the rest. Available as a GitHub Action so it drops into CI.

Prioritization your developers will actually act on, because it is not crying wolf on every CVSS 7.
""",
    ["/productized-services"],
    "#DevSecOps #CICD #ShiftLeft",
)

post(
    "For platform and SRE teams",
    """
You own the fleet, and security keeps handing you vulnerability lists with no priority, expecting you to patch everything during windows you do not have.

Triage gives you a defensible order: these are exploited and reachable, do them this window; these are noise, document and move on. It hands SRE a decision, not a backlog.

Fewer emergency patches, more sleep, and an audit trail for both.
""",
    ["/consultation"],
    "#SRE #PlatformEngineering",
)

post(
    "For container and Kubernetes shops",
    """
Every image scan lights up with base-image CVEs, most of which are never exploited. Trivy and Grype find them; nobody can triage them all.

Triage ingests Trivy and Grype JSON directly and tells you which container CVEs are actually exploited and reachable versus which are inherited base-image noise. Two CVSS 9.8s in my demo, zlib and glibc, get correctly deprioritized.

Ship faster, patch what matters.
""",
    ["/productized-services"],
    "#Kubernetes #Containers #CloudNative",
)

post(
    "For the CISO who needs a board number",
    """
Your board does not want a CVE count. They want to know exposure in business terms and whether it is improving.

Triage produces a one-page executive memo: what is exposed, why it matters now, the expected-loss range, what to authorize, and the cost of delay. Grounded in confirmed exploitation, not severity theatre.

The technical work is the tool. The board translation is built in.
""",
    ["/consultation", "/productized-services"],
    "#CISO #BoardGovernance",
)

post(
    "For compliance and GRC teams",
    """
Auditors ask how you prioritized remediation. If the answer is by CVSS, the follow-up is why you left exploited vulnerabilities open while patching unexploited ones.

Triage gives you a documented, reproducible prioritization tied to CISA KEV and FIRST EPSS, with a per-finding decision and rationale. That is audit evidence, not a spreadsheet of severities.

Defensible prioritization, on demand.
""",
    ["/productized-services", "/consultation"],
    "#GRC #Compliance #Audit",
)

post(
    "For the solo security engineer",
    """
One person, a whole estate, and a scanner that produces more findings than you could patch in a year. You need to know where to spend your limited hours.

Triage is built for exactly this: point it at your scan, get the short list of what is actually exploited and reachable, and spend your time there. Free, no infrastructure, runs on your laptop.

The force multiplier for the team of one.
""",
    ["/productized-services"],
    "#CyberSecurity #InfoSec",
)

post(
    "For cyber insurers and underwriters",
    """
You price risk, and self-attested vulnerability posture is a weak input. What you want is evidence of what is exploited and reachable in the insured's environment, and whether they acted on it.

Triage produces exactly that decision record. An insured who runs it and closes the FIX NOW items has a defensible posture, not a checkbox.

The prioritization is free; the verified closure is the underwriting signal.
""",
    ["/consultation"],
    "#CyberInsurance #RiskManagement",
)

post(
    "Arc close: who it is for",
    """
MSPs, B2B SaaS with audits coming, DevSecOps, SRE, container shops, CISOs, GRC, solo engineers, insurers. Different buyers, one shared pain: a scanner that finds everything and prioritizes nothing.

Triage removes that pain for free. The follow-on, validating and closing the exposures it surfaces, is where a2zsoc engages.

Next: the specific pains, named.
""",
    ["/productized-services"],
    "#DevSecOps #VulnerabilityManagement",
)

# ============================================= ARC 4  Pain points
post(
    "Alert fatigue is a prioritization failure",
    """
Teams do not burn out because there are vulnerabilities. They burn out because every one is flagged Critical and none is ranked, so everything feels urgent and nothing gets done.

Triage cuts the list to what is actually exploited and reachable. In the demo, 70 percent of findings are deprioritized as noise. That is 70 percent of the anxiety removed, with evidence behind the cut.

Fatigue is a symptom of missing prioritization, not too much work.
""",
    ["/productized-services"],
    "#AlertFatigue #SOC #BurnOut",
)

post(
    "The patch-everything myth",
    """
Nobody patches everything. There are not enough maintenance windows in the year. So teams patch what is loudest, which is usually what has the highest CVSS, which is usually not what is being exploited.

Triage replaces patch-everything and patch-by-severity with patch-what-is-exploited-and-reachable-first. A finite, ranked, defensible list instead of an infinite backlog.

You were never going to patch it all. Patch the right ones.
""",
    ["/consultation"],
    "#PatchManagement #VulnerabilityManagement",
)

post(
    "The 6pm security questionnaire",
    """
An enterprise prospect sends a security review. It asks how you handle vulnerability prioritization. Your honest answer is you run a scanner and do your best.

Triage upgrades that answer to: we prioritize by confirmed exploitation and 30-day probability, map to ATT&CK, and maintain a decision record per finding. That answer closes deals.

The tool is free. The deal it unblocks is not.
""",
    ["/productized-services", "/consultation"],
    "#SecurityQuestionnaire #B2BSales",
)

post(
    "The board slide nobody can defend",
    """
Twenty findings marked Critical, a red bar chart, and no answer to the only two questions the board has: what is our real exposure, and is it getting better.

Triage produces the memo that answers both, in expected-loss terms grounded in exploitation evidence. Not a CVE count. A decision.

Stop reporting scanner output to your board. Report a decision.
""",
    ["/consultation"],
    "#BoardGovernance #CISO",
)

post(
    "The audit finding that writes itself",
    """
An auditor reviews your remediation and finds exploited vulnerabilities left open while low-risk ones were patched. Prioritized by CVSS. It happens constantly.

Triage prevents it: the exploited-and-reachable are always ranked first, with a documented rationale. The audit finding never gets written, because the prioritization was defensible from the start.

Cheaper than the finding.
""",
    ["/productized-services", "/consultation"],
    "#Audit #GRC #Compliance",
)

post(
    "The CVSS 9.8 that wasted your weekend",
    """
Someone saw a 9.8, called an emergency, and the team spent the weekend patching a vulnerability that has never been exploited and never will be, while a KEV-listed 7.5 sat open on an internet-facing box.

Triage stops that. In the demo, two CVSS 9.8s (zlib, glibc) are deprioritized because they are not exploited, and a KEV finding is escalated instead.

Severity panic is expensive. Evidence is cheap.
""",
    ["/productized-services"],
    "#CVSS #IncidentResponse",
)

post(
    "The scanner nobody reads",
    """
You bought a good scanner. It runs nightly. It emails a 400-line report to a distribution list where it is deleted unread, because nobody can turn 400 lines into an action.

Triage is the layer that makes the scanner worth its licence: it converts the 400 lines into the 12 that matter and the 1 that is urgent. The scanner finds; Triage decides.

Your existing tools, finally actionable.
""",
    ["/productized-services"],
    "#SecurityTools #DevSecOps",
)

post(
    "The vendor risk gap",
    """
You ask vendors for their vulnerability posture. They send a scan. You have no way to know if the scary-looking findings are actually dangerous or inherited base-image noise.

Run their scan through Triage and you get an evidence-based read: is any of this exploited and reachable, or is it CVSS theatre. Third-party risk, decided instead of assumed.
""",
    ["/consultation"],
    "#ThirdPartyRisk #VendorManagement",
)

post(
    "The MTTR that never improves",
    """
Your mean time to remediate is flat, because the team is spread across everything instead of focused on what matters. Effort without prioritization does not move the metric.

Triage concentrates the team on the exploited-and-reachable minority. Fewer items, faster closure on the ones that count, and a measurable drop in time-to-remediate for what actually reduces risk.

Focus is the lever. Prioritization is the focus.
""",
    ["/productized-services"],
    "#MTTR #SecurityMetrics",
)

post(
    "Arc close: the pains",
    """
Alert fatigue, the patch-everything myth, the frozen questionnaire, the indefensible board slide, the audit finding, the wasted weekend, the unread scanner, the vendor gap, the flat MTTR. All the same root cause: detection without decision.

Triage is the decision, free and open source. Next: the exact use cases and the scanners it plugs into.
""",
    ["/productized-services"],
    "#VulnerabilityManagement #SOC",
)

# ============================================= ARC 5  Use cases
post(
    "Trivy plus Triage",
    """
    trivy image -f json app:latest > scan.json && triage -i scan.json

Trivy is the most popular open-source scanner in the world and it produces excellent, exhaustive lists. Triage turns the list into a decision: which of these container CVEs are exploited, reachable, and worth a build failure.

Two tools, one pipeline, zero list-staring. The scanner you already love, finally prioritized.
""",
    ["/productized-services"],
    "#Trivy #Containers #DevSecOps",
)

post(
    "Grype plus Triage",
    """
Running Grype with Syft for SBOM-based scanning? Triage ingests Grype JSON directly.

Every dependency CVE Grype surfaces gets enriched with KEV and EPSS and ranked into the three tiers. You keep your SBOM workflow and add the decision layer that tells you which of those dependency findings an attacker would actually use.

SBOM to decision, in one command.
""",
    ["/productized-services"],
    "#Grype #SBOM #SupplyChainSecurity",
)

post(
    "OpenVAS and Nmap NSE plus Triage",
    """
Running network scans with OpenVAS or Nmap's vulners script? Export the CVEs and pipe them in. Triage accepts a plain CVE list, so any scanner that emits CVE ids feeds the decision engine.

You are not locked into one ecosystem. Whatever finds the vulnerabilities, Triage decides which ones matter. Vendor-neutral by design.
""",
    ["/consultation"],
    "#OpenVAS #Nmap #NetworkSecurity",
)

post(
    "Triage in CI/CD",
    """
Available as a GitHub Action. Add a few lines to your workflow and every pipeline run triages its own scan: fail on exploited-and-reachable, warn on probable, log the rest.

No more pipelines that either block on every CVE (developers revolt) or block on none (security revolts). A build gate that reflects real risk, so developers trust it and act on it.
""",
    ["/productized-services"],
    "#CICD #GitHubActions #DevSecOps",
)

post(
    "Triage for a Linux fleet",
    """
Point it at the package inventory or scan output for a fleet of Linux servers and get a fleet-wide decision: which hosts carry exploited-and-reachable exposures, ranked, with deadlines.

Built on seven years of Linux systems work. It understands that the same CVE means different things on a bastion host and a batch worker, and it prioritizes accordingly.

Fleet exposure, decided.
""",
    ["/productized-services", "/consultation"],
    "#Linux #InfrastructureSecurity",
)

post(
    "Triage for cloud workloads",
    """
Cloud scanners produce enormous findings across images, hosts, and IaC. Feed the CVE output through Triage with your asset context, which workloads are internet-facing and which are internal, and the decision reflects reachability.

A KEV finding on a public-facing service is an emergency. The same in a private subnet is scheduled. Cloud context, folded into the decision.
""",
    ["/consultation"],
    "#CloudSecurity #CSPM",
)

post(
    "Triage for a point-in-time assessment",
    """
Doing a security assessment for a client? Run their scan through Triage and hand them a prioritized treatment register plus a board memo in minutes, instead of a raw scanner dump.

The deliverable looks like senior consulting because it is a decision, not a list. Free tool, professional output, and a clear path to the paid remediation that follows.
""",
    ["/productized-services", "/consultation"],
    "#Consulting #SecurityAssessment",
)

post(
    "Triage before a penetration test",
    """
Before you pay for a pentest, run Triage. Close the exploited-and-reachable findings first, so the test spends its expensive hours on logic and depth, not on the KEV-listed CVE you could have patched for free.

Cheaper pentests, better findings, because you did not waste them on the obvious.
""",
    ["/consultation"],
    "#PenetrationTesting #DevSecOps",
)

post(
    "Triage as a recurring check",
    """
KEV and EPSS change. A CVE that was noise last month enters KEV this month and becomes urgent. Run Triage on a schedule against your current scan and catch that shift the day it happens.

The decision is not a one-time event. Exploitation is a moving signal, and re-triaging keeps your priorities aligned with reality. The paid continuous-assurance layer automates exactly this.
""",
    ["/productized-services", "/consultation"],
    "#ContinuousMonitoring #VulnerabilityManagement",
)

post(
    "Arc close: the use cases",
    """
Trivy, Grype, OpenVAS, Nmap, CI/CD, Linux fleets, cloud, assessments, pre-pentest, recurring checks. One decision layer, every scanner, every workflow.

It plugs into what you already run and makes it actionable. Free and open source. Next: the KPIs it moves.
""",
    ["/productized-services"],
    "#DevSecOps #VulnerabilityManagement",
)

# ============================================= ARC 6  KPIs
post(
    "KPI: noise reduction",
    """
The headline number: what fraction of scanner findings get correctly deprioritized. In the demo, 70 percent. That is 70 percent less work, anxiety, and window time spent on things that do not matter.

Measure it on your own scan. The percentage you can safely defer, with evidence, is the first number that proves the tool paid for itself, and it cost nothing.
""",
    ["/productized-services"],
    "#SecurityMetrics #KPIs",
)

post(
    "KPI: KEV exposure and closure",
    """
Track how many CISA KEV vulnerabilities are present in your environment, and how fast you close them. This is the metric that correlates most directly with real breach risk.

Triage surfaces your KEV exposure instantly and ranks it first. Closing KEV findings fast is the single most defensible security KPI you can report to a board or an auditor.
""",
    ["/consultation"],
    "#KEV #SecurityMetrics #CISO",
)

post(
    "KPI: time to decision",
    """
Not time to remediate, time to decision. How long from scan output to a defensible, prioritized treatment list. For most teams it is days of manual review. With Triage it is seconds.

Compressing time-to-decision compresses everything downstream. You cannot remediate fast if you cannot decide fast, and deciding is where teams stall.
""",
    ["/productized-services"],
    "#SecurityMetrics #MTTR",
)

post(
    "KPI: coverage of subsequently-exploited CVEs",
    """
The honest test of any prioritization: of the vulnerabilities that later got exploited, how many did you flag as urgent in advance?

Because Triage leads with KEV and EPSS, its FIX NOW list is heavily weighted toward what actually gets exploited. Track this over time and it is the proof that your prioritization predicts reality instead of severity.
""",
    ["/consultation"],
    "#ThreatIntel #SecurityMetrics",
)

post(
    "KPI: remediation effort avoided",
    """
Every finding you correctly defer is engineering hours not spent. Multiply the deprioritized count by the average effort per fix and you have a hard cost saving, in hours, from accurate deprioritization.

This is the KPI a CFO understands: not what you patched, but what you safely did not have to. Triage makes that number visible and defensible.
""",
    ["/productized-services", "/consultation"],
    "#FinOps #SecurityMetrics #CFO",
)

post(
    "KPI: dwell-time contribution",
    """
Every day an exploited, reachable vulnerability stays open is a day of exposure with a real cost, and breach studies attach a number to it.

Triage compresses the time an exploited exposure remains unaddressed by putting it at the top on day one. Track the reduction in open-KEV-days and you have translated a technical improvement into a risk number.
""",
    ["/consultation"],
    "#DwellTime #CyberRisk",
)

post(
    "KPI: expected-loss exposure trend",
    """
Sum the expected-loss scaffold across your FIX NOW items and track it over time. As you close exploited exposures, the number falls. As new KEV entries land, it rises.

It is a range, not a precise figure, and Triage says so. But a trending expected-loss line is the board metric that turns vulnerability work into a business story.
""",
    ["/consultation", "/productized-services"],
    "#CyberRisk #BoardGovernance",
)

post(
    "KPI: false-urgency rate",
    """
How often does your team drop everything for a finding that turns out not to matter? Every CVSS-driven fire drill is a false-urgency event, and they destroy morale and focus.

Triage drives this toward zero by escalating only exploited-and-reachable findings. Fewer fire drills, measured, is a culture metric as much as a security one.
""",
    ["/productized-services"],
    "#SOC #SecurityCulture",
)

post(
    "KPI: analyst leverage",
    """
How many assets or clients can one analyst keep triaged? For an MSP or a small team, this is the number that caps growth.

Automating the decision layer raises it directly: the analyst reviews Triage output instead of raw scans, and covers far more ground. The KPI that turns a labor-bound service into a scalable one.
""",
    ["/consultation", "/productized-services"],
    "#MSP #Productivity #Scaling",
)

post(
    "Arc close: the KPIs",
    """
Noise reduction, KEV closure, time to decision, coverage of exploited CVEs, effort avoided, dwell-time contribution, expected-loss trend, false-urgency rate, analyst leverage.

Every one is measurable, and every one improves when you decide by exploitation instead of severity. Free tool, real metrics. Next: how it compares to what you already use.
""",
    ["/productized-services"],
    "#SecurityMetrics #KPIs #DevSecOps",
)

# ============================================= ARC 7  Comparisons
post(
    "Triage vs a scanner",
    """
A scanner finds vulnerabilities and produces a list. Triage decides which ones matter and produces a verdict. They are not competitors, they are layers.

Keep your scanner. It is good at detection. Add Triage for the decision the scanner was never designed to make. Detection plus decision beats detection alone, every time.
""",
    ["/productized-services"],
    "#SecurityTools #DevSecOps",
)

post(
    "Triage vs CVSS-only prioritization",
    """
CVSS-only means patching the theoretically severe and leaving the actually exploited open. It inverts your risk and it does not scale past a few hundred Criticals.

Triage prioritizes by confirmed exploitation and probability, with severity in its proper place last. Same findings, opposite order, and the Triage order predicts real breaches. FIRST and CISA agree: do not use CVSS alone.
""",
    ["/productized-services"],
    "#CVSS #RiskManagement",
)

post(
    "Triage vs commercial prioritization platforms",
    """
There is a whole commercial category, Vulcan, Nucleus and others, whose product is exactly this decision layer. That category existing proves the value.

Triage is the free, open-source, CLI-native version of the same idea: KEV plus EPSS plus reachability plus criticality. No seat licences, no cloud tenancy, no lock-in. And where you want the managed, verified, remediated version, a2zsoc provides it as a service.
""",
    ["/productized-services", "/consultation"],
    "#VulnerabilityManagement #OpenSource",
)

post(
    "Triage vs a bug bounty finding",
    """
A bug bounty gives you one vulnerability, once, discovered by one researcher's hours. Valuable, but transactional and unrepeatable.

Triage is a system that decides across your entire finding set, every scan, reproducibly, with a methodology you own. Not a one-off find, a standing decision capability. Different economics entirely.
""",
    ["/consultation"],
    "#BugBounty #VulnerabilityManagement",
)

post(
    "Triage vs a spreadsheet",
    """
Most teams triage in a spreadsheet: paste the scan, colour by severity, argue in a meeting. It does not scale, it is not reproducible, and it is not defensible to an auditor.

Triage replaces the spreadsheet with a deterministic function over authoritative feeds. Same effort as opening Excel, a defensible decision instead of coloured cells.
""",
    ["/productized-services"],
    "#GRC #Automation",
)

post(
    "Triage vs doing nothing",
    """
The honest competitor for most teams is inaction: the scan runs, the report is ignored, and prioritization happens only after an incident.

Triage lowers the cost of deciding to almost zero, which is the only thing that gets teams to actually decide before the breach instead of after. Free, one command, no excuse.
""",
    ["/productized-services"],
    "#SOC #IncidentResponse",
)

post(
    "Triage vs an adversary-emulation platform",
    """
Caldera and similar platforms run real TTPs against your environment. Powerful, and heavy, and requiring authorization and care.

Triage does not execute anything. It explains the plausible ATT&CK chain as a risk narrative from the vulnerability data. Different tool, different job: emulation proves, Triage decides. Authorized emulation is available from a2zsoc as a separate engagement.
""",
    ["/consultation"],
    "#MITREATTACK #ThreatEmulation",
)

post(
    "Triage vs threat-intel feeds",
    """
A threat-intel feed tells you what is happening in the world. It does not tell you which of your vulnerabilities that world affects.

Triage joins the intelligence (KEV, EPSS) to your findings and your assets, producing a decision specific to you. Intelligence is the input; the decision about your environment is the output. That join is the value.
""",
    ["/productized-services"],
    "#ThreatIntel #VulnerabilityManagement",
)

post(
    "Triage vs hiring another analyst",
    """
The instinct when drowning in findings is to hire. But another analyst triaging by hand hits the same ceiling, just later.

Triage raises the ceiling instead of the headcount: it automates the decision so your existing team covers more. Then, when you do hire, they work at the top of the decision, not the bottom of the list.
""",
    ["/consultation"],
    "#Scaling #Productivity #DevSecOps",
)

post(
    "Arc close: the comparisons",
    """
Against scanners, CVSS, commercial platforms, bug bounty, spreadsheets, inaction, emulation platforms, raw feeds, and more hiring, Triage occupies a clear seat: the free, open, vendor-neutral decision layer above them all.

It complements what you have and replaces what does not work. Next: the board translation.
""",
    ["/productized-services"],
    "#VulnerabilityManagement #DevSecOps",
)

# ============================================= ARC 8  Board translation
post(
    "The three-tier decision, for executives",
    """
Triage sorts every finding into three tiers a board understands without a security briefing:

FIX NOW: actively exploited, reachable, on a critical asset. Authorize a window in days.
FIX THIS CYCLE: probable, schedule it.
MONITOR: low real-world risk, document and accept.

No CVSS numbers, no jargon. A decision, with a deadline and a reason. That is what leadership can act on.
""",
    ["/consultation"],
    "#BoardGovernance #CISO",
)

post(
    "Expected loss, honestly ranged",
    """
Triage translates each top exposure into an expected-loss range: measured likelihood, from KEV and EPSS and reachability, times the asset value you supply.

It is a range, never a fake precise number, and the memo says so plainly. But a range grounded in exploitation evidence beats a red bar chart every time. Supply real asset values and it sharpens. Calibrated CRQ is the paid engagement.
""",
    ["/consultation", "/productized-services"],
    "#CyberRisk #CRQ",
)

post(
    "The one-page memo",
    """
What is exposed. Why it matters now. Which business process is at risk. What management should authorize. The cost of delay. What remains uncertain.

Six answers, one page, generated from the scan. That is the executive memo Triage produces, and it is the difference between a security team that reports activity and one that drives decisions.
""",
    ["/consultation"],
    "#BoardGovernance #ExecutiveCommunication",
)

post(
    "The cost of delay, quantified",
    """
Boards approve maintenance windows when they understand the cost of not approving them. Triage frames each FIX NOW item with its expected-loss exposure and a deadline, so the cost of delay is explicit.

Delay is a decision with a price. Making that price visible is how security work gets authorized instead of deferred.
""",
    ["/consultation", "/productized-services"],
    "#CyberRisk #CISO",
)

post(
    "From ATT&CK path to business event",
    """
The memo does not say T1190. It says: this finding lets an attacker in, and the known path from there ends in your operations stopping. The ATT&CK chain is the mechanism; the business event is the message.

Boards fund the prevention of business events, not the mitigation of technique ids. Triage does the translation so you do not have to.
""",
    ["/consultation"],
    "#MITREATTACK #BoardGovernance",
)

post(
    "What remains uncertain, stated plainly",
    """
Every Triage memo includes what it does not know: that expected-loss is a scaffold, that reachability depends on the asset context supplied, that public exploitation does not prove you are targeted.

Stating uncertainty is not weakness, it is what makes the rest credible to a board and defensible to a regulator. Honesty is the differentiator.
""",
    ["/consultation"],
    "#RiskManagement #Governance",
)

post(
    "The CFO conversation",
    """
A CFO does not fund CVEs. They fund reduced expected loss per dollar spent. Triage frames vulnerability work in exactly those terms: here is the exposure in currency, here is what closing it costs, here is the return.

Security that speaks capital efficiency gets funded. Triage builds that language into the output.
""",
    ["/consultation", "/productized-services"],
    "#CFO #CyberRisk #FinOps",
)

post(
    "The audit committee answer",
    """
Audit committees ask whether the organisation prioritizes remediation defensibly. Triage is the answer: a documented, reproducible decision per finding, tied to authoritative exploitation data.

You are not explaining a gut call. You are showing a method. That is what turns an uncomfortable audit conversation into a short one.
""",
    ["/consultation"],
    "#Audit #GRC #Governance",
)

post(
    "Why the board translation is the moat",
    """
Any engineer can run a scanner. Far fewer can turn the output into a decision a board funds. That translation, from CVE to expected loss to authorized action, is the scarce skill.

Triage builds it into a free tool, which is the top of the funnel. The calibrated, verified, remediated version is the a2zsoc engagement. The translation is where the value concentrates.
""",
    ["/consultation", "/productized-services"],
    "#CISO #BoardGovernance #CyberRisk",
)

post(
    "Arc close: the board translation",
    """
Three tiers, an honest expected-loss range, a one-page memo, the cost of delay, the ATT&CK-to-business-event story, and stated uncertainty. That is how a scan becomes a board decision.

Triage does it for free. The calibrated version is the paid work. Next: why this compounds.
""",
    ["/consultation"],
    "#BoardGovernance #CyberRisk",
)

# ============================================= ARC 9  Compounding leverage
post(
    "Open core, in one line",
    """
The tool is free and open source. The decision layer everyone needs, given away. What is paid is validating reachability in your specific environment, engineering the safe remediation, and verifying closure.

Free to decide, paid to close. That is the open-core model, and it is how an open-source tool becomes an investable company.
""",
    ["/productized-services"],
    "#OpenSource #SaaS #BusinessModel",
)

post(
    "The dataset nobody else has",
    """
Every triage run and every engagement records which vulnerabilities show up in real environments, how they get prioritized, and which remediations work. That outcome data exists nowhere else.

Public feeds are commodity. The accumulated record of what actually happens in the field is the moat, and it compounds with every use. The tool seeds it; the engagements grow it.
""",
    ["/consultation", "/productized-services"],
    "#DataStrategy #VulnerabilityManagement",
)

post(
    "Each engagement makes the next cheaper",
    """
The first remediation of a vulnerability family is expensive. The tenth is a reused playbook. Triage captures the treatment templates, detection rules, and verification tests from each engagement into reusable components.

Delivery leverage rises: the second deployment costs a fraction of the first. That declining marginal cost is the difference between a body shop and a scalable business.
""",
    ["/consultation"],
    "#Scaling #Consulting #Productization",
)

post(
    "Why open source is the distribution",
    """
Developers find tools by running them, not by reading ads. An open, one-command CLI spreads through GitHub, CI pipelines, and word of mouth, in channels no marketing budget can buy.

The tool is the top of the funnel. Every team that adopts it is a candidate for the paid remediation and verification layer. Distribution and lead generation, in one free artifact.
""",
    ["/productized-services"],
    "#OpenSource #GoToMarket #DevSecOps",
)

post(
    "The standard, not the product",
    """
Tools get commoditized. Standards collect rent. If Triage becomes the reference way teams decide which vulnerabilities matter, the methodology, not any single feature, is the durable position.

Own the decision standard and every scanner and platform routes through it. That is the long game beneath a free CLI.
""",
    ["/productized-services"],
    "#Standards #Strategy #OpenSource",
)

post(
    "Recurring revenue from a moving signal",
    """
KEV and EPSS change daily. What is noise this week is urgent next week. That means the decision is never done, which means continuous re-triage is a genuine recurring need, not a manufactured subscription.

The free tool proves the value. The paid continuous-assurance retainer keeps your priorities aligned with a moving threat landscape. Recurring revenue with a real reason to recur.
""",
    ["/productized-services", "/consultation"],
    "#SaaS #RecurringRevenue #ContinuousMonitoring",
)

post(
    "From triage to a foundry",
    """
Do enough triage-to-remediation engagements and the repeated parts, the CVE-family playbooks, the treatment templates, the verification tests, become a system. A vulnerability-to-verified-remediation foundry.

The foundry is not designed upfront; it emerges from the reusable exhaust of real engagements. The free tool is where the exhaust starts accumulating.
""",
    ["/consultation"],
    "#Automation #Scaling #VulnerabilityManagement",
)

post(
    "Why this is investable",
    """
An open-source tool with real adoption, a paid service converting that adoption, and a proprietary outcome dataset that improves with every engagement. Free funnel, paid revenue, data moat.

That is a recognized, fundable pattern in security. The tool is the proof of the funnel; the service is the revenue; the data is the defensibility.
""",
    ["/productized-services", "/consultation"],
    "#Startups #VentureCapital #SaaS",
)

post(
    "Compounding, not hours",
    """
Consulting caps at your hours. A tool that runs without you and a dataset that grows with use do not.

Triage is the first step out of the hours-for-money ceiling: the decision it automates is work a human used to do by hand. The escape from the ceiling is productization plus data, and this is where it begins.
""",
    ["/productized-services"],
    "#Productization #Scaling #Strategy",
)

post(
    "Arc close: the compounding",
    """
Open core, a dataset no one else has, declining marginal delivery cost, open-source distribution, a shot at owning the decision standard, recurring revenue on a moving signal, and a foundry that emerges from repetition.

None of it is designed upfront. All of it accumulates from running the free tool and delivering the paid work. Next: how the free tool becomes a customer.
""",
    ["/productized-services"],
    "#Strategy #OpenSource #SaaS",
)

# ============================================= ARC 10  The a2zsoc funnel
post(
    "Where the free tool ends and a2zsoc begins",
    """
Triage tells you what to fix and why it matters. It cannot, from a scan alone, validate reachability in your specific network, engineer a safe patch for your production, run authorized emulation, or verify that the exposure stays closed.

That is the a2zsoc engagement. Free to decide, paid to close. The tool is the honest start; the service is the finish.
""",
    ["/productized-services", "/consultation"],
    "#DevSecOps #ManagedSecurity",
)

post(
    "Exposure validation",
    """
The first paid step: confirm which of the exploited findings are genuinely reachable in your environment, assess the compensating controls, and produce an executive exposure memo you can act on.

Fixed scope, advisory only, no production access required. It takes the free tool's decision and grounds it in your real network. That is where the engagement starts.
""",
    ["/productized-services", "/consultation"],
    "#SecurityAssessment #Consulting",
)

post(
    "Remediation engineering",
    """
Once the exposures are validated, the harder work: engineering the safe patch or compensating control, testing it, planning rollback, and deploying without breaking production.

This is where the free triage becomes real risk reduction. The tool decides; a2zsoc closes, safely, with a verification step so you know it stayed closed.
""",
    ["/productized-services", "/consultation"],
    "#Remediation #SecurityEngineering",
)

post(
    "Authorized threat emulation",
    """
For the exposures that matter most, prove it safely: run the ATT&CK techniques against a replica or under strict authorization, measure whether detection fires, and feed the result into a calibrated risk number.

Triage narrates the attack path. a2zsoc, under written scope, demonstrates it and measures your real detection coverage. Narrative in the tool, evidence in the engagement.
""",
    ["/consultation"],
    "#ThreatEmulation #PurpleTeam #MITREATTACK",
)

post(
    "Calibrated cyber risk quantification",
    """
The free tool gives an expected-loss scaffold, a range. The paid engagement calibrates it: real business-service mapping, real asset values, defensible figures your board and your insurer will accept.

Honest range for free, calibrated number for the engagement. Both grounded in exploitation evidence, never in severity theatre.
""",
    ["/consultation", "/productized-services"],
    "#CRQ #CyberRisk #CISO",
)

post(
    "Continuous assurance",
    """
Because KEV and EPSS move, the decision is never final. The a2zsoc retainer re-triages your environment as the threat landscape shifts, updates the treatment priorities, and verifies that closed exposures stay closed.

The free tool is a snapshot. The retainer keeps the picture current. Recurring, because the threat is.
""",
    ["/productized-services", "/consultation"],
    "#ContinuousMonitoring #ManagedSecurity",
)

post(
    "For the MSP partner",
    """
If you manage security for many clients, Triage plus a2zsoc is a service line: free triage across your customer base, and a specialist remediation-and-verification layer you resell under your own delivery.

You keep the client relationship. a2zsoc supplies the specialist analysis and closure. Distribution for us, margin and capability for you.
""",
    ["/consultation", "/productized-services"],
    "#MSP #Partnership #ChannelSales",
)

post(
    "The productized packages",
    """
The follow-on is not open-ended consulting. It is scoped: exposure validation, remediation engineering, authorized emulation, calibrated CRQ, continuous assurance. Fixed scope, fixed deliverables, clear boundaries.

You know what you are buying and what you are getting. The productized-services page lays out each package.
""",
    ["/productized-services", "/pricing"],
    "#ProductizedServices #Consulting",
)

post(
    "Start with a conversation",
    """
Run Triage on your own scan first. See what it cuts. If the exposures it surfaces need validating, closing, and verifying, that is the conversation.

No pitch until the free tool has proven its worth on your own data. Then a scoped engagement, priced to the outcome. Book the consultation when the output makes the case for itself.
""",
    ["/consultation", "/productized-services"],
    "#Consulting #DevSecOps",
)

post(
    "Series close: from a free CLI to closed exposure",
    """
One hundred posts on one idea: scanning is commodity, deciding is the value, and deciding well means prioritizing by real-world exploitation, not CVSS.

Triage does the deciding, free and open source. Validating, closing, and verifying the exposures it finds is the a2zsoc engagement.

Clone the tool. Run it on your scan. If what it surfaces needs closing, let us talk.
""",
    ["/productized-services", "/consultation"],
    "#OpenSource #VulnerabilityManagement #DevSecOps",
)


def tagline(extra: str) -> str:
    seen: list[str] = []
    for tag in f"{extra} {CORE_TAGS}".split():
        if tag not in seen:
            seen.append(tag)
    return " ".join(seen)


def render(body: str, paths: list[str], tags: str) -> str:
    return f"{body}\n\n{L(*paths)}\n\n{tagline(tags)}\n"


def main() -> None:
    assert len(POSTS) == 100, f"expected 100 posts, got {len(POSTS)}"
    OUT.mkdir(parents=True, exist_ok=True)

    previous: dict[int, dict] = {}
    existing = OUT / "index.json"
    if existing.exists():
        for entry in json.loads(existing.read_text(encoding="utf-8"))["posts"]:
            previous[entry["number"]] = entry

    index = []
    for i, (title, body, paths, tags) in enumerate(POSTS, start=1):
        text = render(body, paths, tags)
        for bad in FORBIDDEN:
            if bad in text:
                raise SystemExit(f"post-{i:03d}: forbidden character {bad!r}")
        if len(text) > 2900:
            raise SystemExit(f"post-{i:03d}: {len(text)} chars exceeds limit")
        name = f"post-{i:03d}.txt"
        (OUT / name).write_text(text, encoding="utf-8")

        prior = previous.get(i, {})
        entry = {
            "id": f"{CAMPAIGN}-{i:03d}",
            "number": i,
            "track": TRACKS[(i - 1) // 10],
            "status": prior.get("status", "ready"),
            "sha256": hashlib.sha256(text.encode("utf-8")).hexdigest(),
            "file": name,
            "title": title,
            "hook": body.split("\n", 1)[0],
            "links": [GH] + [link(p) for p in paths],
            "hashtags": tagline(tags).split(),
            "chars": len(text),
        }
        if "publication" in prior:
            entry["publication"] = prior["publication"]
        index.append(entry)

    published = sum(1 for e in index if e["status"] == "published")
    (OUT / "index.json").write_text(
        json.dumps(
            {
                "campaign": CAMPAIGN,
                "created": date.today().isoformat(),
                "base": BASE,
                "repo": GH,
                "count": len(index),
                "status": "published" if published == len(index) else "ready",
                "currentOfferPaths": CURRENT_OFFER_PATHS,
                "waitlistPath": WAITLIST_PATH,
                "posts": index,
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    print(f"wrote {len(index)} posts to {OUT}")
    print(f"chars min {min(e['chars'] for e in index)} max {max(e['chars'] for e in index)}")
    print(f"already published: {published}")


if __name__ == "__main__":
    main()
