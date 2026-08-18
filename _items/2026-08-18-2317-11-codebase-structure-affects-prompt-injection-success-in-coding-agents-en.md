---
layout: item
title: "Codebase Structure Affects Prompt Injection Success in Coding Agents"
date: 2026-08-18 23:17:09 +0000
lang: en
theme: reliability-assurance
theme_name: "Reliability & Assurance"
score: 7.0
link: "https://arxiv.org/abs/2608.14876"
source: "arXiv cs.AI"
edition_url: "/2026/08/18/2317-summary-en.html"
edition_title: "2026-08-18 23:17 UTC"
enriched: true
---
An empirical study finds that the structure of a codebase, not just its content, measurably influences whether indirect prompt injection attacks succeed against agentic coding assistants. The researchers tested three injection entry points across open-source repositories spanning 10 programming languages and 6 engineering domains, using open-weight models running on open source code harnesses. They report that codebase modularity significantly changes Attack Success Rate, with highly modular environments showing markedly lower success rates, and that context framing and the presence of security-related cues in the workspace also shift outcomes. The abstract available does not give the specific numeric ASR values, and the work targets open-weight models and open harnesses rather than commercial deployed products.

rss · arXiv cs.AI · Aug 18, 04:00

**「Background」** Agentic coding assistants are trusted to read and act on third-party code because they operate with broad filesystem access inside developer workspaces, an arrangement assumed to be safe as long as the model itself resists malicious instructions embedded in ingested files. This study questions that assumption by showing that the surrounding workspace, its directory depth, file organization, and modularity, is itself a variable that attackers or evaluators can exploit or must account for, independent of the injected payload&\#x27;s content.

**「Exposure」** The demonstrated effect applies to organizations running agentic coding assistants built on open-weight models with open source code harnesses, in setups where the agent ingests third-party or externally sourced code with filesystem access. Teams should check how modular their typical ingested codebases are, where in a workspace injected instructions might plausibly appear \(directory depth, file position\), and whether their security testing environments are representative of production repository structures. The study does not establish that the same effect sizes hold for closed commercial coding assistants or proprietary harnesses, so exposure for those deployments is unconfirmed rather than ruled out.

**「Mitigation」** No patch or product fix is implicated since this is a research finding about attack surface rather than a specific software defect. The authors suggest that increasing codebase modularity is associated with lower attack success rates, and that security testing of coding agents should use uncontaminated, structurally realistic test environments to produce reliable conclusions; treating workspace topology as a variable in red-teaming and evaluation is a practical near-term compensating step.

**Tags**: `#prompt injection`, `#agentic coding assistants`, `#supply chain security`, `#AI agents`, `#empirical security research`
