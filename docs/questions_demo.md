# ❓ Questions de Démonstration - Risk, Compliance & Audit Analytics

## 📋 Liste de Questions pour Data Agent

Voici 15 questions progressives pour démontrer les capacités du Data Agent sur les données Risk, Compliance & Audit.

---

## 🎯 Niveau 1 : Questions Factuelles (Lecture Simple)

### Q1 : Taux de Conformité Global

**Question :**  
> "Quel est le taux de conformité global actuel ?"

**Objectif :** Baseline assessment de la santé compliance  
**Capacité démontrée :** Agrégation control_executions + calcul métrique  
**Réponse attendue :**
```
**Taux de Conformité Global : 69.9%**

Statuts des exécutions (24 derniers mois) :
- Passed: 23,845 (70%)
- Failed: 6,817 (20%)
- Not Tested: 2,729 (8%)
- Exception: 700 (2%)

🎯 **Target:** >90%
⚠️ **Gap:** -20.1 points (BELOW TARGET)

📊 **Status:** Requires immediate attention before external audit
```

**✅ Validation :**
- Calcul compliance rate correct (passed/total)
- Comparaison au target 90%
- Identification gap significatif

---

### Q2 : Distribution par Framework

**Question :**  
> "Quel est le taux de conformité par framework (SOX, GDPR, ISO27001, PCI-DSS) ?"

**Objectif :** Identifier quel framework a le plus besoin d'attention  
**Capacité démontrée :** Jointure controls + executions, groupBy framework  
**Réponse attendue :**
```
**Compliance Rate par Framework:**

| Framework  | Controls | Executions | Passed Rate | Status |
|------------|----------|------------|-------------|--------|
| SOX        | 45       | 10,227     | 68.5%       | ⚠️ Below target |
| GDPR       | 37       | 8,523      | 71.2%       | ⚠️ Below target |
| ISO27001   | 45       | 10,227     | 70.1%       | ⚠️ Below target |
| PCI-DSS    | 22       | 5,114      | 69.8%       | ⚠️ Below target |

📊 **Insight:** All frameworks below 90% target — no single framework is driving the issue.

💡 **Recommendation:** Issue is cross-framework (likely systemic: automation, process adherence, resource allocation)
```

**✅ Validation :**
- Tous frameworks sous 90%
- Distribution cohérente avec config (SOX 30%, GDPR 25%, ISO27001 30%, PCI-DSS 15%)
- Identification problème systémique vs framework-specific

---

### Q3 : Incidents Non Résolus

**Question :**  
> "Combien d'incidents critiques/high sont encore open ou investigating ?"

**Objectif :** Évaluer risque exposition pour audit externe  
**Capacité démontrée :** Filtrage multi-critères (severity + status)  
**Réponse attendue :**
```
**Incidents Non Résolus (High-Severity):**

| Severity | Open | Investigating | Total | % Total Incidents |
|----------|------|---------------|-------|-------------------|
| Critical | 8    | 12            | 20    | 10%               |
| High     | 15   | 22            | 37    | 18.5%             |
| **TOTAL**| **23**| **34**       | **57**| **28.5%**         |

⚠️ **Risk:** 57 high-severity incidents unresolved = RED FLAG for external auditors

📊 **Age Distribution (Open incidents):**
- <30 days: 18 incidents (acceptable)
- 30-90 days: 25 incidents ⚠️
- >90 days: 14 incidents ❌ (indicates slow remediation process)

💡 **Urgent Action:** Close all >90 days incidents before audit (in 3 weeks)
```

**✅ Validation :**
- Comptage incidents par severity + status
- Identification 14 incidents >90 jours (critical)
- Recommandation d'action urgente

---

## 🔍 Niveau 2 : Analyses Comparatives

### Q4 : Contrôles SOX Critiques

**Question :**  
> "Quels sont les contrôles SOX avec taux d'échec >30% ?"

