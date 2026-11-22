"""Build the course report, README and English presentation from frozen results.

Document-only dependencies are isolated in the workspace's .delivery-tools folder.
This script never trains a model, selects features or changes the test protocol.
"""
from pathlib import Path
import csv
import hashlib
import html
import json
import re
import sys
from xml.sax.saxutils import escape

ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT.parent/'.delivery-tools'))
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle,getSampleStyleSheet
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (SimpleDocTemplate,Paragraph,Spacer,Table,TableStyle,
                               Image,PageBreak,KeepTogether)
from reportlab.pdfgen import canvas
from pptx import Presentation
from pptx.util import Inches,Pt
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE

DELIVERY=ROOT/'submission/GroupXX_PhishingDetection'
PRESENTATION=ROOT/'presentation'
PRESENTATION.mkdir(exist_ok=True)
NAVY='#142B45';TEAL='#087E8B';GOLD='#C77825';PALE='#EAF3F5';INK='#24364A';GRAY='#546879'
MEMBERS=[('Meltem Orhan','221015002'),('Ali Abdel Halim','TO BE ADDED'),('Halil Trabzon','TO BE ADDED')]
DATA_URL='https://archive.ics.uci.edu/dataset/967/phiusiil+phishing+url+dataset'
DOWNLOAD='https://archive.ics.uci.edu/static/public/967/phiusiil+phishing+url+dataset.zip'
SOURCE_SHA='a236549cd369cd80bd478ff8e1779cbf44c58d5c3f79f7a51a1adbed7d06d1c6'

def read_csv(relative):
    with (ROOT/relative).open(encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f))

METRICS=read_csv('reports/final_evaluation/test_metrics.csv')
VALIDATION=read_csv('reports/final_evaluation/validation_test_comparison.csv')
REDUCTION=json.loads((ROOT/'reports/feature_reduction/protocol.json').read_text())
HYPOTHESIS=json.loads((ROOT/'reports/hypothesis/result.json').read_text())
FONT_DIR=Path('C:/Windows/Fonts')
pdfmetrics.registerFont(TTFont('Arial',str(FONT_DIR/'arial.ttf')))
pdfmetrics.registerFont(TTFont('ArialBold',str(FONT_DIR/'arialbd.ttf')))
pdfmetrics.registerFontFamily('Arial',normal='Arial',bold='ArialBold',italic='Arial',boldItalic='ArialBold')
STYLES=getSampleStyleSheet()
STYLES.add(ParagraphStyle(name='Body',fontName='Arial',fontSize=10,leading=14,textColor=INK,spaceAfter=8))
STYLES.add(ParagraphStyle(name='Heading',fontName='ArialBold',fontSize=17,leading=21,textColor=NAVY,spaceBefore=12,spaceAfter=12))
STYLES.add(ParagraphStyle(name='Subheading',fontName='ArialBold',fontSize=12,leading=16,textColor=TEAL,spaceBefore=8,spaceAfter=7))
STYLES.add(ParagraphStyle(name='SmallBody',fontName='Arial',fontSize=8.2,leading=11,textColor=GRAY,spaceAfter=6,splitLongWords=True))
STYLES.add(ParagraphStyle(name='Cell',fontName='Arial',fontSize=8.1,leading=10.5,textColor=INK,wordWrap='LTR'))
STYLES.add(ParagraphStyle(name='CellHead',fontName='ArialBold',fontSize=8.2,leading=10.5,textColor=colors.white))
STYLES.add(ParagraphStyle(name='Cover',fontName='ArialBold',fontSize=29,leading=35,textColor=NAVY,spaceAfter=20))

def para(text,style='Body'):
    return Paragraph(text,STYLES[style])

def safe(text):return escape(str(text))

def table(headers,rows,widths):
    data=[[para(safe(x),'CellHead') for x in headers]]
    data.extend([[para(safe(x),'Cell') for x in row] for row in rows])
    result=Table(data,colWidths=widths,repeatRows=1,hAlign='LEFT')
    result.setStyle(TableStyle([
        ('BACKGROUND',(0,0),(-1,0),colors.HexColor(NAVY)),('VALIGN',(0,0),(-1,-1),'TOP'),
        ('ROWBACKGROUNDS',(0,1),(-1,-1),[colors.white,colors.HexColor('#F0F5F8')]),
        ('LINEBELOW',(0,0),(-1,0),.5,colors.HexColor(TEAL)),
        ('LEFTPADDING',(0,0),(-1,-1),7),('RIGHTPADDING',(0,0),(-1,-1),7),
        ('TOPPADDING',(0,0),(-1,-1),7),('BOTTOMPADDING',(0,0),(-1,-1),7)]))
    return result

def image_flow(filename,width=495):
    path=ROOT/'reports/figures'/filename
    item=Image(str(path))
    item.drawHeight=item.imageHeight*width/item.imageWidth;item.drawWidth=width
    return item

def page_footer(canv,doc):
    canv.setStrokeColor(colors.HexColor('#D7E2EB'));canv.line(45,40,A4[0]-45,40)
    canv.setFont('Arial',8);canv.setFillColor(colors.HexColor(GRAY))
    canv.drawString(45,27,'GroupXX | Detection of Phishing Websites Using Machine Learning')
    canv.drawRightString(A4[0]-45,27,str(doc.page))

def references():
    import nbformat
    nb=nbformat.read(ROOT/'notebooks/01_eda.ipynb',4)
    source=next(c.source for c in nb.cells if c.cell_type=='markdown' and c.source.startswith('## 21.'))
    result=[]
    for entry in re.split(r'\n(?=\d+\. \*\*)',source):
        if re.match(r'\d+\. \*\*',entry):
            entry=entry.split('\n\n**Evidence generated')[0]
            entry=entry.replace('**','').replace('*','')
            entry=re.sub(r'\[([^\]]+)\]\(([^)]+)\)',lambda m:f'{m[1]} ({m[2]})',entry)
            result.append(' '.join(entry.split()))
    assert len(result)==17
    return result

