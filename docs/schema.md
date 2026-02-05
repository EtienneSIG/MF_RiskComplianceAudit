# 📊 Schéma de Données - Risk, Compliance & Audit Analytics

## Vue d'ensemble

Ce projet contient **5 tables CSV** et **2 dossiers de fichiers texte** pour l'analyse risque, conformité et audit.

**Période couverte :** 2023-01-01 à 2025-01-01 (24 mois)  
**Frameworks :** SOX, GDPR, ISO27001, PCI-DSS  
**Contrôles :** 149 contrôles répartis sur 4 frameworks

---

## 📋 Tables CSV

### 1. controls.csv

**Description :** Catalogue des contrôles de conformité selon les différents frameworks réglementaires.

| Colonne | Type | Description | Exemple |
|---------|------|-------------|---------|
| `control_id` | string | Identifiant unique du contrôle (format: CTRL_XXX) | `CTRL_042` |
| `control_name` | string | Nom du contrôle | `Access Review - Quarterly` |
| `framework` | enum | Framework réglementaire | `SOX`, `GDPR`, `ISO27001`, `PCI-DSS` |
| `control_type` | enum | Type de contrôle | `preventive`, `detective`, `corrective` |
| `criticality` | enum | Niveau de criticité | `critical`, `high`, `medium`, `low` |
| `frequency` | enum | Fréquence d'exécution requise | `daily`, `weekly`, `monthly`, `quarterly`, `annual` |
| `owner` | string | Responsable du contrôle | `John Smith (IT Security)` |

**Clé primaire :** `control_id`  
**Volume :** 149 lignes

**Règles métier :**
- Distribution frameworks : SOX 30%, GDPR 25%, ISO27001 30%, PCI-DSS 15%
- Distribution types : Preventive 50%, Detective 35%, Corrective 15%
- Distribution criticality : Critical 20%, High 35%, Medium 30%, Low 15%
- Fréquence selon criticality : Critical → Daily/Weekly, Low → Quarterly/Annual

---

### 2. control_executions.csv

**Description :** Historique d'exécution des contrôles avec résultats et observations.

| Colonne | Type | Description | Exemple |
|---------|------|-------------|---------|
| `execution_id` | string | Identifiant unique de l'exécution (format: EXEC_XXXXXXXX) | `EXEC_00012345` |
| `control_id` | string | Contrôle exécuté (FK → controls) | `CTRL_042` |
| `execution_date` | date | Date d'exécution du contrôle | `2024-06-15` |
| `status` | enum | Résultat de l'exécution | `passed`, `failed`, `not_tested`, `exception` |
| `findings` | string | Observations/anomalies détectées | `2 users with expired access` |
| `performed_by` | string | Auditeur/exécutant | `Sarah Chen` |