**Objectif :** Identifier critical gaps avant audit SOX externe  
**Capacité démontrée :** Filtrage framework + calcul failure rate + tri  
**Réponse attendue :**
```
**Contrôles SOX avec Failure Rate >30%:**

| Control ID | Control Name | Criticality | Failure Rate | Executions | Impact |
|------------|--------------|-------------|--------------|------------|--------|
| CTRL_023   | User Access Review - Quarterly | Critical | 42% | 8 | ❌ HIGH |
| CTRL_045   | Segregation of Duties Matrix | Critical | 38% | 8 | ❌ HIGH |
| CTRL_067   | Change Management Approval | High | 35% | 24 | ⚠️ MEDIUM |
| CTRL_089   | Financial Close Reconciliation | Critical | 33% | 24 | ❌ HIGH |
| CTRL_112   | IT General Controls Audit | High | 31% | 12 | ⚠️ MEDIUM |

🎯 **Total:** 5 SOX controls with >30% failure rate

⚠️ **Critical Finding:** 3 controls marked "Critical" with 33-42% failure → unacceptable for SOX 404 compliance

💡 **Recommendation Priority:**
1. CTRL_023 (Access Review) — Implement automated quarterly review
2. CTRL_045 (SoD Matrix) — Update matrix + automated conflict detection
3. CTRL_089 (Financial Close) — Strengthen reconciliation process + training
```

**✅ Validation :**
- Filtrage framework=SOX
- Calcul failure rate >30%
- Tri par criticality puis failure rate
- Recommandations priorisées

---

### Q5 : Évolution Compliance dans le Temps

**Question :**  
> "Comment le taux de conformité a évolué sur les 24 derniers mois ?"

**Objectif :** Identifier tendance (amélioration vs dégradation)  
**Capacité démontrée :** Time-series analysis  
**Réponse attendue :**
```
**Évolution Compliance Rate (Monthly):**

Q1 2023: 72%
Q2 2023: 74%
Q3 2023: 76% ✅ (improving trend)
Q4 2023: 75%
Q1 2024: 72% ⚠️ (decline starts)
Q2 2024: 70%
Q3 2024: 68%
Q4 2024: 67% ❌
Q1 2025: 69% (slight improvement but still critical)

📊 **Trend Analysis:**
- Peak: Q3 2023 (76%)
- Current: Q1 2025 (69%)
- **Decline: -7 points over 18 months**

🔍 **Inflection Point:** Q4 2023 → Q1 2024 (decline starts)

💡 **Root Cause Investigation Needed:**
What changed in Q1 2024 that caused decline?
- Resource turnover?
- Process change?
- System migration?
- Budget cuts?
```

**✅ Validation :**
- Time-series groupBy month
- Identification peak (Q3 2023) et inflection point (Q1 2024)
- Question root cause investigation

---

### Q6 : Efficacité Détection Incidents

**Question :**  
> "Quel pourcentage d'incidents sont détectés par contrôles vs découverts autrement ?"

**Objectif :** Mesurer efficacité control framework  
**Capacité démontrée :** Analyse incident.execution_id (nullable)  
**Réponse attendue :**
```
**Incident Detection Analysis:**

| Detection Method | Count | Percentage |
|------------------|-------|------------|
| Detected by Control (execution_id != null) | 60 | 30% ✅ |
| Discovered Otherwise (execution_id = null) | 140 | 70% ❌ |

📊 **70% incidents NOT detected by controls** → indicates control coverage gap

**Breakdown of "Discovered Otherwise":**
- Employee reporting: ~35%
- External notification (vendor, customer): ~25%
- System alerts (non-control): ~20%
- Random discovery: ~20%

⚠️ **Control Effectiveness:** Only 30% detection rate is LOW

🎯 **Target:** >80% incidents should be detected by controls (proactive vs reactive)

💡 **Recommendations:**
1. Review control frequency (increase from quarterly to monthly for high-risk)
2. Add automated controls for areas with high "discovered otherwise" incidents
3. Implement continuous monitoring vs periodic testing
```

**✅ Validation :**
- Calcul 30% détectés par contrôles (execution_id != null)
- Identification gap 70% non détectés
- Recommandations pour améliorer coverage

---

## 🧠 Niveau 3 : Analyses avec IA (Texte Non-Structuré)

### Q7 : Extraction Recommandations Audit

**Question :**  
> "Extrais des audit_reports les recommandations les plus récurrentes pour contrôles SOX"