def build_readme():
    req=(ROOT/'requirements-eda.txt').read_text().strip()
    text=f'''DETECTION OF PHISHING WEBSITES USING MACHINE LEARNING
GroupXX - academic project submission

BEFORE SUBMISSION
Replace GroupXX with the assigned group number in folder and file names.
Add Ali Abdel Halim's and Halil Trabzon's student IDs in this README,
the notebook title page and the report/presentation title pages.
Current files deliberately retain these unknown fields as TO BE ADDED.

GROUP MEMBERS
Meltem Orhan - 221015002
Ali Abdel Halim - TO BE ADDED
Halil Trabzon - TO BE ADDED

PROJECT DESCRIPTION
We study whether recorded URL and webpage features distinguish phishing from
legitimate websites in the PhiUSIIL dataset. The notebook documents integrity
checks, training-only EDA, a testable exploratory hypothesis, justified encoding
and scaling, a majority baseline, Logistic Regression, Random Forest, controlled
feature reduction, and a frozen internal test comparison. Source rows/values
are retained. Results do not establish performance on other datasets.

DATASET AND ATTRIBUTION
PhiUSIIL Phishing URL (Website), Arvind Prasad and Shalini Chandra, 2024.
UCI Machine Learning Repository, dataset 967. License: CC BY 4.0.
Dataset record: {DATA_URL}
Direct source download: {DOWNLOAD}
Associated paper: https://doi.org/10.1016/j.cose.2023.103545
dataset.csv is the original PhiUSIIL_Phishing_URL_Dataset.csv, renamed only.
235,795 rows; 56 columns. It has not been cleaned or overwritten in place.
SHA-256: {SOURCE_SHA}
Original label: 0 = phishing, 1 = legitimate.
Model target: y = 1 - label, so positive class 1 = phishing.
See notebook Section 3 for the full data dictionary and definition caveats.

SUBMITTED FILES
GroupXX_Project.ipynb - complete English notebook with saved tables/figures.
GroupXX_Report.pdf - English methods, findings, interpretation and references.
dataset.csv - original source data, required beside the notebook.
README.txt - attribution, group information and execution instructions.
The 8-12 minute English presentation and speaker notes are supplied separately
in the repository's presentation/ folder. No ZIP has been created.

HOW TO RUN
1. Extract/copy the entire submission folder to a writable local directory.
2. Use Python 3.12.10 (the tested interpreter) in a dedicated environment.
3. Install the exact libraries below. From this folder in PowerShell:
   python -m venv .venv
   .\\.venv\\Scripts\\python.exe -m pip install numpy==2.4.4 pandas==3.0.2 matplotlib==3.10.9 scikit-learn==1.8.0 scipy==1.17.1 nbformat==5.10.4 nbclient==0.11.0 nbconvert==7.17.1 ipykernel==7.2.0
4. Open GroupXX_Project.ipynb in VS Code with Python and Jupyter extensions
   (or an existing Jupyter frontend), and select this environment as the kernel.
5. Restart the kernel and Run All from the first cell to the last.
   Keep dataset.csv beside the notebook. No src/, docs/, downloaded model,
   API, network access or previously generated experiment files are required.
6. The notebook creates data/processed/ and reports/ under its working folder.
   These include split manifests, audit tables and image files. They are outputs,
   not additional inputs. Running may take several minutes and use significant
   memory; elapsed times depend on the computer. Random Forest uses two workers.
7. Save the executed notebook so every table and figure remains visible.

PINNED PYTHON LIBRARIES
{req}

REPRODUCIBILITY AND INTERPRETATION
Seed 42; observed URL-host grouping; approximately 60/20/20 rows in training,
validation and test. Fitted transformations use training only. The selected
20-feature Random Forest and threshold 0.5 were frozen before test scoring.
Re-running repeats that fixed experiment; it must not be used to tune from test
results. Earlier work exposed this dataset, so this is internal evaluation,
not retrospectively unseen external confirmation. Parent-domain, campaign,
template and collection dependencies may remain.

Final internal test: 47,583 observations, accuracy 99.9895%, phishing precision
99.9903%, recall 99.9854%, F1 99.9878%, 2 false alarms and 3 missed phishing rows.
These values describe this experiment only. See Sections 18-21 for limitations,
ethics, conclusion and references.
'''
    (DELIVERY/'README.txt').write_text(text,encoding='utf-8')