**Clé primaire :** `execution_id`  
**Clé étrangère :** `control_id` → controls.control_id  
**Volume :** ~34,091 lignes (24 mois d'historique)

**Règles métier :**
- Distribution status : Passed 70%, Failed 20%, Not_tested 8%, Exception 2%
- Exécutions planifiées selon `controls.frequency`
- Daily controls : ~730 exécutions (24 mois)
- Quarterly controls : ~8 exécutions (24 mois)
- `findings` renseigné uniquement si `status = failed` ou `exception`

---

### 3. incidents.csv

**Description :** Incidents de sécurité/conformité détectés, liés ou non à des échecs de contrôles.

| Colonne | Type | Description | Exemple |
|---------|------|-------------|---------|
| `incident_id` | string | Identifiant unique de l'incident (format: INC_XXXXXXXX) | `INC_00001234` |
| `execution_id` | string | Exécution contrôle liée (FK → control_executions, nullable) | `EXEC_00012345` |
| `incident_type` | enum | Type d'incident | `data_breach`, `access_violation`, `policy_violation`, `system_failure`, `third_party_breach` |
| `severity` | enum | Gravité de l'incident | `critical`, `high`, `medium`, `low` |
| `detection_date` | date | Date de détection | `2024-06-16` |
| `status` | enum | Statut de gestion | `open`, `investigating`, `contained`, `resolved`, `closed` |
| `assigned_to` | string | Responsable investigation | `Michael Zhang (Compliance)` |
| `vendor_id` | string | Vendor impliqué (FK → vendors, nullable) | `VND_042` |

**Clé primaire :** `incident_id`  
**Clés étrangères :**  
- `execution_id` → control_executions.execution_id (nullable - 30% liés)  
- `vendor_id` → vendors.vendor_id (nullable - 40% liés)

**Volume :** 200 lignes

**Règles métier :**
- Distribution types : Data_breach 15%, Access_violation 25%, Policy_violation 30%, System_failure 20%, Third_party_breach 10%
- Distribution severity : Critical 20%, High 35%, Medium 30%, Low 15%
- 30% des incidents liés à un échec de contrôle (execution_id renseigné)
- 40% des incidents impliquent un vendor tiers

---

### 4. remediation_actions.csv

**Description :** Actions correctives mises en œuvre suite aux incidents.

| Colonne | Type | Description | Exemple |
|---------|------|-------------|---------|
| `remediation_id` | string | Identifiant unique de l'action (format: REM_XXXXXXXX) | `REM_00001234` |
| `incident_id` | string | Incident traité (FK → incidents) | `INC_00001234` |
| `action_type` | enum | Type d'action corrective | `process_improvement`, `system_patch`, `access_revocation`, `policy_update`, `training` |
| `description` | string | Description de l'action | `Revoke access for 2 users, update access review process` |
| `start_date` | date | Date de début de l'action | `2024-06-17` |
| `due_date` | date | Date d'échéance | `2024-06-24` |
| `completion_date` | date | Date effective de clôture | `2024-06-22` |
| `status` | enum | Statut de l'action | `planned`, `in_progress`, `completed`, `overdue` |
| `owner` | string | Responsable de l'action | `IT Security Team` |

**Clé primaire :** `remediation_id`  
**Clé étrangère :** `incident_id` → incidents.incident_id  
**Volume :** ~186 lignes (93% des incidents ont au moins une action)

**Règles métier :**
- Distribution types : Process_improvement 30%, System_patch 25%, Access_revocation 20%, Policy_update 15%, Training 10%
- MTTR (Mean Time To Remediate) : Critical 3-7 jours, Low 14-30 jours
- 80% des actions complétées avant due_date (status = completed)
- 10% des actions overdue

---

### 5. vendors.csv

**Description :** Fournisseurs tiers avec évaluation de risque et compliance.

| Colonne | Type | Description | Exemple |
|---------|------|-------------|---------|
| `vendor_id` | string | Identifiant unique du vendor (format: VND_XXX) | `VND_042` |
| `vendor_name` | string | Nom du fournisseur | `CloudStorage Inc.` |
| `service_category` | enum | Catégorie de service | `Cloud Storage`, `Payment Processing`, `HR Systems`, `Security Tools`, `Data Analytics` |
| `risk_score` | float | Score de risque (0-100) | `72.5` |
| `last_audit_date` | date | Date du dernier audit | `2024-03-15` |
| `compliance_status` | enum | Statut de conformité | `compliant`, `non_compliant`, `pending_review` |
| `certifications` | string | Certifications détenues | `ISO27001, SOC2` |

**Clé primaire :** `vendor_id`  
**Volume :** 100 lignes

**Règles métier :**
- Distribution services : Cloud_Storage 25%, Payment_Processing 20%, HR_Systems 15%, Security_Tools 20%, Data_Analytics 20%
- Risk score calculé : `Criticality×40% + Compliance_Gap×30% + Audit_Age×30%`
- Distribution compliance : Compliant 60%, Non_compliant 25%, Pending_review 15%
- Last_audit_date : 0-365 jours depuis aujourd'hui

---

## 📄 Fichiers Texte (Non-Structurés)

### 6. audit_reports_txt/

**Description :** Rapports d'audit détaillés rédigés par les auditeurs internes/externes.

**Format :** Fichiers .txt nommés `audit_report_CTRL_XXX_YYYYMMDD.txt`

**Contenu typique :**
```
Control ID: CTRL_042
Control Name: Access Review - Quarterly
Framework: SOX
Audit Date: 2024-06-15
Auditor: Sarah Chen

FINDINGS:
- 2 users (john.doe, jane.smith) have access rights expired 30+ days ago
- Access review process not followed for Q1 2024
- Documentation incomplete for 5 access modifications

RISK LEVEL: High

RECOMMENDATIONS:
1. Immediate revocation of expired access
2. Implement automated alert for expiring access (15 days before)
3. Update access review checklist with mandatory documentation fields

COMPLIANCE IMPACT: SOX 404 control deficiency identified
```

**Volume :** 100 fichiers texte  
**Utilisation :** Extraction d'insights via AI Shortcut dans Data Agent

---

### 7. incident_descriptions_txt/

**Description :** Descriptions narratives détaillées des incidents de sécurité/conformité.

**Format :** Fichiers .txt nommés `incident_INC_XXXXXXXX_YYYYMMDD.txt`

**Contenu typique :**
```
Incident ID: INC_00001234
Type: Access Violation
Severity: High
Detection Date: 2024-06-16

DESCRIPTION:
An automated control execution (EXEC_00012345) detected that two user accounts 
(john.doe and jane.smith) had active system access despite employment termination 
30+ days ago. This represents a significant access control violation.

IMPACT:
- Potential unauthorized access to customer data (GDPR concern)
- SOX control failure (access provisioning/deprovisioning)
- 2 accounts with elevated privileges to production systems

IMMEDIATE ACTIONS TAKEN:
1. Access revoked for both accounts within 2 hours of detection
2. Audit log review initiated (no suspicious activity found)
3. HR-IT notification process reviewed

ROOT CAUSE:
Offboarding workflow does not include automated trigger to IT Security for 
access revocation. Manual email notification was missed due to high HR turnover.

REMEDIATION:
- Action REM_00001234: Implement automated API integration HR→IT Security
- Action REM_00001235: Quarterly reconciliation of HR termination list vs Active Directory
```

**Volume :** 150 fichiers texte (75% des incidents ont description détaillée)  
**Utilisation :** AI analysis pour root cause patterns, impact assessment

---

## 🔗 Relations entre Tables

```
controls (1) ←─── (N) control_executions
                         │
                         │ (1)
                         ↓
                         (N) incidents
                                │
                                │ (1)
                                ↓
                                (N) remediation_actions

vendors (1) ←─── (N) incidents
```

**Cardinalités :**
- 1 control → N executions (fréquence : daily=730, quarterly=8 sur 24 mois)
- 1 execution → 0..N incidents (30% des échecs génèrent incident)
- 1 incident → 1..N remediation_actions (moyenne : 1.5 actions/incident)
- 1 vendor → 0..N incidents (40% incidents impliquent vendor)

---

## 📈 Métriques Clés Calculables

### Compliance Rate
```
Compliance Rate = (Passed Executions / Total Executions) × 100%
```
Target : >90%

### Incident Response Time (IRT)
```
IRT = AVG(Incident Resolved Date - Detection Date) in hours
```
Target : Critical <24h, High <72h, Medium <7 days

### Mean Time To Remediate (MTTR)
```
MTTR = AVG(Completion Date - Start Date) for remediation actions
```
Target : <7 days

### Vendor Risk Score
```
Risk Score = Criticality×40% + Compliance_Gap×30% + Audit_Age×30%
```
Range : 0-100 (100 = highest risk)

### Control Effectiveness
```
Effectiveness = (Failed Executions Detecting Incidents / Total Failed Executions) × 100%
```
Target : >80% (contrôles détectent bien les incidents)

### Audit Coverage
```
Coverage = (Controls Tested in Period / Total Controls) × 100%
```
Target : 100% (tous contrôles testés selon fréquence)

---

## 🎯 Cas d'Usage Data Agent

1. **Compliance Dashboard :** "Quel est le taux de conformité global ?"
2. **Incident Analysis :** "Quels sont les 5 types d'incidents les plus fréquents ?"
3. **Vendor Risk :** "Quels vendors ont un risk_score >70 ?"
4. **Audit Findings :** "Extraire les recommandations des audit reports pour SOX controls"
5. **Remediation Tracking :** "Combien d'actions correctives sont overdue ?"
6. **Framework Performance :** "Comparer compliance rate entre SOX, GDPR, ISO27001, PCI-DSS"
7. **Root Cause Patterns :** "Analyser incident descriptions pour identifier root causes récurrentes"

---

## 📦 Déploiement

1. **Lakehouse** : Charger les 5 CSV dans tables Bronze
2. **Transformation** : Bronze → Silver (nettoyage, typage, calcul métriques)
3. **Semantic Model** : Créer relations entre tables
4. **AI Shortcut** : Pointer vers audit_reports_txt/ et incident_descriptions_txt/
5. **Data Agent** : Configurer avec instructions métier (voir data_agent_instructions.md)

---

**Auteur :** Microsoft Fabric Demo Team  
**Version :** 1.0  
**Date :** Février 2026