**Objectif :** Identifier systemic issues via AI text analysis  
**Capacité démontrée :** AI Shortcut extraction + pattern recognition  
**Réponse attendue :**
```
**Top Recommandations Récurrentes (Audit Reports SOX):**

📄 **Mentioned 23 times:**
"Implement automated alerts for [control name]"

📄 **Mentioned 18 times:**
"Documentation process incomplete — add mandatory checklist items"

📄 **Mentioned 15 times:**
"Manual process not followed consistently — requires automation or training"

📄 **Mentioned 12 times:**
"Evidence retention insufficient — implement automated archival"

📄 **Mentioned 9 times:**
"Approval workflow bypassed — enforce system-level controls"

---

🔍 **Pattern Identified:** 
**LACK OF AUTOMATION** is mentioned in 68% of audit reports (combining "automated alerts", "automation or training", "system-level controls")

💡 **Strategic Insight:**
The compliance gap is NOT a people problem (training, awareness) but a PROCESS/TECHNOLOGY problem.

🎯 **Recommendation:**
Invest in automation platform (e.g., GRC tool) to:
1. Automated control execution (reduce manual)
2. Automated evidence collection
3. Automated alerts/notifications
4. Workflow enforcement

**Projected Impact:** 
Manual controls (35% of total) with 58% pass rate → Automated controls (65% of total) with 92% pass rate
If automate 20 manual controls → Compliance rate 69% → 84% (+15 points)
```

**✅ Validation :**
- Extraction texte audit_reports
- Comptage mentions (23, 18, 15...)
- Pattern recognition ("automation")
- Projection impact business case

---

### Q8 : Analyse Root Causes Incidents

**Question :**  
> "Analyse les incident_descriptions pour identifier les root causes mentionnées >10 fois"

**Objectif :** Découvrir patterns structurels via AI  
**Capacité démontrée :** NLP sur texte non structuré  
**Réponse attendue :**
```
**Root Causes Récurrentes (Incident Descriptions):**

📄 **"Manual process failure" — 62 mentions (31%)**
Example extracts:
- "Manual email notification was missed due to high HR turnover"
- "Manual reconciliation process not performed on schedule"
- "Manual access review delayed by 3 weeks due to owner vacation"

📄 **"Lack of automation" — 48 mentions (24%)**
Example extracts:
- "No automated trigger from HR system to IT Security for access revocation"
- "Offboarding checklist is manual — no system integration"
- "Alert should be automated but currently requires manual monitoring"

📄 **"Training gap / Human error" — 38 mentions (19%)**
Example extracts:
- "New employee not trained on [process]"
- "Checklist step skipped due to unfamiliarity"
- "Incorrect interpretation of policy requirement"

📄 **"System limitation" — 22 mentions (11%)**
Example extracts:
- "Legacy system does not support [required control]"
- "API integration not available between [System A] and [System B]"

📄 **"Resource constraint" — 18 mentions (9%)**
Example extracts:
- "Control owner on extended leave, backup not designated"
- "Insufficient staffing to complete quarterly review"

---

🎯 **Top 2 Root Causes = 55% of incidents:**
1. Manual process failure (31%)
2. Lack of automation (24%)

💡 **Strategic Conclusion:**
**Automation is the solution to 55% of incidents.**

This is consistent with audit report findings (Q7) → converging evidence from multiple data sources.

🚀 **Recommended Investment Priority:**
1. HR-IT integration (offboarding automation)
2. Access review automation
3. Evidence collection automation
```

**✅ Validation :**
- NLP extraction root causes
- Comptage >10 mentions
- Convergence avec Q7 (audit reports)
- Business case automation

---

### Q9 : Pattern Offboarding

**Question :**  
> "Cherche dans incident_descriptions toute mention de 'offboarding', 'termination', ou 'access revocation'"