def build_report():
    story=[]
    def add(text,style='Body'):story.append(para(text,style))
    def heading(text):add(text,'Heading')
    def sub(text):add(text,'Subheading')
    def page():story.append(PageBreak())
    story.append(Spacer(1,45))
    add('ACADEMIC PROJECT REPORT','Subheading')
    add('Detection of Phishing Websites Using Machine Learning','Cover')
    add('From exploratory analysis to a frozen internal test','Subheading')
    story.append(Spacer(1,18))
    story.append(table(['Group member','Student ID'],MEMBERS,[320,175]))
    add('<b>Group:</b> GroupXX (number to be completed before submission).')
    add('<b>Prepared:</b> 22 November 2026. Unknown student IDs must be completed before submission.','SmallBody')
    story.append(Spacer(1,20))
    add('Abstract','Heading')
    add('This study examines recorded URL and webpage features in the PhiUSIIL dataset '
        '(235,795 observations, 56 columns). Integrity and provenance checks informed training-only '
        'exploratory analysis, explicit predictor decisions, encoding and scaling. A host-representative '
        'permutation test found different recorded URL-length distributions between classes. Logistic '
        'Regression and Random Forest were compared against a majority baseline. A controlled reduction '
        'from 48 to 20 original predictors was selected using validation and frozen before test scoring. '
        'The selected Random Forest made five errors among 47,583 internal test observations '
        '(phishing F1 99.9878%). These results are conditional on the source dataset and recorded '
        'measurements; previous dataset exposure, collection bias and residual campaign dependence '
        'limit external interpretation.')
    add('Companion evidence: GroupXX_Project.ipynb, Sections 1-21.','SmallBody')
    page();heading('1. Research question and study design')
    add('<b>Research question:</b> How effectively can recorded URL and webpage features distinguish '
        'phishing websites from legitimate websites?')
    add('<b>H0:</b> The distribution of recorded URLLength is the same in phishing and legitimate websites. '
        '<b>H1:</b> The distributions differ. This hypothesis was specified after EDA and is exploratory. '
        'It concerns the recorded field, whose complete producer formula is unverified. It is not a '
        'claim that URL length causes phishing or is sufficient as a classifier.')
    sub('Order of analysis')
    story.append(table(['Stage','Purpose and decision boundary'],[
        ['Source and integrity','Inspect schema, attribution, missingness and duplicates across source data.'],
        ['Grouped split','Lock original source-row assignments before detailed target-aware exploration.'],
        ['Training-only EDA','Inspect distributions, extremes, class associations, redundancy and provenance.'],
        ['Preprocessing and models','Fit transformations on training; compare candidates on validation.'],
        ['Controlled reduction','Select one reduced feature set using an inner training split; assess validation.'],
        ['Frozen test','Score fixed candidates, then interpret results without further selection or tuning.']],[118,377]))
    sub('Dataset, citation and units')
    add('PhiUSIIL Phishing URL (Website), Prasad and Chandra (2024), UCI dataset 967, licensed CC BY 4.0 [1]. '
        'Each row is a recorded website/URL observation with extracted measurements and a binary source '
        'label. The associated framework paper is cited for attribution [2]; inaccessible publisher '
        'text is not used as proof of feature formulas. Author examples provide partial evidence [3-5].')
    add(f'<link href="{escape(DATA_URL)}" color="{TEAL}">UCI dataset record</link> | '
        f'<link href="{escape(DOWNLOAD)}" color="{TEAL}">Direct download</link>')
    add('The submission includes the original CSV renamed dataset.csv. No source values are overwritten. '
        'SHA-256: '+SOURCE_SHA,'SmallBody')
    add('Original label: 0 phishing, 1 legitimate. Classification recodes y = 1 - label so the positive '
        'class is phishing. Raw identifiers and labels never enter the predictor matrix.')
    page();heading('2. Integrity findings and retained observations')
    story.append(table(['Check','Observed result','Action'],[
        ['Missing / blank / placeholders','0 / 0 / 0','No imputation needed for source data.'],
        ['Infinite / negative numeric values','0 / 0','No replacements justified by these checks.'],
        ['Exact duplicate rows','0','No exact-row removal required.'],
        ['Repeated URL observations','425 extra rows in 425 URL groups; 850 rows total','Retain distinct observations in the same partition.'],
        ['Conflicting labels within URLs','0','No label conflict resolved or guessed.'],
        ['Observed URL hosts','220,077','Use parsed hosts for grouped partitioning.']],[133,172,190]))
    add('Repeated URLs are not identical records: recorded features vary, and no trusted timestamp or '
        'ground-truth rule identifies a uniquely correct row. Arbitrarily retaining the first record '
        'would introduce an ordering assumption. This academic experiment retains all source observations '
        'and keeps repeated hosts together.')
    sub('Measurement consistency is distinct from missingness')
    add('Training comparisons found 112,331 discrepancies between recorded URLLength and the available '
        'URL string length; 112,329 had a difference of -1. Recorded IsHTTPS differed from a scheme-based '
        'indicator for 271 training rows, but matched the tested substring rule. These are evidence of '
        'measurement-definition uncertainty, not permission to overwrite source features. IsHTTPS does '
        'not establish certificate validity. Candidate formula agreement does not verify producer code.')
    sub('Original interpretation')
    add('A clean-looking table can still contain unclear measurements. Our decision was to preserve '
        'recorded data, document uncertainty and limit conclusions to the observed dataset. Deleting all '
        'flagged rows would conflate unusual or differently defined values with verified errors.')
    page();heading('3. Split, leakage controls and class balance')
    rows=read_csv('reports/initial_audit/split_summary.csv')
    story.append(table(['Partition','Observations','Observed hosts','Row share'],[
        [r['partition'].title(),f"{int(r['rows']):,}",f"{int(r['host_groups']):,}",f"{float(r['row_percent']):.2f}%"] for r in rows],[105,130,130,130]))
    add('Seed 42 and two GroupShuffleSplit operations allocate approximately 60/20/20 by host groups '
        '[7]. Parsed hosts are lowercased, IDNA-normalized and stripped of trailing dots. Partition '
        'assignments and source/configuration fingerprints are saved. Host and repeated-URL overlap '
        'across partitions is checked. Exact row fractions differ because groups have different sizes.')
    add('Training contains 80,787 legitimate and 60,467 phishing observations: about 57.2% versus 42.8%. '
        'This moderate imbalance motivates per-class precision, recall and F1 alongside accuracy. '
        'The majority baseline detects no phishing, despite roughly 56.8% accuracy on test. No '
        'oversampling or class weighting was added without validation evidence.')
    sub('What the split controls')
    add('Detailed distributions, target relations, hypothesis testing and feature choices use training '
        'data. Scaling and categories are fitted on training; holdouts are transformed only [8]. '
        'Feature reduction uses an additional grouped split inside training, and validation chooses '
        'the final variant. Test labels are used for the fixed final comparison, not candidate selection.')
    sub('What it cannot establish')
    add('Earlier work exposed this dataset. The current protocol cannot retroactively make the test '
        'newly unseen. Different observed hosts may share a registered domain, campaign or template. '
        'No collection-time grouping, external dataset or temporal evaluation was available. '
        'The test is internal evidence under these limitations.')
    page();heading('4. Exploratory analysis and decisions')
    add('Notebook Sections 7-11 provide more than five meaningful visualizations, with English titles, '
        'axis labels and interpretations: zero proportions, binary rates, numeric distributions, raw/log '
        'views, TLD frequencies, outlier boxplots, class ECDFs, rank effects, correlations and scatterplots.')
    story.append(image_flow('07_raw_and_log_examples.png'))
    add('Figure 1. Training distributions on raw and log-display axes. The log view exposes a long tail; '
        'it is a visualization, not an unreported model transformation.','SmallBody')
    story.append(table(['Finding','Interpretation and decision'],[
        ['50 numeric candidates; 19 binary','No constant numeric candidate. Study prevalence before treating a zero as absent information.'],
        ['10 fields at least 95% zero','Sparsity alone does not prove irrelevance; retain pending model evidence.'],
        ['9 nonbinary fields have IQR = 0','Their IQR fences are degenerate; do not use these fences to delete rows.'],
        ['73,484 rows beyond at least one nondegenerate IQR fence','About 52.02% of training; this is not an error rate. No automatic clipping/removal.'],
        ['14 candidate logical checks passed','Passing these checks does not verify every feature-extraction formula.']],[176,319]))
    page();heading('4. Exploratory analysis (continued)')
    story.append(image_flow('09_class_ecdfs.png'))
    add('Figure 2. Within-class training ECDFs; each class is normalized separately. Separation can '
        'reflect source collection and extraction differences as well as predictive signal.','SmallBody')
    add('Median recorded URLLength is 26 for legitimate and 34 for phishing training observations; '
        'median LineOfCode is 1,105 versus 12 and median NoOfExternalRef is 45 versus 0. HasSocialNet '
        'is present in approximately 79.40% versus 0.49%. These strong source-specific differences '
        'deserve provenance review. Association alone neither proves leakage nor explains causality.')
    add('The 50 numeric candidates form 1,225 pairs; seven reach absolute correlation of at least '
        '0.90 in Pearson or Spearman. Equality, formula relationships and correlation are checked '
        'separately. Correlation motivates a controlled reduction experiment; it does not identify '
        'a universal set of dispensable variables. TLD summaries describe this sample, not a '
        'trustworthiness ranking for all websites.')
    page();heading('5. Exploratory hypothesis evaluation')
    add('To reduce repeated-host weighting, select one observation per training host using seed '
        '20261121. This yields 132,045 representatives: 51,271 phishing and 80,774 legitimate. '
        'Compute the empirical two-sample KS distance and use 1,999 fixed-size label permutations. '
        'The plus-one Monte Carlo convention avoids a reported p-value of zero [14-15].')
    story.append(table(['Quantity','Result'],[
        ['KS distance D',f"{HYPOTHESIS['KS_D']:.6f}"],
        ['Monte Carlo p estimate','0.0005 (minimum reportable with 1,999 permutations)'],
        ['Threshold and decision','alpha = 0.05; reject H0 under stated assumptions'],
        ['Median recorded length','Legitimate 26; phishing 32; phishing-minus-legitimate +6'],
        ['Rank effect, phishing-minus-legitimate',f"{HYPOTHESIS['rank_effect_phishing_minus_legitimate']:.4f}"]],[235,260]))
    story.append(image_flow('15_url_length_hypothesis.png'))
    add('Figure 3. Host-representative training distributions and effect summary.','SmallBody')
    add('The direction and effect size support a descriptive distribution difference. The p estimate '
        'is exploratory after EDA and relies on exchangeability. Host representatives can remain '
        'dependent by campaign or parent domain; source URLLength definitions remain uncertain. '
        'Neither statistical significance nor this test establishes a useful standalone detector.')
    page();heading('6. Justified preprocessing')
    story.append(table(['Decision','Rationale'],[
        ['Exclude FILENAME, URL, Domain and Title','Identifier/raw text/group metadata are not directly encoded. Prevent trivial identity memorization and keep this experiment defined.'],
        ['Exclude URLSimilarityIndex, TLDLegitimateProb and URLCharProb','Reference populations and fitting time are uncertain; exclude potential reference/target leakage without claiming it is proven.'],
        ['Use 47 numeric predictors plus TLD','48 original predictors remain after excluding identifiers, target and three reference scores.'],
        ['One-hot encode TLD','Nominal categories have no numeric order. Fit training categories; ignore unseen holdout categories. 594 training categories expand the full matrix to 641 columns.'],
        ['Scale numeric fields for Logistic Regression','Train-fitted StandardScaler makes penalized linear coefficients comparable in scale.'],
        ['Pass numeric fields through for Random Forest','Tree splits do not need standardized numeric scales; TLD still uses one-hot encoding.'],
        ['No imputation, clipping or row deletion','Audits did not justify these changes. Recorded measurements remain unchanged.'],
        ['No class weighting or resampling','Moderate imbalance is measured; any intervention would need its own justified comparison.']],[185,310]))
    add('The full matrix has 641 encoded columns but only 48 original variables. The reduced model '
        'uses 20 numeric variables and no TLD, so it has 20 encoded columns. These counts must not be '
        'confused. Validation/test transformations do not learn means, scales or categories.')
    page();heading('7. Models and controlled feature reduction')
    story.append(table(['Candidate','Fixed configuration and purpose'],[
        ['Majority baseline','DummyClassifier(strategy=most_frequent). Non-informative reference; no feature learning.'],
        ['Logistic Regression','C=1, lbfgs, max_iter=2000, random_state=42; numeric scaling plus TLD encoding. Regularized linear comparator [9].'],
        ['Full Random Forest','200 trees, max_depth=20, min_samples_leaf=2, random_state=42, n_jobs=2. Default max_features=sqrt; nonlinear comparator [10].'],
        ['Reduced Random Forest','Same forest parameters; 20 selected numeric variables. One predeclared reduction candidate.']],[160,335]))
    add('Every candidate uses the same training, validation and test row assignments. Phishing is '
        'positive. Learned-model threshold is 0.5, inclusive; there is no threshold sweep, parameter '
        'search or refitting on train plus validation. These are defensible comparators, not a claim '
        'that they are the best possible classifiers.')
    sub('One reduction experiment, without test selection')
    add('Inside the original training partition, use a host-grouped split (seed 142). A fixed '
        '4,000-row inner holdout supports permutation importance (three repeats, seed 42, F1 scorer). '
        'Within inner training, a graph connects numeric pairs with absolute Spearman correlation '
        'at least 0.90; retain one ranked representative per component and fill the fixed 20-feature '
        'budget. Importance is model- and sample-dependent, especially with correlated fields [12-13].')
    add('After refitting each fixed candidate on the original training partition, the reduced forest '
        'is chosen only if validation F1 and recall are both no lower than the full forest. '
        'Full forest validation F1: 99.9573%, FN: 16, FP: 1. Reduced forest: 99.9799%, FN: 5, FP: 3. '
        'This met the pre-test selection rule. The small difference is descriptive, not a proven '
        'universal improvement. Recorded fit times were about 20 versus 8 seconds on this machine.')
    sub('The final 20 original predictors')
    add(safe(', '.join(REDUCTION['reduced_columns'])), 'SmallBody')
    page();heading('8. Frozen internal test comparison')
    add('Before scoring test labels, record the selected reduced forest, its feature list, all '
        'candidate parameters, source/split fingerprints, library versions and threshold. Check this '
        'protocol against fitted objects. Prediction does not refit models; before/after serialized '
        'model states are unchanged. All four fixed candidates are reported for transparency.')
    headers=['Model','Acc. %','Prec. %','Recall %','F1 %','FP','FN']
    rows=[]
    names={'Majority baseline':'Majority','Logistic Regression':'Logistic Reg.','Full Random Forest':'Full RF (48)','Reduced Random Forest':'Reduced RF (20)'}
    for r in METRICS:
        rows.append([names[r['Model']],*[f'{100*float(r[k]):.4f}' for k in ['Accuracy','Precision (phishing)','Recall (phishing)','F1 (phishing)']],r['False alarms (FP)'],r['Missed phishing (FN)']])
    story.append(table(headers,rows,[125,64,65,65,64,56,56]))
    add('All precision, recall and F1 values use phishing as the positive class. Test size: 47,583 '
        '(20,561 phishing, 27,022 legitimate). Undefined positive precision for the majority baseline '
        'is set to zero. FP means legitimate incorrectly flagged; FN means phishing missed.','SmallBody')
    story.append(image_flow('18_test_confusion_matrices.png'))
    add('Figure 4. Confusion matrices for every fixed candidate. Rows are true labels; columns are '
        'predictions. The selected reduced forest has TN 27,020; FP 2; FN 3; TP 20,558.','SmallBody')
    page();heading('9. Interpretation, limitations and ethics')
    sub('What the model results mean')
    add('The majority baseline shows why accuracy is insufficient: it misses all phishing. Logistic '
        'Regression is already highly effective in this source, suggesting strong separability rather '
        'than a requirement for complex models. The full forest has zero false alarms but 20 missed '
        'phishing observations. The selected reduced forest has two false alarms and three misses, '
        'a better observed recall/F1 tradeoff at the fixed threshold. Neither zero false alarms '
        'nor five total errors guarantees safety outside this experiment.')
    add('Reduced-forest validation/test F1 is 99.9799%/99.9878%. The difference is about +0.0079 '
        'percentage points, which is descriptive variation, not an independent superiority test. '
        'ROC-AUC and average precision are also reported in the notebook, but threshold-specific '
        'error counts make the remaining failures easier to understand. No post-test tuning occurred.')
    sub('Remaining limitations')
    for text in [
        'Prior dataset exposure limits claims of a genuinely untouched holdout. This is internal evaluation, not external confirmation.',
        'Observed-host grouping may leave registered-domain, campaign, template and chronological dependencies. No temporal/campaign identifiers were verified.',
        'Extraction definitions are partly unverified. Missing original HTML prevents conclusive reconstruction of recorded content features.',
        'Three uncertain reference scores were excluded, but that does not prove all collection or label proxies were removed.',
        'Class prevalence, language, geography, website type and acquisition process may differ in other populations; subgroup fairness was not established.',
        'Only fixed Logistic Regression/forest settings and one reduction candidate were compared. No uncertainty intervals or independent claim of statistical model superiority is reported.']:
        add('• '+safe(text))
    sub('Ethical considerations')
    add('Credit the dataset authors and CC BY 4.0 license. Do not treat URLs or titles as proof of '
        'wrongdoing or expose sensitive strings unnecessarily. Do not open potentially malicious '
        'addresses during analysis; this study works offline with recorded data. False positives '
        'can harm legitimate users/sites, while false negatives miss harmful examples. Explain '
        'these error types, collection bias and provenance uncertainty alongside scores; do not '
        'claim universal reliability.')
    page();heading('10. Conclusion and evaluation')
    add('Recorded URL and webpage measurements strongly distinguish source classes in this internal '
        'experiment. A transparent pipeline connects audits, training-only EDA, explicit preprocessing, '
        'an exploratory hypothesis, baseline/linear/nonlinear comparisons and a fixed test protocol. '
        'The chosen 20-feature Random Forest achieves phishing F1 99.9878%, with two false alarms '
        'and three missed phishing observations on 47,583 test rows.')
    add('The study contributes reasoned decisions rather than only scores: repeated observations '
        'are retained without inventing a correct row; long-tail values are not automatically '
        'deleted; three uncertain reference scores are excluded; transformations and feature '
        'selection are restricted to appropriate partitions. The recorded-length hypothesis '
        'supports a distribution difference under exploratory assumptions. External and temporal '
        'evaluation with verified extraction definitions would be needed before broader claims.')
    sub('Reproducing the submitted evidence')
    add('Place the submitted notebook beside dataset.csv in a writable folder. Install the pinned '
        'libraries in README.txt, select the matching Python kernel, restart and Run All. The '
        'notebook embeds the complete dictionary and frozen protocol; it creates its own audit '
        'and split outputs and does not require repository source files. Saved outputs remain '
        'visible in the submitted notebook. The source file is fingerprinted before analysis.')
    page();heading('References')
    for ref in references():add(safe(ref),'SmallBody')
    page();heading('Appendix A. Complete data dictionary')
    add('The following working meanings cover every source variable. They distinguish explicit '
        'source statements, inspected author examples and interpretations based on column names. '
        'An intuitive definition does not certify exact CSV formulas or extraction parity. '
        'Original spelling is retained. The full evidence/status table is in notebook Section 3.')
    dictionary=(ROOT/'docs/data_dictionary_en.md').read_text(encoding='utf-8')
    entries=[]
    for line in dictionary.splitlines():
        if line.startswith('| ') and not line.startswith('| Column '):
            parts=[p.strip() for p in line.strip('|').split('|')]
            entries.append([parts[0],parts[1],parts[3]])
    assert len(entries)==56
    story.append(table(['Column','Working meaning','Evidence'],entries,[162,239,94]))
    SimpleDocTemplate(str(DELIVERY/'GroupXX_Report.pdf'),pagesize=A4,rightMargin=50,leftMargin=50,
        topMargin=45,bottomMargin=55,title='Detection of Phishing Websites Using Machine Learning',
        author='Meltem Orhan; Ali Abdel Halim; Halil Trabzon').build(story,onFirstPage=page_footer,onLaterPages=page_footer)

