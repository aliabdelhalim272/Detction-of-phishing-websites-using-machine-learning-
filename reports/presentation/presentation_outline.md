# English presentation — speaker notes

**Total planned speaking time: 10 minutes.** Open `presentation.html` in a browser. Use arrow keys or the Next/Previous buttons. Print to PDF in landscape orientation if a PDF is required. Figures are embedded, so the deck can be shared as a single HTML file.

Add member names on the title slide before submission. Divide slides according to the actual group size: for example, research/data, EDA/statistics, models/results, limitations/conclusion. Every member must speak and understand the entire workflow. Rehearse transitions and keep the full presentation between 8 and 12 minutes.

## Slide 1 — Detection of Phishing Websites Using Machine Learning (30 seconds)

Introduce every member. Explain that phishing websites imitate trusted services to deceive users. Our project evaluates an offline classifier, not a deployed browser protection system.

## Slide 2 — Research question and hypothesis (50 seconds)

Distinguish the association hypothesis from the predictive research question. Explain why recall alone could produce too many false alarms and why accuracy alone can hide missed attacks.

## Slide 3 — Dataset and label meaning (55 seconds)

Credit Prasad and Chandra and UCI. Point out that a reversed positive-class convention would make phishing recall misleading. Some feature formulas could not be verified, and the dictionary says so.

## Slide 4 — Quality checks and split design (65 seconds)

Explain why a random row split can share repeated domains across partitions. We prevent identical observed domains from crossing, but different subdomains or campaigns may still overlap. Group proportions differ from row proportions.

## Slide 5 — EDA: feature distributions (55 seconds)

Describe the observed distribution differences shown in the actual chart. Log1p makes long tails readable and does not remove records. Explain why a long URL alone cannot establish malicious intent. The notebook contains additional class-balance, content, TLD and correlation figures.

## Slide 6 — HTTPS association: evidence and caution (60 seconds)

Report rejection of independence at alpha 0.05 if confirmed in the notebook. The displayed zero p-value is numeric underflow. Discuss within-domain dependence and the one-record-per-domain sensitivity check. HTTPS encrypts transport; it does not certify a safe website. Collection bias may explain part of the pattern.

## Slide 7 — Two models, one evaluation protocol (60 seconds)

Explain linear log-odds versus nonlinear tree interactions, why Logistic Regression needs scaling and why Random Forest does not. Class weighting changes training penalties rather than duplicating rows. The original target and grouping identifiers never enter X.

## Slide 8 — Held-out model comparison (65 seconds)

Read the phishing metrics, not only accuracy. The preferred model was selected on validation F1, before final test reporting. These are results from one internal split; the gap does not prove statistically significant or universal superiority.

## Slide 9 — What do the errors mean? (60 seconds)

Define false negative as phishing predicted legitimate, and false positive as legitimate predicted phishing. Discuss harm to users versus disruption to legitimate businesses. A production threshold would depend on costs and real deployment prevalence.

## Slide 10 — Limitations, ethics and next steps (60 seconds)

Explain why high internal scores do not guarantee future detection. A lower phishing base rate can reduce alert precision. Describe one concrete improvement that you would prioritize and why.

## Slide 11 — Conclusion and references (40 seconds)

Conclude with the research question and a bounded answer. Credit the dataset and method sources. Invite questions and ensure every member can explain preprocessing, label recoding, confusion matrices and leakage controls.

## Questions to rehearse

- Why is phishing positive when the source label for phishing is zero?
- Why use a domain-grouped split instead of a random row split?
- Which leakage risks remain after these controls?
- Why were three reference-based features excluded?
- Why does Logistic Regression use a scaler while Random Forest does not?
- What are the false-positive and false-negative costs?
- Why can HTTPS not prove legitimacy?
- What does the chi-square test assume, and what does Cramer's V add?
- Why is a high internal score insufficient for deployment?
- Which feature definitions are inferred rather than verified?

Brief scheduling note: the provided course sheet lists Room 318 on December 23 and December 30. Confirm your assigned date with the instructor.