**Objectif :** Identifier HR-IT integration gap spécifique  
**Capacité démontrée :** Semantic search multi-termes  
**Réponse attendue :**
```
**Incidents liés Offboarding/Access Revocation:**

📄 **Total incidents mentionnant ces termes: 18 (9% du total)**

**Sample Extracts:**

📄 INC_00012345 (High severity):
> "Access not revoked after employee termination 30+ days ago. Offboarding 
> workflow does not include automated trigger to IT Security. Manual email 
> notification was missed due to high HR turnover."

📄 INC_00023456 (Critical severity):
> "Terminated contractor still had VPN access 45 days post-departure. No 
> automated reconciliation between HR termination list and Active Directory."

📄 INC_00034567 (High severity):
> "Access revocation delayed 2 weeks after termination. Manual process relies 
> on HR sending email to IT Security, which was missed due to vacation coverage gap."

---

🔍 **Pattern Identified:**

**Root Cause:** HR-IT offboarding process is MANUAL (email-based)
- Single point of failure: HR email notification
- No automated reconciliation
- No backup process when owner absent

**Frequency:** 18 incidents / 24 months = 0.75 incidents/month (recurring!)

**Impact:**
- 12 incidents = High severity (unauthorized access to customer data)
- 6 incidents = Critical severity (elevated privileges to production)

🎯 **Control That Should Catch This:**
CTRL_023: "User Access Review - Quarterly"
- Current compliance rate: **58%** ❌
- Why failing: Manual quarterly review insufficient frequency for 0.75 incidents/month

💡 **Recommended Fix:**
1. **Immediate (Week 1):** API integration HR system → IT Security (automated trigger)
2. **Short-term (Week 2-3):** Automated reconciliation HR terminations vs Active Directory (weekly)
3. **Long-term (Month 2):** Increase CTRL_023 frequency from Quarterly → Monthly

**Projected Impact:**
- Eliminate 18 incidents/24 months → 0 incidents
- CTRL_023 compliance rate 58% → 95% (automated vs manual)
- GDPR risk reduction: Unauthorized data access is material breach
```

**✅ Validation :**
- Search sémantique 3 termes
- Extraction 18 incidents
- Identification pattern (manual email)
- Control linkage (CTRL_023)
- Action plan 3 phases

---

## 💰 Niveau 4 : Business Intelligence & ROI

### Q10 : Vendor Risk Élevé

**Question :**  
> "Quels vendors ont risk_score >70 ET incidents non résolus ?"

**Objectif :** Identifier third-party risk critique  
**Capacité démontrée :** Jointure vendors + incidents, filtres multiples  
**Réponse attendue :**
```
**High-Risk Vendors avec Incidents Actifs:**

| Vendor ID | Vendor Name | Service Category | Risk Score | Incidents (Open/Investigating) | Compliance Status |
|-----------|-------------|------------------|------------|--------------------------------|-------------------|
| VND_042   | CloudStorage Inc. | Cloud Storage | 78.5 | 3 (2 High, 1 Medium) | Non-compliant ⚠️ |
| VND_067   | PayGateway Systems | Payment Processing | 76.2 | 2 (1 Critical, 1 High) | Pending review |
| VND_089   | DataAnalytics Pro | Data Analytics | 74.8 | 2 (2 High) | Non-compliant ⚠️ |
| VND_112   | HR Cloud Solutions | HR Systems | 72.1 | 1 (1 High) | Compliant |
| VND_134   | SecureAuth Ltd. | Security Tools | 71.5 | 2 (1 High, 1 Medium) | Pending review |

🎯 **Total:** 5 vendors avec risk_score >70 + incidents actifs

⚠️ **Critical Vendors (requires immediate action):**

**VND_042 (CloudStorage Inc.)** — Risk Score 78.5
- Incidents: Data breach (INC_00045678), Access violation (INC_00056789)
- Compliance: Non-compliant (failed SOC2 audit)
- Last audit: 8 months ago (overdue)
- **Action:** Demand re-certification within 30 days OR replace vendor

**VND_067 (PayGateway Systems)** — Risk Score 76.2
- Incidents: System failure causing PCI-DSS violation (INC_CRITICAL_001)
- Compliance: Pending review (PCI-DSS re-cert in progress)
- **Action:** Escalate to executive sponsor, require weekly status update

💡 **Third-Party Risk Management Recommendations:**
1. Quarterly vendor risk review (currently ad-hoc)
2. Automated risk scoring based on:
   - Certifications expiry
   - Incident history
   - Audit findings
3. Mandatory re-certification for risk_score >70
4. Exit strategy for vendors non-compliant >90 days
```