def slide_content():
    return [
    dict(title='Detection of Phishing Websites',kicker='USING MACHINE LEARNING',speaker='Ali Abdel Halim',seconds=40,
      stats=[('235,795','recorded observations'),('20','selected predictors'),('5','internal test errors')],
      bullets=['GroupXX | Academic project', 'Meltem Orhan 221015002 | Ali Abdel Halim: ID TO BE ADDED',
               'Halil Trabzon: ID TO BE ADDED'],ref='Prasad & Chandra (2024), UCI PhiUSIIL; CC BY 4.0.',
      notes='Our project investigates whether recorded URL and webpage measurements can distinguish phishing websites from legitimate websites. We will explain the decisions behind the analysis before presenting model scores. We used the PhiUSIIL dataset and preserved its original recorded values. Meltem will discuss the data and exploratory analysis, Halil will explain preprocessing and models, and I will discuss the hypothesis, limitations and conclusion. The very high scores describe this dataset and do not establish performance on other sources.'),
    dict(title='Question and exploratory hypothesis',kicker='DEFINE THE CLAIM BEFORE INTERPRETING IT',speaker='Meltem Orhan',seconds=50,
      bullets=['RQ: How effectively do recorded URL and webpage features distinguish the classes?',
        'H0: Recorded URL-length distributions are the same in both classes.',
        'H1: The distributions differ. This is exploratory after EDA.',
        'Association is neither causation nor a complete classifier.'],
      ref='Notebook Sections 1 and 15; SciPy permutation-test documentation.',
      notes='Our research question concerns classification using recorded URL and webpage features. The hypothesis is narrower: whether recorded URL length has the same distribution in phishing and legitimate observations. We use recorded length deliberately, because the stored measurement does not always equal the current URL string length. We specified this hypothesis after exploration, so we call it exploratory. A difference between distributions would support an association in this source, but would not explain why phishing occurs or prove that length alone is sufficient for classification.'),
    dict(title='Know the source and the target',kicker='DATASET AND ATTRIBUTION',speaker='Meltem Orhan',seconds=45,
      stats=[('235,795','rows'),('56','source columns'),('220,077','observed URL hosts')],
      bullets=['PhiUSIIL | Prasad & Chandra (2024) | UCI | CC BY 4.0',
        'Source: 0 phishing / 1 legitimate. Model: positive class 1 = phishing.',
        'All 56 variables are explained; uncertain formulas are marked.'],
      ref='UCI dataset 967; notebook Sections 2, 3 and 11.',
      notes='Each row is a recorded URL or website observation with extracted measurements and a source label. We include the original dataset, renamed only, and cite its authors and license. The source uses zero for phishing and one for legitimate; we invert this for modeling so that precision, recall and F1 refer to phishing as the positive class. We also document all variables. Some meanings are supported explicitly by UCI, some have author-code examples, and others remain interpretations with unverified formulas.'),
    dict(title='Audit first, then lock the split',kicker='QUALITY AND LEAKAGE CONTROLS',speaker='Meltem Orhan',seconds=55,
      stats=[('141,254','training rows'),('46,958','validation rows'),('47,583','test rows')],
      bullets=['No missing/blank/infinite values; no exact duplicate rows.',
        '425 extra URL observations vary in features: retain within one partition.',
        'Group by observed host, seed 42; detailed EDA uses training only.'],
      ref='Notebook Sections 4-6; GroupShuffleSplit; source/split fingerprints saved.',
      notes='Source integrity checks found no missing, blank or infinite values and no exact duplicate rows. Repeated URLs are different: 425 extra observations share URL strings but contain varying recorded features. We do not have evidence identifying a uniquely correct first row, so we retain them and keep matching hosts together. We then lock a grouped training, validation and test split. The row proportions are approximately sixty, twenty and twenty percent. Detailed target-aware exploration uses training, and later transformations are fitted only on training.'),
    dict(title='EDA findings must change decisions',kicker='ORIGINAL INTERPRETATIONS',speaker='Meltem Orhan',seconds=60,
      bullets=['52.02% exceed at least one valid IQR fence: this is not an error rate.',
        'Strong webpage/class separation may reflect collection conditions.',
        'Recorded length and HTTPS definitions show discrepancies: document, do not guess.',
        'Exclude three uncertain reference scores; test feature reduction separately.'],
      ref='Notebook Sections 6.2 and 7-12; more than five explained visualizations.',
      notes='Exploration was used to decide what not to modify as well as what to change. More than half the training observations exceed at least one nondegenerate IQR fence, but multiple checks and long tails can produce many flags without proving errors. Some webpage fields separate classes very strongly, which may reflect collection conditions as well as predictive signal. Recorded length and HTTPS indicators have definition discrepancies, so we preserve them and document uncertainty. We exclude three uncertain reference scores and later test a controlled reduction rather than deleting correlated fields automatically.'),
    dict(title='The recorded-length hypothesis',kicker='EXPLORATORY TRAINING-ONLY EVIDENCE',speaker='Ali Abdel Halim',seconds=60,
      stats=[('0.3783','empirical KS distance'),('0.0005','Monte Carlo p estimate'),('+6','median difference')],
      bullets=['One random observation per training host: 132,045 representatives.',
        '1,999 permutations; p = 0.0005 is the reporting floor, not zero.',
        'Reject H0 under assumptions; campaign dependence remains possible.'],
      ref='Notebook Section 15; seed 20261121; legitimate median 26, phishing 32.',
      notes='We select one random observation per training host to reduce repeated-host weighting. This produces 132,045 representatives. Their recorded URL-length distributions differ by a KS distance of about 0.378. None of 1,999 permutations is at least as extreme, and the plus-one convention gives an estimated p-value of 0.0005, the minimum reportable at this simulation size. The median difference is six characters in the recorded field. We reject the null under our assumptions, while acknowledging that hosts can remain dependent by campaign and the hypothesis is exploratory after EDA.'),
    dict(title='Preprocessing follows the evidence',kicker='FIT ON TRAINING; TRANSFORM HOLDOUTS',speaker='Halil Trabzon',seconds=60,
      stats=[('48','original full predictors'),('641','encoded full columns'),('20','reduced numeric predictors')],
      bullets=['Exclude identifiers/raw text, target and three uncertain reference scores.',
        'One-hot encode TLD; standardize numeric values for Logistic Regression.',
        'Forest numeric values pass through; no imputation or automatic clipping.'],
      ref='Notebook Sections 13-14; scikit-learn preprocessing and leakage guidance.',
      notes='The full predictor set contains 47 numeric variables and the nominal TLD category. We exclude raw identifiers, text fields, the original target and three uncertain reference scores. The TLD has 594 training categories, so one-hot encoding expands the full matrix to 641 columns. This is different from the count of original variables. Logistic Regression also receives standardized numeric values because scale affects regularized coefficients. Tree splits do not need this numeric scaling. All fitted statistics and categories come from training; validation and test only use transform.'),
    dict(title='Compare complementary models',kicker='FIXED CONFIGURATIONS AND THRESHOLD',speaker='Halil Trabzon',seconds=50,
      bullets=['Majority baseline: exposes the limits of accuracy alone.',
        'Logistic Regression: regularized linear comparator, C = 1.',
        'Random Forest: 200 trees, depth 20, minimum leaf size 2.',
        'Same partitions; threshold 0.5; no parameter or threshold search.'],
      ref='Notebook Sections 15.4 and 16; scikit-learn model documentation.',
      notes='We compare two different model families rather than claim that these are universally best. The majority baseline predicts legitimate and measures how much accuracy can be achieved without useful detection. Logistic Regression is a regularized linear comparator. Random Forest can represent nonlinear splits and interactions. The forest uses two hundred trees, maximum depth twenty and minimum leaf size two. We keep partitions and a threshold of zero point five fixed. We do not sweep parameters or thresholds, and test performance does not select a model.'),
    dict(title='One controlled reduction experiment',kicker='VALIDATION CHOOSES; TEST DOES NOT',speaker='Halil Trabzon',seconds=55,
      stats=[('48 to 20','original predictors'),('16 to 5','validation misses'),('1 to 3','validation false alarms')],
      bullets=['Rank on an inner training host holdout; screen correlated components.',
        'Fixed budget: 20; one reduced candidate; identical forest settings.',
        'Reduced chosen only if validation F1 and recall are both no lower.'],
      ref='Notebook Section 17; permutation importance is model/sample dependent.',
      notes='Feature reduction is a separate, controlled experiment. Inside the original training partition we create another grouped split and compute permutation importance on a fixed inner holdout sample. We also screen highly correlated numeric components and use a fixed budget of twenty variables. We evaluate only one reduced candidate and keep forest settings unchanged. The selection rule requires validation F1 and recall to be no lower. The reduced candidate meets this rule: missed phishing decreases from sixteen to five, while false alarms increase from one to three. We freeze this choice before scoring test.'),
    dict(title='Frozen internal test results',kicker='PHISHING IS THE POSITIVE CLASS',speaker='Halil Trabzon',seconds=75,
      metric_table=True,bullets=['Selected RF (20): TN 27,020 | FP 2 | FN 3 | TP 20,558.',
        '47,583 test observations. No post-test tuning or refitting.'],
      ref='Notebook Section 18; exact metrics and all confusion matrices are saved.',
      notes='The majority baseline achieves about fifty-seven percent accuracy but misses all phishing, so accuracy alone is misleading. Logistic Regression is already highly effective in this source. The full forest produces zero false alarms but misses twenty phishing observations. Our preselected reduced forest makes two false alarms and three misses among 47,583 test rows, with phishing F1 about 99.9878 percent. Its confusion matrix contains 27,020 true negatives and 20,558 true positives. These counts explain the tradeoff more clearly than a rounded near-perfect score. The candidate, features and threshold were frozen before these results; we made no post-test changes.'),
    dict(title='High scores need bounded claims',kicker='LIMITATIONS AND ETHICS',speaker='Ali Abdel Halim',seconds=60,
      bullets=['Earlier dataset exposure: internal evidence, not external confirmation.',
        'Observed hosts can still share parent domains, campaigns or templates.',
        'Unverified extraction and collection bias remain; no fairness claim.',
        'Credit the source; explain both errors; do not open suspicious URLs.'],
      ref='Notebook Sections 18-20; UCI CC BY 4.0 attribution.',
      notes='The most important limitation is that this dataset was exposed during earlier work. A current split cannot retroactively create a newly unseen external test. Observed-host separation also does not guarantee independence by registered domain, campaign or template. Several extraction definitions are partly unverified, and collection conditions may explain unusually strong separation. These limitations prevent claims of universal reliability or established subgroup fairness. Ethically, we credit the source and license, avoid unnecessary disclosure of raw strings, do not visit suspicious addresses during analysis, and explain how false alarms and missed phishing can cause different harms.'),
    dict(title='Answer, evidence and next steps',kicker='CONCLUSION AND QUESTIONS',speaker='Ali Abdel Halim',seconds=40,
      bullets=['Recorded features strongly distinguish classes in this internal experiment.',
        'The selected 20-feature forest made five fixed-threshold test errors.',
        'Next evidence: verified extraction, temporal/campaign and external evaluation.',
        'Full methods, 56-variable dictionary and references are in the notebook/report.'],
      ref='Key sources: Prasad & Chandra (2024), UCI; scikit-learn; SciPy. Full references: report.',
      notes='Our answer is that recorded URL and webpage features strongly distinguish the source classes under this internal protocol. The contribution is not only a high F1 score, but a traceable sequence of audits, training-only exploration, reasoned preprocessing, a hypothesis and controlled comparisons. The selected twenty-feature forest made five test errors at the fixed threshold. Broader conclusions would require verified extraction definitions and independent temporal or external evidence. The notebook and report contain the complete data dictionary, detailed results and references. Thank you; we are ready to discuss our choices and limitations.')
    ]

