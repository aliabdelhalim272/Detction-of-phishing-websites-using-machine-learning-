# Data dictionary

| Column | Working meaning | Group / role | Evidence status | Source |
|---|---|---|---|---|
| FILENAME | Source file identifier; UCI states it may be ignored. | Identifier / raw text / grouping | UCI explicit | UCI |
| URL | Recorded website address; raw input for identity and parsing audits. | Identifier / raw text / grouping | Name-based interpretation | Column-name interpretation |
| URLLength | Recorded URL length; exact representation counted is not fully verified. | Recorded numeric feature | Name-based interpretation | Column-name interpretation |
| Domain | Recorded domain/netloc text; may include port or user information. | Identifier / raw text / grouping | Name-based interpretation | Column-name interpretation |
| DomainLength | Recorded domain length. | Recorded numeric feature | Name-based interpretation | Column-name interpretation |
| IsDomainIP | Indicator interpreted as IP-address domain usage. | Recorded numeric feature | Name-based interpretation | Column-name interpretation |
| TLD | Recorded top-level domain category. | Categorical predictor | Name-based interpretation | Column-name interpretation |
| URLSimilarityIndex | Reference-based URL similarity score; reference population and formula need verification. | Recorded numeric feature | Name-based interpretation | Column-name interpretation |
| CharContinuationRate | Character-continuation statistic; author example code is available, CSV parity unverified. | Recorded numeric feature | Author code found | Author example |
| TLDLegitimateProb | TLD legitimacy probability; reference population and estimation process unverified. | Recorded numeric feature | Name-based interpretation | Column-name interpretation |
| URLCharProb | URL character probability score; reference distribution and formula unverified. | Recorded numeric feature | Name-based interpretation | Column-name interpretation |
| TLDLength | Recorded TLD length. | Recorded numeric feature | Name-based interpretation | Column-name interpretation |
| NoOfSubDomain | Recorded subdomain count; suffix/www rules unverified. | Recorded numeric feature | Name-based interpretation | Column-name interpretation |
| HasObfuscation | Obfuscation indicator; detection rules unverified. | Recorded numeric feature | Name-based interpretation | Column-name interpretation |
| NoOfObfuscatedChar | Count of characters identified as obfuscated; detection rules unverified. | Recorded numeric feature | Name-based interpretation | Column-name interpretation |
| ObfuscationRatio | Obfuscated-character ratio; denominator/rounding unverified. | Recorded numeric feature | Name-based interpretation | Column-name interpretation |
| NoOfLettersInURL | Recorded letter count in URL; character scope unverified. | Recorded numeric feature | Name-based interpretation | Column-name interpretation |
| LetterRatioInURL | Recorded letter ratio; denominator/rounding unverified. | Recorded numeric feature | Name-based interpretation | Column-name interpretation |
| NoOfDegitsInURL | Recorded digit count; original misspelling retained. | Recorded numeric feature | Name-based interpretation | Column-name interpretation |
| DegitRatioInURL | Recorded digit ratio; denominator/rounding unverified; original spelling retained. | Recorded numeric feature | Name-based interpretation | Column-name interpretation |
| NoOfEqualsInURL | Recorded equals-sign count. | Recorded numeric feature | Name-based interpretation | Column-name interpretation |
| NoOfQMarkInURL | Recorded question-mark count. | Recorded numeric feature | Name-based interpretation | Column-name interpretation |
| NoOfAmpersandInURL | Recorded ampersand count. | Recorded numeric feature | Name-based interpretation | Column-name interpretation |
| NoOfOtherSpecialCharsInURL | Recorded other-special-character count; character set unverified. | Recorded numeric feature | Name-based interpretation | Column-name interpretation |
| SpacialCharRatioInURL | Recorded special-character ratio; character set and denominator unverified. | Recorded numeric feature | Name-based interpretation | Column-name interpretation |
| IsHTTPS | Recorded HTTPS indicator; not certificate validation; scheme mismatches audited. | Recorded numeric feature | Name-based interpretation | Column-name interpretation |
| LineOfCode | Recorded source-code line count. | Recorded numeric feature | Name-based interpretation | Column-name interpretation |
| LargestLineLength | Recorded maximum source-code line length. | Recorded numeric feature | Name-based interpretation | Column-name interpretation |
| HasTitle | Page-title presence indicator. | Recorded numeric feature | Name-based interpretation | Column-name interpretation |
| Title | Recorded raw page title text. | Identifier / raw text / grouping | Name-based interpretation | Column-name interpretation |
| DomainTitleMatchScore | Domain/title matching score; author example inspected, CSV parity unverified. | Recorded numeric feature | Author code found | Author example |
| URLTitleMatchScore | URL/title matching score; author example inspected, CSV parity unverified. | Recorded numeric feature | Author code found | Author example |
| HasFavicon | Favicon presence indicator. | Recorded numeric feature | Name-based interpretation | Column-name interpretation |
| Robots | Robots-related indicator; robots.txt versus metadata rule unverified. | Recorded numeric feature | Name-based interpretation | Column-name interpretation |
| IsResponsive | Responsive-page indicator; detection rule unverified. | Recorded numeric feature | Name-based interpretation | Column-name interpretation |
| NoOfURLRedirect | Recorded URL redirects; only 0/1 observed, original counting rule unverified. | Recorded numeric feature | Name-based interpretation | Column-name interpretation |
| NoOfSelfRedirect | Recorded self-redirects; self-redirect definition unverified. | Recorded numeric feature | Name-based interpretation | Column-name interpretation |
| HasDescription | Page-description presence indicator. | Recorded numeric feature | Name-based interpretation | Column-name interpretation |
| NoOfPopup | Recorded popup count; detection method unverified. | Recorded numeric feature | Name-based interpretation | Column-name interpretation |
| NoOfiFrame | Recorded iframe count. | Recorded numeric feature | Name-based interpretation | Column-name interpretation |
| HasExternalFormSubmit | External form-submit indicator; external-target rule unverified. | Recorded numeric feature | Name-based interpretation | Column-name interpretation |
| HasSocialNet | Social-network signal indicator; scope unverified. | Recorded numeric feature | Name-based interpretation | Column-name interpretation |
| HasSubmitButton | Submit-button presence indicator. | Recorded numeric feature | Name-based interpretation | Column-name interpretation |
| HasHiddenFields | Hidden-form-field presence indicator. | Recorded numeric feature | Name-based interpretation | Column-name interpretation |
| HasPasswordField | Password-field presence indicator. | Recorded numeric feature | Name-based interpretation | Column-name interpretation |
| Bank | Bank-related keyword indicator; vocabulary and searched text unverified. | Recorded numeric feature | Name-based interpretation | Column-name interpretation |
| Pay | Payment-related keyword indicator; matching rule unverified. | Recorded numeric feature | Name-based interpretation | Column-name interpretation |
| Crypto | Cryptocurrency-related keyword indicator; matching rule unverified. | Recorded numeric feature | Name-based interpretation | Column-name interpretation |
| HasCopyrightInfo | Copyright-information presence indicator. | Recorded numeric feature | Name-based interpretation | Column-name interpretation |
| NoOfImage | Recorded image count; element scope unverified. | Recorded numeric feature | Name-based interpretation | Column-name interpretation |
| NoOfCSS | Recorded CSS resource count; inline/external scope unverified. | Recorded numeric feature | Name-based interpretation | Column-name interpretation |
| NoOfJS | Recorded JavaScript resource count; inline/external scope unverified. | Recorded numeric feature | Name-based interpretation | Column-name interpretation |
| NoOfSelfRef | Recorded same-site reference count; site boundary rule unverified. | Recorded numeric feature | Name-based interpretation | Column-name interpretation |
| NoOfEmptyRef | Recorded empty-reference count; empty/# handling unverified. | Recorded numeric feature | Name-based interpretation | Column-name interpretation |
| NoOfExternalRef | Recorded external-reference count; external-target rule unverified. | Recorded numeric feature | Name-based interpretation | Column-name interpretation |
| label | Original target: 0 phishing, 1 legitimate; confirmed by UCI. | Target | UCI explicit | UCI |