**✅ Validation :**
- Jointure vendors + incidents
- Filtrage risk_score >70 + status IN (open, investigating)
- Priorisation par risk_score
- Recommandations actionnables

---

### Q11 : MTTR Actions Correctives

**Question :**  
> "Quel est le Mean Time To Remediate (MTTR) pour les actions correctives par criticité d'incident ?"

**Objectif :** Mesurer efficacité remediation process  
**Capacité démontrée :** Calcul DATEDIFF + agrégation  
**Réponse attendue :**
```
**Mean Time To Remediate (MTTR) Analysis:**

| Incident Severity | Actions | Avg MTTR (days) | Target | Status |
|-------------------|---------|-----------------|--------|--------|
| Critical          | 38      | 12.5            | <7     | ❌ 78% over target |
| High              | 68      | 14.2            | <10    | ⚠️ 42% over target |
| Medium            | 58      | 18.7            | <14    | ⚠️ 33% over target |
| Low               | 22      | 25.3            | <21    | ⚠️ 20% over target |

📊 **Overall MTTR:** 15.8 days (vs target 10 days) → **58% over target**

**Breakdown by Action Type:**

| Action Type | Avg MTTR | % On-Time Completion |
|-------------|----------|---------------------|
| System Patch | 8.2 days | 85% ✅ |
| Access Revocation | 3.5 days | 92% ✅ |
| Process Improvement | 28.4 days | 45% ❌ |
| Policy Update | 32.1 days | 38% ❌ |
| Training | 21.5 days | 55% ⚠️ |

🔍 **Root Cause of Delays:**

**Process Improvement & Policy Update** have longest MTTR (28-32 days):
- Requires multi-stakeholder approval
- Cross-functional coordination (Legal, HR, IT, Compliance)
- No dedicated project manager

**Impact:**
- 25 actions currently OVERDUE (>14 days past due_date)
- Incidents remain "open" waiting for remediation → audit exposure

💡 **Recommendations:**
1. **Immediate:** Assign dedicated remediation PM for Critical/High incidents
2. **Process:** Streamline approval workflow (reduce from 5 approvers to 2)
3. **Automation:** System Patch + Access Revocation already efficient (85-92%) — replicate this model
4. **Target:** Reduce MTTR to <10 days average (current 15.8 days)

**Projected Impact:**
- Reduce overdue actions from 25 → <5
- Improve audit readiness (fewer open incidents)
- Faster risk mitigation (12.5 days → 7 days for Critical)
```

**✅ Validation :**
- Calcul MTTR (completion_date - start_date)
- Agrégation par severity + action_type
- Identification goulots (Process Improvement, Policy Update)
- Recommandations process improvement

---

### Q12 : Simulation Automation Impact

**Question :**  
> "Si j'automatise les 5 contrôles manuels les plus failing, quel impact sur le compliance rate global ?"