class SlideWriter:
    """Write the same layout to editable PowerPoint and a matching PDF."""
    def __init__(self,prs,pdf,index,total):
        self.slide=prs.slides.add_slide(prs.slide_layouts[6]);self.pdf=pdf
        self.index=index;self.total=total;self.background()
    def rect(self,x,y,w,h,color):
        shape=self.slide.shapes.add_shape(MSO_SHAPE.RECTANGLE,Inches(x/72),Inches(y/72),Inches(w/72),Inches(h/72))
        shape.fill.solid();shape.fill.fore_color.rgb=RGBColor.from_string(color.lstrip('#'));shape.line.fill.background()
        self.pdf.setFillColor(colors.HexColor(color));self.pdf.rect(x,540-y-h,w,h,fill=1,stroke=0)
    def background(self):
        self.rect(0,0,960,540,'#FFFFFF');self.rect(0,0,12,540,TEAL)
        self.rect(56,494,848,1,'#D7E2EB')
    def text(self,text,x,y,w,h,size=21,color=INK,bold=False):
        font='ArialBold' if bold else 'Arial'
        lines=[]
        for paragraph in text.split('\n'):
            current=''
            for word in paragraph.split():
                test=(current+' '+word).strip()
                if current and pdfmetrics.stringWidth(test,font,size)>w:
                    lines.append(current);current=word
                else:current=test
            lines.append(current)
        leading=size*1.23
        assert len(lines)*leading<=h+3,(self.index,text,lines,h)
        box=self.slide.shapes.add_textbox(Inches(x/72),Inches(y/72),Inches(w/72),Inches(h/72))
        frame=box.text_frame;frame.clear();frame.margin_left=frame.margin_right=frame.margin_top=frame.margin_bottom=0
        frame.word_wrap=False
        for i,line in enumerate(lines):
            p=frame.paragraphs[0] if i==0 else frame.add_paragraph()
            p.text=line;p.font.name='Arial';p.font.size=Pt(size);p.font.bold=bold
            p.font.color.rgb=RGBColor.from_string(color.lstrip('#'));p.space_before=Pt(0);p.space_after=Pt(0);p.line_spacing=Pt(leading)
            self.pdf.setFont(font,size);self.pdf.setFillColor(colors.HexColor(color))
            self.pdf.drawString(x,540-y-size-i*leading,line)
    def header(self,item):
        self.text(item['kicker'],56,27,820,18,10,TEAL,True)
        self.text(item['title'],56,58,848,64,30,NAVY,True)
        self.text(item['ref'],56,506,785,24,7.7,GRAY)
        self.text(f'{self.index:02d} / {self.total:02d}',855,507,80,15,9,GRAY)
    def cards(self,stats):
        for i,(number,label) in enumerate(stats):
            x=56+i*286
            self.rect(x,143,270,102,PALE)
            self.text(number,x+16,155,242,48,31,TEAL,True)
            self.text(label,x+16,207,242,28,12,GRAY)
    def bullets(self,bullets,y=145,small=False):
        size=17 if small else 20
        gap=57 if len(bullets)<=4 else 49
        if y>=265:gap=59;size=17.5
        for i,text in enumerate(bullets):
            yy=y+i*gap
            self.rect(57,yy+8,5,5,TEAL)
            self.text(text,75,yy,815,gap-5,size,INK)
    def metrics(self):
        widths=[220,120,120,120,120,74,74]
        headers=['Model','Acc. %','Prec. %','Recall %','F1 %','FP','FN']
        y=145
        self.rect(56,y,848,36,NAVY)
        x=56
        for name,width in zip(headers,widths):self.text(name,x+8,y+8,width-12,22,12,'#FFFFFF',True);x+=width
        names=['Majority','Logistic Reg.','Full RF (48)','Reduced RF (20)']
        for row,(r,name) in enumerate(zip(METRICS,names)):
            yy=y+36+row*39
            self.rect(56,yy,848,39,PALE if row==3 else '#F2F5F8' if row%2==0 else '#FFFFFF')
            values=[name,*[f'{100*float(r[k]):.4f}' for k in ['Accuracy','Precision (phishing)','Recall (phishing)','F1 (phishing)']],r['False alarms (FP)'],r['Missed phishing (FN)']]
            x=56
            for v,width in zip(values,widths):self.text(v,x+8,yy+11,width-12,22,13,TEAL if row==3 else INK,row==3);x+=width

