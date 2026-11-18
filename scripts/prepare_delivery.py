"""Package an already executed notebook, results and an English presentation."""
from pathlib import Path
import base64
import html
import json
import nbformat
import pandas as pd
from nbconvert import HTMLExporter

root = Path(__file__).resolve().parents[1]
notebook = root / 'notebooks' / '01_analysis_and_modeling.ipynb'
presentation = root / 'reports' / 'presentation'
presentation.mkdir(parents=True, exist_ok=True)
out = root / 'reports' / 'results'
nb = nbformat.read(notebook, as_version=4)
nbformat.validate(nb)
code_cells = [c for c in nb.cells if c.cell_type == 'code']
assert all(c.execution_count is not None for c in code_cells)
assert not [o for c in code_cells for o in c.outputs if o.output_type == 'error']
body, _ = HTMLExporter(template_name='lab').from_notebook_node(nb)
(root / 'reports' / 'analysis.html').write_text(body, encoding='utf-8')
meta = json.loads((out/'run_metadata.json').read_text(encoding='utf-8'))
results = pd.read_csv(out/'test_metrics.csv', index_col=0)
errors = pd.read_csv(out/'test_errors.csv', index_col=0)
splits = pd.read_csv(out/'split_summary.csv')
hypothesis = pd.read_csv(out/'hypothesis_test.csv', index_col=0).iloc[:,0]
winner = meta['preferred_model_from_validation']
r = results.loc[winner]
e = errors.loc[winner]
def esc(s): return html.escape(str(s))
def image(name, alt):
    data = base64.b64encode((out/name).read_bytes()).decode('ascii')
    return f'<img alt="{esc(alt)}" src="data:image/png;base64,{data}">'
def bullets(*items): return '<ul>'+''.join(f'<li>{item}</li>' for item in items)+'</ul>'

slides = []
notes = []
def slide(title, content, seconds, note):
    slides.append(f'<section><p class="eyebrow">PHISHING DETECTION / MACHINE LEARNING</p><h1>{title}</h1>{content}<footer>{len(slides)+1} / 11 · Target: {seconds} seconds</footer></section>')
    notes.append(f'## Slide {len(slides)} — {title} ({seconds} seconds)\n\n{note}\n')
slide('Detection of Phishing Websites Using Machine Learning',
      '<p class="lead">A comparison of Logistic Regression and Random Forest with domain-separated evaluation.</p><p>Add group-member names before presenting.</p>',
      30, 'Introduce every member. Explain that phishing websites imitate trusted services to deceive users. Our project evaluates an offline classifier, not a deployed browser protection system.')
slide('Research question and hypothesis', bullets(
      'How well do two classifiers distinguish phishing and legitimate websites on unseen observed domains?',
      'H0: HTTPS usage and website class are independent.',
      'H1: HTTPS usage is associated with class, with lower prevalence among phishing records.',
      'Primary model comparison metric: phishing F1; validation chooses the preferred model.'),
      50, 'Distinguish the association hypothesis from the predictive research question. Explain why recall alone could produce too many false alarms and why accuracy alone can hide missed attacks.')
slide('Dataset and label meaning',bullets(
      f'PhiUSIIL, UCI: {meta["original_rows"]:,} original records and 56 CSV columns.',
      'Original labels: 0 = phishing; 1 = legitimate. Our positive target is is_phishing = 1.',
      'Recorded URL structure and webpage-content features; this is not a URL-only experiment.',
      'A 56-variable working dictionary distinguishes documented facts from inferred feature meanings.'),
      55, 'Credit Prasad and Chandra and UCI. Point out that a reversed positive-class convention would make phishing recall misleading. Some feature formulas could not be verified, and the dictionary says so.')
slide('Quality checks and split design',bullets(
      f'{meta["original_rows"]-meta["deduplicated_rows"]:,} repeated exact URLs removed under a first-record rule; raw CSV unchanged.',
      'Missing values and placeholders audited; imputation fitted only on training data.',
      'Approximately 60/20/20 observed-domain-grouped split; exact domain and URL overlaps are asserted absent.',
      'Raw identifiers/text and three unverified reference-based scores excluded.'
      ) + splits[['Partition','Rows','Phishing percent']].round(2).to_html(index=False,border=0),
      65, 'Explain why a random row split can share repeated domains across partitions. We prevent identical observed domains from crossing, but different subdomains or campaigns may still overlap. Group proportions differ from row proportions.')
slide('EDA: feature distributions',image('02_url_domain_lengths.png','URL and domain length distributions'),
      55, 'Describe the observed distribution differences shown in the actual chart. Log1p makes long tails readable and does not remove records. Explain why a long URL alone cannot establish malicious intent. The notebook contains additional class-balance, content, TLD and correlation figures.')
slide('HTTPS association: evidence and caution',image('04_https_prevalence.png','HTTPS prevalence by website class')+
      f'<p>Cramer’s V = <strong>{hypothesis["Cramers V"]:.3f}</strong>; HTTPS prevalence gap = <strong>{100*hypothesis["Legitimate minus phishing HTTPS rate"]:.2f} percentage points</strong>.</p>',
      60, 'Report rejection of independence at alpha 0.05 if confirmed in the notebook. The displayed zero p-value is numeric underflow. Discuss within-domain dependence and the one-record-per-domain sensitivity check. HTTPS encrypts transport; it does not certify a safe website. Collection bias may explain part of the pattern.')
slide('Two models, one evaluation protocol',bullets(
      'Logistic Regression: train-fitted median imputation → fixed log1p → standardization → balanced classifier.',
      'Random Forest: train-fitted median imputation → 120 trees, depth limit 18, balanced class weights.',
      f'{len(meta["predictors"])} numeric features; categorical encoding is unnecessary because text/TLD predictors are excluded.',
      'Fixed threshold 0.5; no hyperparameter search; majority-class baseline included.'),
      60, 'Explain linear log-odds versus nonlinear tree interactions, why Logistic Regression needs scaling and why Random Forest does not. Class weighting changes training penalties rather than duplicating rows. The original target and grouping identifiers never enter X.')
