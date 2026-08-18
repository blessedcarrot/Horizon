---
layout: item
title: "Old sqrt(DS) gap in multiclass sample complexity finally closed"
date: 2026-08-18 23:17:09 +0000
lang: en
theme: horizon-research
theme_name: "Horizon"
score: 8.0
link: "https://arxiv.org/abs/2604.24749"
source: "arXiv cs.LG"
edition_url: "/2026/08/18/2317-summary-en.html"
edition_title: "2026-08-18 23:17 UTC"
enriched: true
---
The paper proves that the maximum hypergraph density of any multiclass hypothesis class is upper-bounded by its DS dimension, resolving a conjecture of Daniely and Shalev-Shwartz from 2014. This closes a sqrt\(DS\) gap that had persisted between upper and lower bounds on the sample complexity of multiclass classification, giving an optimal characterization of that complexity in terms of the DS dimension. The same technique also settles the optimal sample complexity of list learning. The result builds directly on a very recent algebraic characterization of multiclass hypothesis classes by Hanneke et al., dated 2026, which the paper treats as an established input rather than proving itself.

rss · arXiv cs.LG · Aug 18, 04:00

**「Background」** For binary classification, the VC dimension pins down the optimal sample complexity exactly, but the analogous problem for multiclass classification, where the DS dimension is the relevant complexity measure, has resisted a tight answer for over a decade, leaving a sqrt\(DS\) gap between known upper and lower bounds. Daniely and Shalev-Shwartz conjectured in 2014 that a quantity called the maximum hypergraph density of a hypothesis class is bounded by its DS dimension, which would close that gap, but the conjecture remained open despite subsequent work on characterizing multiclass learnability. This paper builds on a very recent algebraic characterization of multiclass hypothesis classes \(Hanneke et al., cited as 2026\) to prove the conjecture directly.

**「What would make this matter」** This is a pure sample complexity theorem: it tells you the tight number of examples needed for PAC learning multiclass and list learning problems as a function of DS dimension, with no algorithmic or computational content attached. For it to matter beyond closing a gap in the theory literature, it would need the underlying Hanneke et al. \(2026\) characterization to hold up once that work is fully published and checked by the community, since this paper depends on it as a foundation rather than reproving it. Practical relevance would also require someone to translate the tight bound into learning algorithms whose sample requirements actually approach this theoretical optimum, since matching an information-theoretic bound is distinct from having an efficient learner that achieves it.

**「Maturity」** This is a theoretical proof settling a long-open question in statistical learning theory, not an empirical or applied result. Its correctness rests partly on a cited 2026 result that has not yet had time for independent community verification.

<details><summary>References</summary>
<ul>
<li><a href="https://openreview.net/pdf?id=l2yvtrz3On">Improved Sample Complexity for Multiclass PAC Learning Steve Hanneke</a></li>
<li><a href="https://arxiv.org/html/2604.24749v1">The Optimal Sample Complexity of Multiclass and List Learning</a></li>
<li><a href="https://eccc.weizmann.ac.il/report/2022/035/download/">A CHARACTERIZATION OF MULTICLASS LEARNABILITY</a></li>

</ul>
</details>

**Tags**: `#learning theory`, `#sample complexity`, `#multiclass classification`, `#VC/DS dimension`, `#theoretical computer science`
