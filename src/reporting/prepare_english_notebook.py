"""Prepare the English, self-contained academic notebook without changing results."""
from pathlib import Path
import hashlib,json,re,shutil
import nbformat as nbf

ROOT=Path(__file__).resolve().parents[2]
DELIVERY=ROOT/'submission/GroupXX_PhishingDetection'
DELIVERY.mkdir(parents=True,exist_ok=True)
PROJECT='GroupXX_Project'
MEMBERS=[('Meltem Orhan','221015002'),('Ali Abdel Halim','TO BE ADDED'),('Halil Trabzon','TO BE ADDED')]

def build():
    nb=nbf.read(ROOT/'notebooks/01_eda.ipynb',as_version=4)
    descriptions=[
      'Source file identifier; UCI states it may be ignored.',
      'Recorded website address; raw input for identity and parsing audits.',
      'Recorded URL length; exact representation counted is not fully verified.',
      'Recorded domain/netloc text; may include port or user information.',
      'Recorded domain length.', 'Indicator interpreted as IP-address domain usage.',
      'Recorded top-level domain category.',
      'Reference-based URL similarity score; reference population and formula need verification.',
      'Character-continuation statistic; author example code is available, CSV parity unverified.',
      'TLD legitimacy probability; reference population and estimation process unverified.',
      'URL character probability score; reference distribution and formula unverified.',
      'Recorded TLD length.', 'Recorded subdomain count; suffix/www rules unverified.',
      'Obfuscation indicator; detection rules unverified.',
      'Count of characters identified as obfuscated; detection rules unverified.',
      'Obfuscated-character ratio; denominator/rounding unverified.',
      'Recorded letter count in URL; character scope unverified.',
      'Recorded letter ratio; denominator/rounding unverified.',
      'Recorded digit count; original misspelling retained.',
      'Recorded digit ratio; denominator/rounding unverified; original spelling retained.',
      'Recorded equals-sign count.', 'Recorded question-mark count.', 'Recorded ampersand count.',
      'Recorded other-special-character count; character set unverified.',
      'Recorded special-character ratio; character set and denominator unverified.',
      'Recorded HTTPS indicator; not certificate validation; scheme mismatches audited.',
      'Recorded source-code line count.', 'Recorded maximum source-code line length.',
      'Page-title presence indicator.', 'Recorded raw page title text.',
      'Domain/title matching score; author example inspected, CSV parity unverified.',
      'URL/title matching score; author example inspected, CSV parity unverified.',
      'Favicon presence indicator.',
      'Robots-related indicator; robots.txt versus metadata rule unverified.',
      'Responsive-page indicator; detection rule unverified.',
      'Recorded URL redirects; only 0/1 observed, original counting rule unverified.',
      'Recorded self-redirects; self-redirect definition unverified.',
      'Page-description presence indicator.', 'Recorded popup count; detection method unverified.',
      'Recorded iframe count.', 'External form-submit indicator; external-target rule unverified.',
      'Social-network signal indicator; scope unverified.', 'Submit-button presence indicator.',
      'Hidden-form-field presence indicator.', 'Password-field presence indicator.',
      'Bank-related keyword indicator; vocabulary and searched text unverified.',
      'Payment-related keyword indicator; matching rule unverified.',
      'Cryptocurrency-related keyword indicator; matching rule unverified.',
      'Copyright-information presence indicator.', 'Recorded image count; element scope unverified.',
      'Recorded CSS resource count; inline/external scope unverified.',
      'Recorded JavaScript resource count; inline/external scope unverified.',
      'Recorded same-site reference count; site boundary rule unverified.',
      'Recorded empty-reference count; empty/# handling unverified.',
      'Recorded external-reference count; external-target rule unverified.',
      'Original target: 0 phishing, 1 legitimate; confirmed by UCI.'
    ]
    # Use the source schema order, not a hand-sorted dictionary.
    import csv
    with (ROOT/'data/raw/PhiUSIIL_Phishing_URL_Dataset.csv').open(encoding='utf-8-sig',newline='') as f: columns=next(csv.reader(f))
    assert len(columns)==len(descriptions)==56
    dictionary=['| Column | Working meaning | Group / role | Evidence status | Source |','|---|---|---|---|---|']
    for c,meaning in zip(columns,descriptions):
        status='UCI explicit' if c in ['FILENAME','label'] else 'Author code found' if c in ['CharContinuationRate','DomainTitleMatchScore','URLTitleMatchScore'] else 'Name-based interpretation'
        group='Target' if c=='label' else 'Identifier / raw text / grouping' if c in ['FILENAME','URL','Domain','Title'] else 'Categorical predictor' if c=='TLD' else 'Recorded numeric feature'
        source='UCI' if status=='UCI explicit' else 'Author example' if status=='Author code found' else 'Column-name interpretation'
        dictionary.append(f'| {c} | {meaning} | {group} | {status} | {source} |')
    dictionary_table='\n'.join(dictionary)
    dictionary_md='# Data dictionary\n\n'+dictionary_table
    (ROOT/'docs/data_dictionary_en.md').write_text(dictionary_md,encoding='utf-8')

    translations={
    0:'''# Detection of Phishing Websites Using Machine Learning

**Group:** GroupXX (number to be completed before submission)

| Group member | Student ID |
|---|---|
| Meltem Orhan | 221015002 |
| Ali Abdel Halim | TO BE ADDED |
| Halil Trabzon | TO BE ADDED |

This academic study connects source attribution, quality audits, exploratory analysis,
justified preprocessing, an exploratory hypothesis, classifier comparison, a limited
feature-reduction experiment and frozen internal test evaluation. Raw data remain unchanged.
All computational outputs are saved. Run the cells in order using the versions in README.txt.

**Important limitation:** Earlier experiments exposed this dataset. The current split
organizes this study but is not retrospectively unseen external confirmation. Observed-host
separation does not establish registered-domain, campaign, template or temporal independence.
''',
    1:'''## 1. Research question and exploratory hypothesis

**Research question:** How effectively can recorded URL and webpage features distinguish
phishing websites from legitimate websites?

**H0:** The distribution of recorded URL length is the same for phishing and legitimate websites.

**H1:** The distribution of recorded URL length differs between phishing and legitimate websites.

The source variable is recorded `URLLength`, and source labels are 0 phishing and 1 legitimate.
The hypothesis was specified after EDA and is explicitly exploratory. Its evaluation in
Section 15 uses training-host representatives and reports the exchangeability/dependence limits.
The original length-extraction discrepancy remains relevant; results concern recorded values.
A distribution difference does not establish causality or prove that length alone is sufficient.

At least two learned classifiers are compared using phishing precision, recall, F1, accuracy
and confusion counts. Preprocessing and model fitting use training data; selection uses
validation; final test scoring follows the frozen protocol. Positive modelling target is phishing=1.
''',
    2:'''## 2. Data source and reproducibility

[PhiUSIIL, UCI](https://archive.ics.uci.edu/dataset/967/phiusiil%2Bphishing%2Burl%2Bdataset),
Arvind Prasad and Shalini Chandra (2024), CC BY 4.0. The supplied CSV contains
235,795 observations and 56 columns, including identifier and target fields.
Features originate from URLs and recorded page content. Exact formulas, record-level
timestamps and campaign membership are not fully established here.

**Check:** Record the input SHA-256 and runtime versions. Analysis does not fetch websites.
The submission reads the unchanged source as `dataset.csv` beside this notebook.
All report and split folders are generated by running the cells; no repository files are needed.
''',
    4:'''## 3. Dataset structure

**Question:** What does a row represent, and which fields are available?
A row is a recorded URL/page observation; a URL may occur more than once.
Types, missing counts and distinct-value counts form a measured inventory, not verification
of all extraction formulas. Raw addresses and page titles are not rendered as links.
The complete dictionary below is embedded in the notebook for independent execution.
''',
    6:'''<a id="data-dictionary"></a>
### 3.1. Variable meanings and evidence status

**UCI explicit:** meaning directly documented by UCI. **Author code found:** example inspected,
but exact local CSV parity unverified. **Name-based interpretation:** a working meaning,
not a verified extraction formula. Original column misspellings are preserved.

Sources: [UCI](https://archive.ics.uci.edu/dataset/967/phiusiil%2Bphishing%2Burl%2Bdataset),
[character statistic](https://github.com/arvindbitm/PhiUSIIL/blob/main/CharConRate.ipynb),
[title scores](https://github.com/arvindbitm/PhiUSIIL/blob/main/WebPageTitleMatchScore.ipynb).

'''+dictionary_table+'''

The author's character-statistic example preprocesses domain text, so applying it to a
complete URL is not automatically equivalent. Title-score preprocessing and error cases
also require care. No unverified formula is presented as confirmed.
''',
    7:'''## 4. Quality and integrity

**Question:** Are there missing/blank values, placeholders, nonfinite numbers or basic URL
parsing problems? Placeholders are review flags, not automatically recoded missing data.
URL checks inspect scheme/host/port structure; they do not verify a site's existence or safety.
Negative numbers are flagged for interpretation rather than automatically removed.
No global imputation, clipping or row deletion is performed.
''',
    9:'''## 5. Repeated URLs and conflicting observations

**Question:** Are rows identical, or are there different recorded measurements for one URL?
Full-row duplicates, identical content excluding filename, repeated exact URLs and conflicting
labels are counted separately. There are 425 additional URL observations across 850 rows;
all repeated URL groups vary in recorded features, with no conflicting labels.

Selecting the first record would not establish that it is more correct. Deleting all repeated
groups would discard 850 observations. In this recorded-feature experiment, observations
are retained within the same host partition. Their possible weighting effect is a limitation.
Source data are unchanged. Training-only paired examples are displayed after splitting in 6.1.
''',
    11:'''## 6. Class balance and observed-host-grouped partitioning

The overall class balance describes source coverage. The split does not search seeds for
desirable label proportions. Hostnames parsed from URLs are IDNA-normalized, lowercased
and stripped of a trailing dot. Exact URL repetition therefore cannot cross host groups.

GroupShuffleSplit assigns approximately 60/20/20 of observed-host groups using fixed seeds
42/43. Row percentages may differ from group percentages. Overlap checks cover rows,
exact URLs and observed hostnames. Original recorded Domain mismatches are audited separately.
No temporal split is claimed without verified timestamps. Different subdomains or campaigns
may still cross the partitions; registered-domain independence is not established.
''',
    13:'''### 6.1. Inspect repeated URL observations side by side

This continues Section 5 using training rows only. `N_GROUPS` controls the displayed groups,
and `GROUP_OFFSET` selects later groups. `SHOW_URLS` is false by default to avoid exposing
raw query values. Each comparison identifies source rows and displays only fields that vary.
The policy-count table illustrates possible deletions; none is applied in this experiment.
''',
    15:'''### 6.2. Consistency between recorded features and URL text

Training-only candidate calculations compare recorded lengths, Domain, HTTPS and character
counts with explicit parsing/counting rules. Scheme removal, www, trailing slash, decoding
and IDNA conventions can change measurements. Highest agreement among tested candidates
does not verify the original producer formula. No value is silently corrected.
Tables show mismatch rates, length-difference frequencies and domain mismatch categories.
Raw URL text remains hidden unless `SHOW_URL_TEXT` is enabled for local inspection.
''',
    17:'''## 7. Univariate distributions: training data only

Describe ranges, concentration, sparsity and variability before making treatment decisions.
The target is excluded from predictor summaries. Identifiers and raw text are handled separately.
No feature selection, clipping or fitted transformation is performed here.
Sequence: numeric inventory, zeros/constants, binary fields, distributions, categories and findings.
''',
    19:'''### 7.1. Constants and zero concentration

Identify constant numeric fields and high zero proportions. A zero may mean true absence or
an extraction convention; its meaning requires the dictionary. Rarity alone does not justify
removal. No numeric field is constant in training, although several have very high zero rates.
''',
    21:'''### 7.2. Binary indicators

Within-training proportions of zero/one describe prevalence, not predictive usefulness.
Fields named as counts, notably NoOfURLRedirect and NoOfSelfRedirect, contain only 0/1;
this warrants checking the original extraction rule rather than silently renaming them.
''',
    23:'''### 7.3. Numeric distribution plots

Every nonbinary, nonconstant numeric field is plotted. Three examples compare raw and log1p
views. Further panels use log1p for nonnegative values to reveal long tails, without changing
the training table or dropping tail observations. Histograms use 40 bins.
''',
    25:'''### 7.4. Categorical frequencies and text structure

Distinct-value and repetition rates describe identifier/text fields separately from numeric
predictors. TLD frequencies show the 15 most common categories and their combined remainder.
URL, Domain and Title string lengths are descriptive; they need not equal supplied feature
definitions. Raw addresses/titles are not published. Category variety alone does not establish utility.
''',
    27:'''### 7.5. Measured summary and decision inputs

The following summary is computed from the training results. High zero rates or skewness
are review evidence rather than deletion rules. Extreme records and logical checks follow in
Section 8; final feature/model choices appear in later sections.
''',
    29:'''### 7.6. Interpretation of univariate findings

- The 50 numeric predictor candidates include 19 binary fields and 31 other numeric fields;
  none is constant. This does not establish independence or predictive usefulness.
- Ten fields are at least 95% zero. HasObfuscation is positive in 321 training records
  (0.227%); IsDomainIP in 353 (0.250%). Rare does not mean invalid or irrelevant.
- Long right tails are substantial: URLLength median 27 versus maximum 5,794;
  LineOfCode median 429 versus maximum 442,666; LargestLineLength median 1,067
  versus maximum 13,975,732. A large value is not automatically an error.
- Log1p plots improve visibility without altering the data. The recorded-length caveat remains.
- HasTitle is 1 in 86.303%, recorded IsHTTPS in 78.128%, and IsResponsive in 62.071%
  of training records. These are overall rates, not class-separation evidence.
- There are 594 training TLD categories. com accounts for 47.662%; the first 15 categories
  cover 77.790%. Rare categories and sample-source concentration require care.
- No field was removed, clipped or transformed based solely on these observations.
''',
    30:'''## 8. Outliers: training data only

For nonbinary/nonconstant fields, compute Q1, Q3 and IQR, then flag values outside
[Q1-1.5 IQR, Q3+1.5 IQR] for review only. Values above the 99th percentile are also counted.
These statistical fences are not validated physical boundaries or automatic deletion rules.
When IQR is zero, a fence collapses and may flag every nonzero count; those cases are
reported separately. No validation/test data or target-dependent rule is used here.
''',
    32:'''### 8.1. Inspect extreme records in context

For eight selected URL/content fields, display the five largest records with source-row
identifiers and contextual measurements. Different units need not agree numerically.
Without archived HTML, an extreme source-code length cannot be confirmed from this table.
Raw addresses are hidden unless `SHOW_OUTLIER_TEXT` is enabled. No address is visited.
''',
    34:'''### 8.2. Candidate logical checks

Check positive lengths, plausible 0-1 ranges and consistency of obfuscation indicators,
counts and ratios. Several rules rely on name-based meanings rather than fully verified
producer definitions. A flag therefore triggers review rather than automatic correction;
zero flags only show that these particular checks passed.
''',
    36:'''### 8.3. Outlier summary

Statistical extremeness, a logical contradiction and an unreproduced source feature are
different issues. They cannot all be solved by a generic outlier-removal operation.
''',
    38:'''### 8.4. Interpretation of outlier findings

Among 31 nonbinary fields, nine have zero IQR. For the remaining fields, 73,484 training
records (52.02%) fall outside at least one fence. That is not an error rate: long tails and
multiple simultaneous checks naturally flag many records. Blanket deletion would remove
over half the training set without verified justification.

Zero-IQR fields include subdomain/digit/obfuscation counts or ratios and several sparse
character/popup counts; zero IQR does not mean a constant column. The 14 candidate logical
checks found no violations, but this does not verify all extraction formulas. Large HTML
measurements might reflect minified content, but without original HTML that remains a
possible explanation rather than a confirmed fact. No clipping or row deletion is applied.
''',
    39:'''## 9. Relationships with the target: training data only

Compare within-class binary rates, numeric percentiles, signed rank effects and TLD
frequencies. Source label 0 denotes phishing; local phishing_target=1 is used for the
comparisons without changing the original table. No raw text/identifier is treated as an
ordinary numeric predictor. These are descriptive relationships, not causal or test-performance claims.
Dependent host observations and large sample size make naive significance claims inappropriate.
''',
    41:'''### 9.1. Binary class rates

Normalize each class separately. Gap = phishing one-rate minus legitimate one-rate,
in percentage points. Positive gaps indicate more frequent positive flags in phishing.
A sensitivity comparison weights each observed hostname to total weight 1. This changes
the descriptive weighting; it does not ensure registered-domain/campaign independence.
''',
    43:'''### 9.2. Numeric percentiles and rank effects

For each nonbinary field report within-class quartiles, median, p95 and zero rate.
Signed rank effect = 2 U / (n_phishing n_legitimate) - 1, with phishing as the first sample
and ties contributing half. Positive values favor larger phishing values, negative values
favor larger legitimate values. Near zero does not prove identical distributions.
The host-weighted version uses 2 weighted AUC - 1. No independent-sample p-value is
reported here and no feature is selected from this ranking alone.
[U statistic](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.mannwhitneyu.html),
[weighted AUC](https://scikit-learn.org/stable/modules/generated/sklearn.metrics.roc_auc_score.html).
''',
    45:'''### 9.3. Within-class empirical cumulative distributions

Six predefined features are shown as ECDFs. At a given x, y is the within-class fraction
at or below x. The first four fields use log1p display only; the table is unchanged.
Including a reference score here does not verify its provenance or select it for modelling.
''',
    47:'''### 9.4. TLD sample proportions

Show counts, within-class category shares and the phishing fraction within each recorded
TLD sample. These are not internet-wide risk probabilities. The 15 most common training
categories are displayed; no target encoding or rare-category regrouping is applied here.
''',
    49:'''### 9.5. Interpretation of class relationships

- Training contains 80,787 legitimate and 60,467 phishing observations. Within-class rates
  avoid confusing unequal sample sizes with feature differences.
- HasSocialNet is positive in 79.40% of legitimate versus 0.49% of phishing records;
  HasCopyrightInfo in 80.85% versus 5.27%; HasDescription in 73.76% versus 4.23%.
  These large gaps can reflect content and collection conditions, not universal safety rules.
- LineOfCode medians are 1,105 versus 12, and external-reference medians 45 versus 0.
  Failed retrieval/extraction policies and source selection need investigation.
- Recorded URLLength medians are 26 versus 34, with p95 35 versus 97. A long URL alone
  is not a phishing diagnosis; recorded-length uncertainty remains.
- URLSimilarityIndex medians are 100 versus 51.63 and signed rank effect about -0.992.
  Reference population, label use and computation time require verification before modelling.
- Recorded IsHTTPS is 1 in 100% of legitimate versus 48.91% of phishing records;
  previously observed definition discrepancies prevent treating it as validated transport security.
- Host weighting changes some effects (URLLength by about 0.065), without ruling out
  campaign or collection bias. TLD sample fractions are not general risk estimates.
''',
    50:'''## 10. Relationships among predictors: training data only

Pearson describes linear association and sensitivity to extreme values; Spearman describes
rank association. For binary fields Pearson corresponds to phi. Neither establishes causality
or interchangeability. Target and raw identifiers/text are excluded. Exact equality,
complements, derived-rule candidates and within-class relationships are checked separately.
''',
    52:'''### 10.1. Correlation heatmaps

Both matrices use identical feature order and a fixed -1 to +1 color scale. The diagonal
is self-correlation and is excluded from pair counts. CSVs and pair tables support precise
reading. Absolute correlation 0.90 is a reporting flag, not an automatic deletion rule.
''',
    54:'''### 10.2. Exact equality, complements and candidate formulas

High correlation does not imply equal values. Search exact equality in training and
complements among binary columns. Check obfuscation indicators against positive counts/ratios.
For ratio candidates compare recorded URLLength and actual string length denominators using
absolute tolerance 1e-6 and zero relative tolerance. Rounding may explain disagreement.
Shared zeros can inflate apparent agreement, so positive-count records are also examined.
''',
    56:'''### 10.3. Do relationships persist within classes?

Two features may correlate in the pooled sample because both differ between classes.
For the 15 largest absolute Spearman pairs, report within-class correlations as well.
Undefined correlation for a within-class constant stays NaN, not zero. Scatterplots use
a fixed random sample of at most 20,000 training rows for display only; correlation
calculations use the full relevant training sample.
''',
    58:'''### 10.4. Interpretation of predictor relationships

The 50 numeric candidates form 1,225 unique pairs; seven have absolute Pearson or
Spearman at least 0.90. No exact equal/complement pair exists across all training rows.
Obfuscation count/ratio Spearman is nearly 1 while Pearson is about 0.342; shared zeros
strongly influence the rank association and do not prove equal information among positives.

URLLength/letter count Pearson is 0.954 and Spearman 0.972; within-class rank relationships
also persist. Title-score Pearson is 0.960 and Spearman 0.964, but their class-specific
structure differs. CSS/JS pooled Spearman is 0.884 versus about 0.656 and 0.620 within classes.

The obfuscation-count/recorded-length ratio candidate matches about 99.782% overall but only
4.050% of positive-count records: common zeros conceal formula uncertainty. No source ratio
is replaced with an assumed formula. Relationship groups guide later inspection, not automatic removal.
''',
    59:'''## 11. Feature provenance, leakage and potential bias

**Question:** What do recorded fields measure, how were they obtained, and could reference
or target information affect them? Direct target copies, reference fitting, related sites
crossing partitions and collection bias are distinct risks. Strong class association is not
proof of leakage. Checks use training data; modelling decisions follow in later sections.
''',
    60:'''### 11.1. Source evidence and measurement basis

The UCI record establishes source/label information; the author's repository provides partial
character-statistic and title-score examples. Examples do not verify exact parity for every
CSV value. The following inventory classifies measurement basis and evidence status rather
than claiming a complete reconstruction of producer algorithms. Reference populations,
suffix policies, keyword scope and collection conditions remain relevant uncertainties.

[UCI](https://archive.ics.uci.edu/dataset/967/phiusiil%2Bphishing%2Burl%2Bdataset),
[author repository](https://github.com/arvindbitm/PhiUSIIL),
[leakage guidance](https://scikit-learn.org/stable/common_pitfalls.html).
''',
    62:'''### 11.2. Direct target-copy checks and HTTPS meaning

Search numeric fields that exactly equal the source target or its inverse. Passing this check
does not exclude indirect leakage. Compare the recorded HTTPS indicator with parsed scheme
and with substring search anywhere in the URL. A query may itself contain another HTTPS
address, so these definitions differ. Neither validates a TLS certificate or site safety.
''',
    66:'''### 11.4. Interpretation of provenance findings

All 56 fields are inventoried, with unequal evidence levels. No numeric field directly copies
the target, but indirect label/reference/source effects remain possible. Three reference scores
have unresolved populations/timing and are treated cautiously in the primary experiment.
Recorded IsHTTPS differs from parsed scheme in 271 training rows but matches an anywhere-https
substring flag; this is a behavioral clue rather than proof of producer code. Observed-host
grouping does not establish registered-domain/campaign/template/temporal independence.
These limitations are carried into predictor selection and final interpretation.
''',
    67:'''## 12. From EDA evidence to the academic experiment

The source observations are retained; no blanket duplicate/outlier deletion is justified.
Missing-value filling is unnecessary for this input. Identifiers and target are separated;
uncertain reference scores are excluded from the primary predictor schema. Recorded
measurement caveats remain explicit rather than silently changing definitions.

The following executed sections implement the academic workflow: 13 defines X/y and partitions,
14 fits preprocessing on training data, 15 evaluates the exploratory hypothesis, 16 compares
classifiers on validation, 17 tests one reduced feature set, and 18 scores the frozen internal
test protocol. Sections 19–21 provide conclusion, ethics and consolidated references.
''',
    68:'''## 13. Justified preprocessing: predictor and target definition

### 13.1. Column decisions

The academic predictor table uses recorded features without changing the source.
FILENAME, URL and Domain remain audit/group metadata; raw Title is excluded from the first
experiment because text processing requires a separate design. URLSimilarityIndex,
TLDLegitimateProb and URLCharProb are excluded due to unresolved reference provenance,
not proven leakage. The initial X contains 47 numeric fields and categorical TLD.
Target is is_phishing=1-label and is never included in X.

Different recorded observations for an exact URL remain in the same partition; no arbitrary
representative is chosen for page measurements. Recorded length/ratio/HTTPS fields are not
silently replaced. No encoding, scaling or classifier fitting occurs in this section.
''',
    70:'''### 13.2. Separate X, y and metadata without changing partitions

X contains the explicit predictors and y the phishing-positive target. source_row is an index,
not a model feature. Recorded addresses remain metadata, not published example links.
Deterministic selection/target recoding does not learn from holdout feature distributions.
Each partition is kept separately for later training-fitted transformations.
''',
    72:'''### 13.3. Validation checks and remaining preprocessing

Check row/target alignment, recoding, finite numeric cells, nonmissing categories and absence
of row/URL/host overlap. Unexpected missing values stop the run rather than trigger global
imputation. This defines raw X/y; encoding/scaling follows in Section 14. Outliers and sparse
or correlated fields are not automatically removed. No model is fitted here.
''',
    74:'''## 14. Training-fitted encoding and scaling

### 14.1. Preprocessing decisions

TLD is nominal, so arbitrary numeric ordering is avoided. One-hot categories are learned
only from X_train. Unknown categories use an all-zero TLD block with handle_unknown='ignore';
this limitation is reported without expanding categories using holdouts.

| Branch | Numeric fields | TLD | Rationale |
|---|---|---|---|
| Linear classifier | Training-fitted StandardScaler | Training-fitted one-hot encoding | Regularized linear methods depend on scale |
| Tree ensemble | Recorded values unchanged | Training-fitted one-hot encoding | Tree splits do not require standardization |

Scaling subtracts the training mean and divides by training standard deviation; it does not
remove outliers or create normality. No imputation is needed here. ColumnTransformer/Pipeline
keep transformations together. Any future cross-validation must refit preprocessing inside
each training fold rather than split matrices already transformed using all training rows.
''',
    76:'''### 14.2. Apply training transformations to holdouts

Validation/test use transform only. Means, variances and categories are not learned there.
Unknown-category counts are schema-compatibility diagnostics, not performance-based tuning.
The code verifies that transformation leaves learned parameters unchanged.
''',
    78:'''### 14.3. Transformation checks and interpretation

Check matrix shapes/finite values, manually calculated numeric scaling, preservation in the
tree branch, and all-zero TLD behavior for a synthetic unseen category. Successful
preprocessing does not establish predictive success. The original X/y tables remain unchanged.
''',
    80:'''## 15. Exploratory hypothesis: recorded URL-length distributions

**H0:** Recorded URLLength has the same distribution in phishing and legitimate observations.
**H1:** The distributions differ. Variable: recorded URLLength, without scaling/clipping.
Data: training only. Significance level: 0.05. The hypothesis was specified after EDA.

### 15.1. Analysis unit and test choice

First describe all training rows, then randomly select one observation per normalized training
hostname with fixed seed 20261121, without conditioning selection on length or label.
This reduces repeated-host weighting but changes the descriptive unit to host representatives.
Registered-domain/campaign dependence may persist, so independence is not guaranteed.

Use empirical two-sample KS distance D, the maximum absolute ECDF gap, to compare
distributions rather than only medians. Recorded lengths are tied/discrete, so the continuous
KS p-value is not used. A fixed-class-size label-permutation reference with 1,999 permutations
is constructed, assuming representative exchangeability under H0 and acknowledging its limits.
[Permutation principles](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.permutation_test.html).
''',
    82:'''### 15.2. Monte Carlo permutation test and effect sizes

Keep sample sizes fixed, permute assignments, and compute D from counts at actual distinct
lengths rather than histogram bins. Estimate p=(at_least_as_extreme+1)/(B+1).
The minimum reportable Monte Carlo value is 0.0005, not an exact population p-value.
Report median difference and signed rank effect alongside D; neither establishes causality.
''',
    84:'''### 15.3. Visual evidence and interpretation

ECDFs use within-class fractions in the host-representative sample; log1p affects display
only. The permutation histogram compares null-reference distances with observed D.
These are statistical descriptors, not classifier performance measurements.
''',
    }
    for i,text in translations.items():
        assert nb.cells[i].cell_type=='markdown',i
        nb.cells[i].source=text.strip()
    # Preserve the already-English model rationale table and references, replace its Turkish prose.
    c=nb.cells[86]
    if 'Bu seçim' in c.source:
        start=c.source.index('Bu seçim');end=c.source.index('References:')
        c.source=c.source[:start]+'''The two learned models represent different families, not a claim that either is globally best.
The dummy model is the non-informative baseline. Other candidates require a separately justified
comparison; increased complexity does not guarantee improvement. Model/configuration selection
uses validation, and the final test does not choose the candidate. No classifier is fitted here.

'''+c.source[end:]
    nb.cells[64].source=nb.cells[64].source.replace('Bu liste sınırları kaydeder; bütün sorunların çözüldüğünü veya sızıntı\nbulunduğunu kanıtlamaz.',
        'This checklist records limitations; it does not prove that all risks are resolved or that leakage exists.')

    # Translate executable narrative and table labels, keeping variable names and source schema intact.
    replacements={
      'Sürüm':'Version','Yapı':'Structure','Sayı':'Count','Yok':'None',
      '**Bulgu:** Eksik hücre: ':'**Finding:** Missing cells: ', '; boş metin: ':'; blank strings: ',
      '; sonsuz sayı: ':'; infinite values: ','; temel URL kontrolünde sorun: ':'; basic URL issues: ',
      '. **Karar:** Bu aşamada doldurma, kırpma veya satır silme yapılmadı.':'. **Decision:** No imputation, clipping or row removal at this stage.',
      ' ek URL kaydı var; ':' extra URL observations; ',
      ' tekrar URL grubunda özellikler değişiyor. **Yorum:** URL tekrarı, tam satır tekrarıyla aynı değildir. **Karar:** Kayıtları şimdilik koru; tüm tekrar gözlemlerini aynı ayrımda tut.':' repeated URL groups have varying features. **Interpretation:** A repeated URL is not an identical row. **Decision:** Retain observations within one partition.',
      'Aynı URL için çelişkili etiketler incelenmeli; ayrım durduruldu.':'Conflicting labels require review; splitting stopped.',
      'URL sorunları gruplama öncesi incelenmeli.':'Review URL issues before grouping.',
      'Eksik ayrım dosyaları incelenmeli.':'Review incomplete split files.',
      'Ayrım ayarları değişti; mevcut kilidi inceleyin.':'Split settings differ; inspect the existing lock.',
      'Grup kontrolü':'Group audit',
      '**Karar:** Ayrım kaynak satır numaralarıyla kilitlendi. Ham dosya değişmedi; satır silinmedi. Doğrulama ve test için özellik dağılımları veya hedef ilişkileri incelenmedi. Sonraki bölümler yalnızca `train` ile ilerleyecek.':'**Decision:** Split assignments are locked by source row. No raw values or rows changed. Detailed EDA below uses training only.',
      'Eğitimde tekrar URL grubu: ':'Repeated training URL groups: ', '; bu gruplardaki kayıt: ':'; observations in these groups: ',
      '\\nGrup ':'\\nGroup ',' kayıt, ':' observations, ',' değişen alan':' varying fields','URL (metin):':'URL (text):',
      'değişen_sütun':'varying_column','FILENAME dışında değişen alan yok.':'No varying field other than FILENAME.',
      'politika':'policy','kalan_satır':'retained_rows','çıkarılan_satır':'removed_rows',
      'Tüm kayıtları koru (mevcut)':'Retain all observations (current)',
      'Her URL için ilk kaydı tut (uygulanmadı)':'Keep first observation per URL (not applied)',
      'Tekrar eden URL gruplarını tamamen çıkar (uygulanmadı)':'Remove all repeated URL groups (not applied)',
      'Bu hücre train verisini veya ayrım manifestini değiştirmez.':'This cell does not change training data or split assignments.',
      'En sık URL uzunluğu farkları (kayıtlı - eldeki metin):':'Most common length differences (recorded minus string length):',
      'Ham URL uzunluğu uyuşmayan örnekler:':'Examples with length discrepancies:',
      'Domain uyuşmazlığı örnekleri:':'Domain/hostname discrepancy examples:',
      '**Yorum:** Aşağıdaki kurallar yalnızca denenen adaylar arasında en yüksek uyumu gösterir; üretici formülü doğrulanmış değildir. Özellikle her tekrar çiftinde aynı URL metnine karşı farklı uzunluk değerleri varsa, tek bir deterministik uzunluk kuralı iki kaydı birlikte açıklayamaz.':'**Interpretation:** Best agreement among tested rules does not verify the producer formula. Different recorded lengths for the same string cannot both follow one deterministic string-length rule.',
      '**Karar:** Kayıtlı özelliklere dokunulmadı. Ham metinden yeniden hesaplama ancak özellik kökeni, girdi gösterimi ve ölçüm tanımı açıklığa kavuşturulduktan sonra ayrı isimli sütunlarla değerlendirilecek. Domain örnekleri ve uzunluk farkları bu karar için inceleme kanıtıdır.':'**Decision:** Recorded values remain unchanged. Candidate calculations are audit evidence, not automatic replacements for unverified measurements.',
      'Sabit sayısal sütunlar:':'Constant numeric fields:','İkili sayısal sütun sayısı:':'Binary field count:',
      'Diğer sayısal sütun sayısı:':'Other numeric field count:',
      '**Nasıl okunur?** Medyan (50%) tipik merkezi, 95%/99% üst kuyruğu, maksimum en uç kaydı gösterir. Yüksek sıfır oranı seyrek görülmeyi gösterebilir; tek başına gereksizlik kanıtı değildir. Çarpıklık uç değerlere duyarlıdır ve tek başına dönüşüm gerekçesi sayılmaz.':'**Reading:** Median describes the center, p95/p99 the upper tail and maximum the extreme. Zero concentration and skewness alone do not justify deletion or transformation.',
      '**Dikkat:** Buradaki metin uzunlukları mevcut metinden hesaplanır; kaynak `URLLength` ile aynı tanımda oldukları varsayılmaz. Önceki tutarlılık bulguları geçerlidir.':'**Caution:** String lengths are newly counted descriptors, not assumed equivalent to recorded URLLength. Earlier consistency caveats remain.',
      '**Bulgu:** ':'**Finding:** ', ' sayısal özellik adayı; ':' numeric candidate fields; ', ' ikili alan; ':' binary fields; ',
      ' sabit alan. En az %95 sıfır içeren ':' constant fields. Fields at least 95% zero: ',
      ' alan var. Eğitimde ':'; training contains ', ' farklı TLD bulunuyor; ilk 15 kategori kayıtların %':' TLD categories; the first 15 cover ',
      "'sini kapsıyor.":'% of observations.',
      'Üst kuyruğu belirgin alanlar (çarpıklığa göre ilk 10; hata etiketi değildir):':'Long-tail review (top 10 by skewness; not an error diagnosis):',
      '**Karar:** Eğitim tablosunun değişmediği doğrulandı. Sıfır ağırlıklı alanların anlamı, sayım isimli ikili alanlar ve uzun kuyruklar 8–11. bölümlerde incelenecek; uygulanacak veri hazırlama akışı 12. bölümde belirlenecek.':'**Decision:** Training data remain unchanged. Sparse fields, binary counts and tails are examined before choosing preprocessing.',
      'IQR sıfır olan alanlar (eşik dejenere):':'Zero-IQR fields (degenerate fences):',
      'IQR sıfır olmayan alanlardan en az birinde eşik dışı kalan eğitim kaydı: ':'Training observations outside at least one nondegenerate IQR fence: ',
      '**Yorum:** Çok sayıda kaydın en az bir eşik dışında kalması, hepsinin hatalı olduğu anlamına gelmez. Çok değişkenli veride birçok ayrı eşik uygulamak doğal olarak işaretlenen kayıt sayısını artırır.':'**Interpretation:** Multiple fences and long tails can flag many valid observations; this is not an error rate.',
      'En büyük kayıtlar:':'Largest records:',
      '**Sınır:** Sıfır ihlal bulunması tüm verinin doğru olduğunu kanıtlamaz; yalnızca denenen kuralları geçtiğini gösterir. İhlal bulunması da doğrulanmamış bir kuralın otomatik düzeltme gerekçesi olamaz.':'**Limit:** Zero flags only show that these candidate rules passed. Neither flags nor their absence verify every extraction formula.',
      ' ikili olmayan alan incelendi; ':' nonbinary fields reviewed; ', ' alanda IQR sıfır. ':' zero-IQR fields. ',
      ' kontrol adayında işaretlenen kayıt var. Sayısal sonuçlar üstteki tablolarda kayıtlıdır.':' candidate checks have flagged records. See the tables for measured results.',
      '**Yorum:** Seyrek sayaçlarda IQR sınırı yanıltıcı olabilir. Büyük HTML ölçümleri sıkıştırılmış/minify edilmiş içerik gibi makul nedenlerle oluşabilir; elde HTML olmadan bu açıklama doğrulanmış sayılmaz. Çok uzun URL ve çok sayıda kaynak gerçek bir örüntü de olabilir. **Karar:** Otomatik silme/kırpma uygulanmadı. 12. bölümde kaynak doğrulama, açık tanımlı yeni özellikler ve gerekiyorsa eğitimde öğrenilen dönüşümlerin değerlendirilmesi ayrı kararlar olarak ele alınacak.':'**Interpretation:** Sparse-count IQR fences may be misleading. Large content values may have valid explanations, unverified without original HTML. **Decision:** No automatic deletion or clipping.',
      '**Karar:** Yalnızca eğitim örnekleminde ilişkiler betimlendi. Güçlü farklar özellikle özellik kökeni ve toplama yanlılığı açısından 11. bölüme taşınır; özellik seçimi ve hazırlık akışı 12. bölümde gerekçelendirilecek. Eğitim tablosunun değişmediği doğrulandı.':'**Decision:** Relationships are descriptive and training-only. Strong differences motivate provenance/bias review. Training data remain unchanged.',
      'En yüksek mutlak Spearman değerine sahip 20 çift:':'Top 20 pairs by absolute Spearman correlation:',
      'Pearson ve Spearman farkının en yüksek olduğu 10 çift:':'Top 10 pairs by Pearson/Spearman difference:',
      '**Nasıl okunur?** İki yöntemin belirgin farklılığı uzun kuyruk, uç kayıt, sıfır yığılması veya doğrusal olmayan ilişkiyle bağlantılı olabilir. Hangisinin geçerli olduğunu tek başına bu fark belirlemez.':'**Reading:** Pearson/Spearman disagreement may reflect tails, ties, zeros or nonlinearity; the difference alone does not identify the cause.',
      '**Yorum:** Sıfır ağırlıklı alanlarda basit bir oran adayı yalnızca ortak sıfırlar nedeniyle yüksek eşleşebilir. Bu yüzden pozitif kayıtlardaki kontrol de aşağıda ayrı verilir.':'**Interpretation:** Common zeros can inflate ratio agreement. Positive-count records are checked separately.',
      '**Karar:** Tam eşitlik, yüksek korelasyon, mantıksal türetme ve sınıf karışımı ayrı bulgular olarak kaydedildi. Hiçbir sütun silinmedi; hangi alanın tutulacağı ölçüm tanımı ve köken incelemesi tamamlandıktan sonra 12. bölümde belirlenecek. Eğitim verisinin değişmediği doğrulandı.':'**Decision:** Equality, correlation, derivation and class mixing are separate findings. No field was removed here; training data remain unchanged.',
      '**Yorum:** URL veya sayfa kaynaklı gruplama hesaplama formülünü doğrulamaz. Anahtar kelimelerin hangi metin alanında arandığı belirsizdir. Referans skorlarının kaynak evreni ve hesaplama zamanı ön işleme kararından önce değerlendirilmelidir.':'**Interpretation:** Measurement grouping does not verify formulas. Keyword scope and reference-score populations/timing remain uncertain.',
      'Doğrudan etiket kopyası bulunan sayısal sütunlar:':'Numeric fields exactly copying the target:',
      '**Bulgu:** Eğitimde metin içi https arama kuralı kayıtlı IsHTTPS ile tamamen eşleşiyorsa bu güçlü bir davranış ipucudur, üretici kodunun doğrulanması değildir. Şemadan türetilmiş yeni bir gösterge gerekiyorsa ayrı ve belgeli isimle üretilecektir.':'**Finding:** Agreement with substring search is a behavioral clue, not verified producer code. Recorded IsHTTPS is not certificate validation.',
      '**Karar:** Ölçüm belirsizliği, hedef/referans sızıntısı ve örneklem yanlılığı ayrı kaydedildi. Akademik ön işleme kararları 12. bölümde gerekçelendirilecek. Ham veri, eğitim tablosu ve ayrım değiştirilmedi.':'**Decision:** Measurement uncertainty, target/reference leakage and sample bias are distinguished. Raw data and split assignments remain unchanged.'
    }
    for c in nb.cells:
        if c.cell_type=='code':
            for a,b in sorted(replacements.items(),key=lambda item:len(item[0]),reverse=True):
                c.source=c.source.replace(a,b)
            c.source=c.source.replace('En az bir yöntemde |korelasyon| >= 0.90 olan çiftler:',
                                      'Pairs with |correlation| >= 0.90 in either method:')
            c.source=c.source.replace('# Ayrıntılı EDA için yalnızca eğitim verisi çalışma değişkeninde tutulur.',
                '# Detailed EDA below uses the training partition only.')
        if c.cell_type=='markdown':
            c.source=c.source.replace('../docs/data_dictionary.md','#data-dictionary')
            c.source=c.source.replace('`requirements-eda.txt`','the pinned library list in `README.txt`')
    nb.cells[3].source=nb.cells[3].source.replace(
        "ROOT = next(p for p in (Path.cwd(), *Path.cwd().parents) if (p/'data/raw/PhiUSIIL_Phishing_URL_Dataset.csv').is_file())\nSOURCE = ROOT/'data/raw/PhiUSIIL_Phishing_URL_Dataset.csv'",
        "ROOT = next(p for p in (Path.cwd(), *Path.cwd().parents) if (p/'dataset.csv').is_file() or (p/'data/raw/PhiUSIIL_Phishing_URL_Dataset.csv').is_file())\nSOURCE = ROOT/'dataset.csv' if (ROOT/'dataset.csv').is_file() else ROOT/'data/raw/PhiUSIIL_Phishing_URL_Dataset.csv'")
    if 'SPLITS.mkdir(' not in nb.cells[3].source:
        nb.cells[3].source=nb.cells[3].source.replace("SPLITS = ROOT/'data/processed'","SPLITS = ROOT/'data/processed'\nSPLITS.mkdir(parents=True,exist_ok=True)")
    nb.cells[61].source=re.sub(r'^dictionary_text=.*$',lambda _: 'dictionary_text='+repr(dictionary_md),nb.cells[61].source,flags=re.M)
    frozen=json.loads((ROOT/'reports/final_evaluation/frozen_protocol.json').read_text())
    # Embed the already frozen configuration; no new decisions are made from test outcomes.
    for c in nb.cells:
        if c.cell_type=='code' and 'final_lock_path=FINAL/' in c.source and 'embedded_frozen_protocol=' not in c.source:
            needle="final_lock_path=FINAL/'frozen_protocol.json'"
            provision="\nFINAL.mkdir(parents=True,exist_ok=True)\nembedded_frozen_protocol=json.loads("+repr(json.dumps(frozen))+''')
if not final_lock_path.exists():
    final_lock_path.write_text(json.dumps(embedded_frozen_protocol,indent=2),encoding='utf-8')
else:
    assert json.loads(final_lock_path.read_text(encoding='utf-8'))==embedded_frozen_protocol, 'Existing frozen protocol differs.'
'''
            c.source=c.source.replace(needle,needle+provision)
    # Fail on untranslated Turkish characters in executable explanations or Markdown.
    tr=re.compile('[\u011f\u0131\u015f\u0130\u011e\u015e\u00fc\u00dc\u00e7\u00c7\u00f6\u00d6]')
    failures=[(i,[line for line in c.source.splitlines() if tr.search(line)]) for i,c in enumerate(nb.cells) if tr.search(c.source)]
    assert not failures,failures
    for c in nb.cells:
        if c.cell_type=='code':
            compile(c.source,'<english notebook>','exec');c.outputs=[];c.execution_count=None
    nbf.validate(nb)
    source=ROOT/'data/raw/PhiUSIIL_Phishing_URL_Dataset.csv'
    target=DELIVERY/'dataset.csv'
    if not target.exists():shutil.copy2(source,target)
    assert hashlib.sha256(source.read_bytes()).hexdigest()==hashlib.sha256(target.read_bytes()).hexdigest()
    nbf.write(nb,DELIVERY/f'{PROJECT}.ipynb')
    print('English standalone notebook prepared:',DELIVERY/f'{PROJECT}.ipynb')
    return DELIVERY

if __name__=='__main__':build()