**Objectif :** Business case pour investissement automation  
**Capacité démontrée :** Simulation what-if scenario  
**Réponse attendue :**
```
**Automation Impact Simulation:**

**Top 5 Manual Controls (Highest Failure Rate):**

| Control ID | Control Name | Current Pass Rate | Executions | Manual? |
|------------|--------------|-------------------|------------|---------|
| CTRL_023   | User Access Review - Quarterly | 58% | 8 | ✅ Manual |
| CTRL_045   | Segregation of Duties Matrix | 62% | 8 | ✅ Manual |
| CTRL_067   | Change Management Approval | 65% | 24 | ✅ Manual |
| CTRL_089   | Financial Close Reconciliation | 67% | 24 | ✅ Manual |
| CTRL_112   | IT General Controls Audit | 69% | 12 | ✅ Manual |

**Current State:**
- Total executions (5 controls): 76
- Passed: 48
- **Current pass rate (5 controls): 63.2%**

**Projected State (Post-Automation):**
Assuming automated controls achieve 92% pass rate (benchmark from existing automated controls):
- Total executions: 76
- Passed (projected): 70
- **Projected pass rate (5 controls): 92.1%**

---

📊 **Impact on Global Compliance Rate:**

**Before Automation:**
- Total executions (all controls): 34,091
- Passed: 23,845
- **Global compliance rate: 69.9%**

**After Automation (5 controls):**
- Incremental passed: +22 (70 - 48)
- New total passed: 23,867
- **New global compliance rate: 70.6%** (+0.7 points)

⚠️ **Wait, only +0.7 points?**

Let me recalculate with ALL 52 manual controls (35% of 149 = 52):

**All Manual Controls:**
- Current pass rate: 58%
- Executions: ~11,930 (35% of 34,091)
- Passed currently: 6,919

**If automate ALL manual controls:**
- Projected pass rate: 92%
- Projected passed: 10,975
- Incremental: +4,056

**New Global Compliance Rate:**
- (23,845 - 6,919 + 10,975) / 34,091 = **81.2%** (+11.3 points) ✅

---

💰 **Business Case:**

**Investment:**
- GRC automation platform: $250K (initial)
- Implementation (52 controls × $5K avg): $260K
- **Total: $510K**

**Benefits:**
- Compliance rate: 69.9% → 81.2% (+11.3 points)
- Gap to 90% target: -20.1 → -8.8 (reduced by 56%)
- MTTR reduction: 15.8 → 8.5 days (automated evidence collection)
- Audit findings reduction: 35 → 12 (fewer manual control failures)

**Avoid Costs:**
- SOX non-certification risk: $50M (stock price impact)
- GDPR fines: €5M (3 data breach incidents/year)
- Audit remediation costs: $180K/year (fewer findings)

**ROI:** ($55M - $0.51M) / $0.51M = **10,680%** over 3 years

🎯 **Recommendation:** STRONGLY APPROVE automation investment
```

**✅ Validation :**
- Identification 5 contrôles manuels worst performing
- Calcul impact partiel (+0.7 points)
- Recalcul avec TOUS contrôles manuels (+11.3 points)
- Business case complet (investment + ROI)

---

## 🔬 Niveau 5 : Analyses Avancées

### Q13 : Corrélation Control Criticality vs Compliance

**Question :**  
> "Y a-t-il une corrélation entre la criticité des contrôles et leur taux de conformité ?"

**Objectif :** Vérifier si contrôles critiques sont mieux exécutés  
**Capacité démontrée :** Analyse statistique multi-tables  
**Réponse attendue :**
```
**Correlation Analysis: Control Criticality vs Compliance Rate**

| Criticality | Controls | Avg Compliance Rate | Expectation |
|-------------|----------|---------------------|-------------|
| Critical    | 30       | 65.2%               | Should be >90% ❌ |
| High        | 52       | 68.7%               | Should be >85% ❌ |
| Medium      | 45       | 72.4%               | Should be >80% ⚠️ |
| Low         | 22       | 78.1%               | Should be >75% ✅ |

⚠️ **INVERTED CORRELATION:** 
Critical controls have LOWER compliance (65.2%) than Low controls (78.1%)

This is OPPOSITE of what should happen!

🔍 **Root Cause Investigation:**

**Why are Critical controls failing more?**

Analysis shows:
1. **Manual execution:** 75% of Critical controls are manual (vs 30% for Low)
2. **Frequency burden:** Critical = daily/weekly (high execution volume → fatigue)
3. **Complexity:** Critical controls require multi-step process + evidence collection
4. **Resource constraint:** Same 12 control owners handle Critical + Low → prioritize Low (easier)

**Evidence from audit_reports (AI extract):**
> "Critical controls are consistently marked 'Not Tested' or 'Exception' due to 
> owner workload. Recommendation: Automate Critical controls as priority."

💡 **Strategic Insight:**

The compliance program is BACKWARDS:
- **Critical controls** (highest risk) = 65% compliance (most likely to fail)
- **Low controls** (lowest risk) = 78% compliance (least likely to fail)

This creates MAXIMUM RISK exposure.

🎯 **Urgent Recommendations:**
1. **Week 1:** Audit all 30 Critical controls — identify automation candidates
2. **Week 2-3:** Automate top 10 Critical controls (est. cost $50K)
3. **Week 4+:** Increase frequency of Critical control review (weekly → daily monitoring)

**Projected Impact:**
- Critical controls: 65.2% → 90% (+24.8 points)
- Global compliance: 69.9% → 78.6% (+8.7 points)
- Risk exposure: REDUCED by 60% (Critical controls protecting key assets)
```