def build_presentation():
    items=slide_content();prs=Presentation();prs.slide_width=Inches(960/72);prs.slide_height=Inches(540/72)
    prs.core_properties.title='Detection of Phishing Websites Using Machine Learning'
    prs.core_properties.author='Meltem Orhan; Ali Abdel Halim; Halil Trabzon'
    pdf=canvas.Canvas(str(PRESENTATION/'GroupXX_Presentation.pdf'),pagesize=(960,540))
    pdf.setTitle(prs.core_properties.title);pdf.setAuthor(prs.core_properties.author)
    for i,item in enumerate(items,1):
        writer=SlideWriter(prs,pdf,i,len(items));writer.header(item)
        if item.get('metric_table'):
            writer.metrics();writer.bullets(item['bullets'],365,True)
        elif item.get('stats'):
            writer.cards(item['stats']);writer.bullets(item['bullets'],270,True)
        else:writer.bullets(item['bullets'])
        writer.slide.notes_slide.notes_text_frame.text=(f"Speaker: {item['speaker']}\nTarget: {item['seconds']} seconds\n\n{item['notes']}\n\n{item['ref']}")
        pdf.showPage()
    pdf.save();prs.save(str(PRESENTATION/'GroupXX_Presentation.pptx'))
    story=[para('Presentation guide and questions','Cover'),para('GroupXX | English presentation | Target: 10 minutes 50 seconds')]
    totals={name:sum(x['seconds'] for x in items if x['speaker']==name) for name,_ in MEMBERS}
    story.append(table(['Member','Assigned slides','Target time'],[[name,', '.join(str(i) for i,x in enumerate(items,1) if x['speaker']==name),f'{t//60}:{t%60:02d}'] for name,t in totals.items()],[160,210,125]))
    story.append(para('All members should understand the complete experiment. These assignments ensure everyone speaks; rehearse transitions together. Group number and two IDs remain to be completed.'))
    for i,item in enumerate(items,1):
        story.append(para(f"{i}. {item['title']}",'Heading'))
        story.append(para(f"{item['speaker']} | {item['seconds']} seconds",'Subheading'))
        story.append(para(safe(item['notes'])))
    story.append(PageBreak());story.append(para('Prepare for questions','Heading'))
    questions=[
        ('Why not remove every repeated URL?','They are distinct observations with varying features, not exact duplicate rows. No trusted rule identifies a uniquely correct observation. We retain them and group matching hosts.'),
        ('Why were missing values not filled?','No missing, blank or placeholder values were observed. Imputation without missingness would not solve measurement uncertainty.'),
        ('Why not remove all IQR outliers?','Extremes and sparse counts are not verified errors. Many separate fences flag valid long-tail records, and nine fields have degenerate zero IQR.'),
        ('What is the target direction?','Source label 0 is phishing and 1 legitimate. Modeling uses y=1-label, so positive precision, recall and F1 mean phishing.'),
        ('Why is a grouped split preferable here?','The same host or repeated URL should not appear in multiple partitions. However, campaigns and parent domains can still cross observed hosts.'),
        ('Is this an untouched external test?','No. Earlier work exposed the dataset. This is a frozen internal comparison, with explicit limitations and no post-test tuning.'),
        ('Why exclude the three reference scores?','Their reference populations and fitting times are uncertain. We exclude them as a precaution without claiming leakage was proven.'),
        ('Why use both Logistic Regression and Random Forest?','They provide regularized linear and nonlinear tree comparisons. The majority predictor supplies a separate baseline.'),
        ('Why scale only the linear numeric inputs?','Scale affects regularized linear coefficients. Tree split thresholds do not require standardization; the forest still needs categorical encoding in the full model.'),
        ('How were 20 features chosen?','One inner training host split supports permutation importance and a correlation-component screen. A fixed budget and one candidate are evaluated; validation decides using a pre-test F1/recall rule.'),
        ('Does p=0.0005 mean a 0.05% chance H0 is true?','No. It is a Monte Carlo tail estimate under the permutation null and exchangeability assumptions. It is also the reporting floor for 1,999 permutations.'),
        ('Why are representative medians 26/32 but all-training medians 26/34?','The hypothesis gives one row per host; descriptive EDA uses all training observations. They are different analysis samples with different weighting.'),
        ('Why are 48 predictors expanded to 641 columns?','There are 47 numeric fields plus 594 training TLD categories after one-hot encoding. The reduced set has 20 numeric fields and excludes TLD.'),
        ('What do five errors mean?','On 47,583 internal test rows, the selected forest has two legitimate rows incorrectly flagged and three phishing rows missed. These are sample counts, not guarantees for other data.'),
        ('What evidence would strengthen the study?','Verified feature extraction, campaign/registered-domain and temporal controls, independent source data and an appropriately designed uncertainty analysis.')]
    for question,answer in questions:story.extend([para(safe(question),'Subheading'),para(safe(answer))])
    SimpleDocTemplate(str(PRESENTATION/'GroupXX_SpeakerNotes.pdf'),pagesize=A4,leftMargin=50,rightMargin=50,topMargin=45,bottomMargin=55).build(story,onFirstPage=page_footer,onLaterPages=page_footer)
    (PRESENTATION/'README.txt').write_text('ENGLISH CLASSROOM PRESENTATION\n\nGroupXX_Presentation.pptx: editable 12-slide PowerPoint with speaker notes.\nGroupXX_Presentation.pdf: matching portable slide view.\nGroupXX_SpeakerNotes.pdf: timed script, member assignments and questions.\n\nTarget duration: 10 minutes 50 seconds. All three members have speaking parts.\nReplace GroupXX and add the two unknown student IDs before submission.\nThe notebook/report/dataset/README submission folder is separate; no ZIP was created.\n',encoding='utf-8')

if __name__=='__main__':
    assert hashlib.sha256((DELIVERY/'dataset.csv').read_bytes()).hexdigest()==SOURCE_SHA
    build_readme();build_report();build_presentation()
    print('Built English report, README, 12-slide PPTX/PDF and timed speaker notes.')
