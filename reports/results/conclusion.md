The domain-grouped comparison selected **Random Forest** using validation phishing F1. On 46,632 held-out websites,
it achieved phishing F1 **0.9999** and recall **0.9998** at threshold 0.5.
The final comparison reports both linear and nonlinear classifiers rather than relying on accuracy alone.

The training-data HTTPS association test produced Cramer's V **0.602** and the decision **Reject H0** at alpha 0.05;
the expected lower HTTPS prevalence among phishing records was **True** in this sample.
This does not imply that HTTPS proves a website is safe.

These results support the feasibility of classification on this recorded dataset under the stated split, with important limits.
Remaining priorities are registered-domain and campaign audits, repeated grouped evaluation, confidence intervals,
feature-provenance verification, a URL-only comparison, temporal/external testing and cost-aware threshold selection.
No claim of production readiness or universal model superiority follows from the internal scores.