**✅ Validation :**
- Corrélation inverse identifiée
- Root cause (manual + frequency + complexity)
- Evidence AI extraction (audit reports)
- Recommandations stratégiques

---

### Q14 : Vendor Risk Score Validation

**Question :**  
> "Valide la formule risk_score en comparant vendors avec incidents vs sans incidents"

**Objectif :** Vérifier si risk_score prédit effectivement incidents  
**Capacité démontrée :** Validation modèle prédictif  
**Réponse attendue :**
```
**Vendor Risk Score Validation:**

**Formula (from AGENTS.md):**
```
Risk Score = Criticality×40% + Compliance_Gap×30% + Audit_Age×30%
```

**Validation Test:**

| Risk Score Range | Vendors | With Incidents | Incident Rate |
|------------------|---------|----------------|---------------|
| 80-100 (Extreme) | 8       | 7              | 87.5% ⚠️     |
| 70-79 (High)     | 15      | 9              | 60.0%         |
| 60-69 (Medium)   | 28      | 8              | 28.6%         |
| 50-59 (Low)      | 35      | 6              | 17.1%         |
| <50 (Minimal)    | 14      | 1              | 7.1% ✅       |

📊 **Correlation:** Strong positive correlation (r = 0.82)

**Risk Score >70:** 60-87% have incidents ⚠️  
**Risk Score <50:** 7% have incidents ✅

✅ **Conclusion:** Risk score formula is PREDICTIVE

---

**Incident Severity by Risk Score:**

| Risk Score Range | Avg Incident Severity | Critical/High % |
|------------------|----------------------|-----------------|
| 80-100           | 2.8 (High)           | 71%             |
| 70-79            | 2.2 (High-Medium)    | 56%             |
| 60-69            | 1.9 (Medium)         | 38%             |
| <60              | 1.5 (Medium-Low)     | 25%             |

(Severity scale: Critical=4, High=3, Medium=2, Low=1)

✅ **Validation:** High risk score → Higher severity incidents (as expected)

---

💡 **Actionable Insights:**

**8 vendors with risk_score 80-100:**
- 7 have had incidents (87.5%)
- 5 incidents are Critical/High severity
- **Recommendation:** Quarterly executive review + exit strategy if non-compliant >90 days

**15 vendors with risk_score 70-79:**
- 9 have had incidents (60%)
- **Recommendation:** Monthly risk review + compliance improvement plan

**Threshold Proposal:**
- Risk Score >80: **Immediate action required**
- Risk Score 70-80: **Enhanced monitoring**
- Risk Score <70: **Standard monitoring**

🎯 **Use Case for Data Agent:**
"Show me all vendors with risk_score >70 AND compliance_status = 'non_compliant'"
→ Immediate escalation list for board review
```

**✅ Validation :**
- Test corrélation risk_score ↔ incidents
- Validation formule (r = 0.82)
- Severity correlation
- Actionable thresholds (>80, 70-80, <70)

---

### Q15 : Framework Overlap Analysis

**Question :**  
> "Quels contrôles couvrent plusieurs frameworks ? Peut-on optimiser en consolidant ?"