slide('Held-out model comparison',results[['Accuracy','Precision (phishing)','Recall (phishing)','F1 (phishing)']].round(4).to_html(border=0)+
      f'<p>Validation-selected model: <strong>{esc(winner)}</strong>. Test F1: <strong>{r["F1 (phishing)"]:.4f}</strong>.</p>',
      65, 'Read the phishing metrics, not only accuracy. The preferred model was selected on validation F1, before final test reporting. These are results from one internal split; the gap does not prove statistically significant or universal superiority.')
slide('What do the errors mean?',image('07_confusion_matrices.png','Confusion matrices for all classifiers')+
      f'<p>{esc(winner)}: <strong>{int(e["Missed phishing"]):,}</strong> missed phishing sites; <strong>{int(e["False alarms"]):,}</strong> legitimate sites flagged.</p>',
      60, 'Define false negative as phishing predicted legitimate, and false positive as legitimate predicted phishing. Discuss harm to users versus disruption to legitimate businesses. A production threshold would depend on costs and real deployment prevalence.')
slide('Limitations, ethics and next steps',bullets(
      'Collection and HTTPS bias; unknown extraction provenance; possible campaign/template dependence.',
      'No independent current dataset, temporal test or confidence intervals.',
      'Content features require safe page retrieval; protect personal URL information.',
      'Next: registered-domain audits, repeated grouped validation, URL-only comparison and external testing.',
      'Use predictions to support review and appeal; avoid irreversible automated blocking.'),
      60, 'Explain why high internal scores do not guarantee future detection. A lower phishing base rate can reduce alert precision. Describe one concrete improvement that you would prioritize and why.')
slide('Conclusion and references',
      f'<p class="lead">{esc(winner)} achieved phishing F1 <strong>{r["F1 (phishing)"]:.4f}</strong> under the stated internal evaluation.</p>'+
      '<p>Predictive performance is promising within this dataset; external generalization remains unverified.</p>'+
      '<p>Prasad &amp; Chandra (2024), PhiUSIIL dataset, UCI. CC BY 4.0.<br>Paper DOI: 10.1016/j.cose.2023.103545.<br>Methods: scikit-learn and SciPy documentation. Full references in the notebook.</p>',
      40, 'Conclude with the research question and a bounded answer. Credit the dataset and method sources. Invite questions and ensure every member can explain preprocessing, label recoding, confusion matrices and leakage controls.')

template = '''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Phishing Detection — Project Presentation</title>
<style>*{box-sizing:border-box}body{margin:0;background:#0c1828;color:#172c45;font-family:Arial,sans-serif}section{display:none;background:#fff;min-height:100vh;padding:4vh 6vw 7vh;position:relative}section.active{display:block}.eyebrow{font-size:14px;letter-spacing:2px;color:#3379a5}h1{font-size:clamp(28px,3.5vw,48px);margin:14px 0 24px}p,li{font-size:clamp(17px,1.65vw,24px);line-height:1.45}li{margin:12px 0}.lead{font-size:clamp(23px,2.5vw,36px)}img{display:block;max-height:54vh;max-width:100%;object-fit:contain;margin:auto}table{border-collapse:collapse;font-size:clamp(14px,1.4vw,21px);width:100%;margin:20px 0}th,td{padding:12px;text-align:left;border-bottom:1px solid #dbe4ed}th{background:#eaf1f8}footer{position:absolute;bottom:22px;font-size:14px;color:#536b80}nav{position:fixed;bottom:12px;right:18px;z-index:5}button{border:0;padding:10px 18px;margin-left:6px;background:#183c5f;color:#fff;border-radius:6px;cursor:pointer}@media print{section{display:block!important;min-height:0;height:185mm;break-after:page;padding:12mm}nav{display:none}img{max-height:110mm}body{background:white}@page{size:A4 landscape;margin:0}}</style>
BODY<nav><button onclick="move(-1)">← Previous</button><button onclick="move(1)">Next →</button></nav>
<script>let current=0;const slides=[...document.querySelectorAll('section')];function show(){slides.forEach((s,i)=>s.classList.toggle('active',i===current));location.hash=current+1}function move(n){current=Math.max(0,Math.min(slides.length-1,current+n));show()}document.addEventListener('keydown',e=>{if(['ArrowRight','PageDown',' '].includes(e.key)){e.preventDefault();move(1)}if(['ArrowLeft','PageUp'].includes(e.key)){e.preventDefault();move(-1)}});const initial=Number(location.hash.slice(1));if(initial>0&&initial<=slides.length)current=initial-1;show();</script></html>'''
(presentation/'presentation.html').write_text(template.replace('BODY',''.join(slides)),encoding='utf-8')
outline = '''# English presentation — speaker notes

**Total planned speaking time: 10 minutes.** Open `presentation.html` in a browser. Use arrow keys or the Next/Previous buttons. Print to PDF in landscape orientation if a PDF is required. Figures are embedded, so the deck can be shared as a single HTML file.

Add member names on the title slide before submission. Divide slides according to the actual group size: for example, research/data, EDA/statistics, models/results, limitations/conclusion. Every member must speak and understand the entire workflow. Rehearse transitions and keep the full presentation between 8 and 12 minutes.

'''+ '\n'.join(notes)+'''
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
'''
(presentation/'presentation_outline.md').write_text(outline,encoding='utf-8')
print(f'Validated {len(code_cells)} executed code cells; exported notebook, browser view, presentation and documentation.')