**Objectif :** Identifier opportunities de simplification compliance program  
**Capacité démontrée :** Cross-framework mapping + optimization  
**Réponse attendue :**
```
**Framework Overlap Analysis:**

**Current State:**
- Total controls: 149
- SOX-only: 28
- GDPR-only: 18
- ISO27001-only: 25
- PCI-DSS-only: 12
- **Multi-framework: 66 (44% of total)** ✅

**Multi-Framework Controls Breakdown:**

| Framework Combination | Controls | Example |
|-----------------------|----------|---------|
| SOX + ISO27001        | 18       | Access Review, Change Mgmt |
| GDPR + ISO27001       | 15       | Data Classification, Encryption |
| SOX + PCI-DSS         | 8        | Financial Controls |
| All 4 frameworks      | 12       | Incident Response, Backup/Recovery |
| Other combinations    | 13       | Various |

🔍 **Optimization Opportunity:**

**12 controls cover ALL 4 frameworks** (SOX + GDPR + ISO27001 + PCI-DSS):
- CTRL_005: Incident Response Plan
- CTRL_018: Backup & Recovery Testing
- CTRL_042: Disaster Recovery Plan
- CTRL_067: Change Management
- ... (8 more)

📊 **Current execution:**
These 12 controls are executed 4 SEPARATE TIMES (once per framework) in some cases.

**Example: CTRL_067 (Change Management)**
- Tested for SOX compliance: Quarterly (8 executions)
- Tested for ISO27001: Quarterly (8 executions)
- Tested for PCI-DSS: Quarterly (8 executions)
- **Total: 24 executions for SAME control**

💡 **Consolidation Proposal:**

**Option 1: Single Execution, Multi-Framework Credit**
- Execute CTRL_067 once per quarter (8 executions)
- Credit result to all 3 frameworks (SOX, ISO27001, PCI-DSS)
- **Reduction: 24 → 8 executions (67% reduction)**

**Option 2: Harmonized Control Framework**
- Create "Universal Control" for common requirements
- Map to framework-specific requirements
- Single evidence package satisfies multiple audits

**Projected Impact (All 66 multi-framework controls):**

**Current:**
- Executions: ~15,200 (44% of 34,091)
- Effort: ~15,200 control-hours

**After Consolidation:**
- Executions: ~6,800 (eliminate duplicates)
- Effort: ~6,800 control-hours
- **Savings: 8,400 control-hours (55% reduction)**

💰 **Cost Savings:**
- Control owner time: 8,400 hours × $75/hr = $630K/year
- Evidence collection: $120K/year (automated retrieval once vs 4x)
- **Total savings: $750K/year**

⚠️ **Caveat:**
Must ensure consolidated approach meets each framework's SPECIFIC requirements.
Requires mapping exercise + auditor pre-approval.

🎯 **Recommendation:**
1. Pilot with 12 "All 4 frameworks" controls
2. Get auditor approval for consolidated testing
3. Expand to all 66 multi-framework controls
4. Estimated project cost: $80K (mapping + auditor engagement)
5. **ROI: ($750K - $80K) / $80K = 838%**
```

**✅ Validation :**
- Identification 66 contrôles multi-framework (44%)
- Calcul executions dupliquées
- Proposition consolidation
- ROI quantifié ($750K savings)

---

## 🎓 Guide d'Utilisation

### Séquence de Démo Recommandée

**Phase 1 : Baseline (Q1-Q3)** - 3 min  
Établir état actuel : 69.9% compliance, 57 incidents non résolus

**Phase 2 : Diagnostic (Q4-Q6)** - 4 min  
Identifier gaps : SOX controls failing, incidents 70% non détectés par contrôles

**Phase 3 : Root Cause (Q7-Q9)** - 4 min  
AI extraction : "automation" mentionné 48x, offboarding gap 18 incidents

**Phase 4 : Business Case (Q10-Q12)** - 3 min  
Quantifier : vendor risk, MTTR 58% over target, automation ROI 10,680%

**Phase 5 : Strategic (Q13-Q15)** - (optionnel) 5 min  
Analyses avancées : inverted correlation, risk score validation, framework consolidation

---

## 💡 Tips de Présentation

1. **Commencer avec choc** (Q1 : 69.9% vs 90%) pour capter attention
2. **Montrer convergence multi-sources** (Q7 audit reports + Q8 incidents = automation)
3. **Utiliser Q9 comme "story"** (18 offboarding incidents = human narrative)
4. **Conclure avec ROI** (Q12 : $510K invest → 10,680% ROI)
5. **Q13-Q15 pour audiences executives** (CFO, Board) — strategic optimization

---

**Auteur :** Microsoft Fabric Demo Team  
**Scénario :** L'Audit qui Révèle (Pre-Audit Crisis)  
**Version :** 1.0 - Février 2026
