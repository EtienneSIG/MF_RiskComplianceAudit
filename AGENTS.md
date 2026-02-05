# Conventions de Développement - Risk, Compliance & Audit

## 🎯 Objectif

Ce document définit les **conventions de développement** pour le projet Risk, Compliance & Audit avec Microsoft Fabric Data Agent.

---

## 📋 Conventions de Nommage

### Identifiants

| Entité | Format | Exemple | Description |
|--------|--------|---------|-------------|
| **Control** | `CTRL_XXX` | `CTRL_001` | Identifiant unique du contrôle |
| **Execution** | `EXEC_XXXXXXXX` | `EXEC_00001234` | Identifiant unique d'exécution |
| **Incident** | `INC_XXXXXXXX` | `INC_00005678` | Identifiant unique d'incident |
| **Remediation** | `REM_XXXXXXXX` | `REM_00001234` | Identifiant unique de remédiation |
| **Vendor** | `VND_XXX` | `VND_001` | Identifiant unique du fournisseur |

### Fichiers Texte

**Audit Reports** :
```
audit_report_CTRL_XXX_YYYYMMDD.txt
```
Exemple : `audit_report_CTRL_045_20250115.txt`

**Incident Descriptions** :
```
incident_INC_XXXXXXXX_YYYYMMDD.txt
```
Exemple : `incident_INC_00001234_20250120.txt`

---

## 🏢 Contexte Métier

### Frameworks de Conformité

Le système couvre 4 frameworks réglementaires principaux :

1. **SOX (Sarbanes-Oxley)** : Conformité financière
   - Contrôles sur le reporting financier
   - Séparation des pouvoirs (segregation of duties)
   - Audit trail des transactions

2. **GDPR (General Data Protection Regulation)** : Protection des données
   - Consentement utilisateur
   - Droit à l'oubli
   - Sécurité des données personnelles

3. **ISO 27001** : Sécurité de l'information
   - Gestion des risques IT
   - Politiques de sécurité
   - Contrôle d'accès

4. **PCI-DSS (Payment Card Industry)** : Sécurité des paiements
   - Cryptage des données de carte
   - Tests de sécurité réseau
   - Gestion des vulnérabilités

### Types de Contrôles

| Type | Description | Fréquence Typique |
|------|-------------|-------------------|
| **Preventive** | Empêche les incidents | Continue |
| **Detective** | Détecte les incidents | Quotidienne |
| **Corrective** | Corrige après incident | Ad-hoc |

### Criticité des Contrôles

| Criticité | Impact | Exemple |
|-----------|--------|---------|
| **Critical** | Risque majeur, non-conformité grave | Séparation des pouvoirs financiers |
| **High** | Risque significatif | Gestion des accès privilégiés |
| **Medium** | Risque modéré | Revue des logs d'accès |
| **Low** | Risque mineur | Documentation des procédures |

### Statuts d'Exécution

| Statut | Description | Action Requise |
|--------|-------------|----------------|
| **passed** | Contrôle réussi | Aucune |
| **failed** | Contrôle échoué | Remédiation urgente |
| **not_tested** | Non testé | Planifier test |
| **not_applicable** | Non applicable | Documentation |

### Sévérité des Incidents

| Sévérité | Impact | Exemple |
|----------|--------|---------|
| **critical** | Impact business majeur, perte financière > $100K | Fuite de données clients |
| **high** | Impact significatif, perte < $100K | Accès non autorisé à système critique |
| **medium** | Impact modéré | Violation mineure de politique |
| **low** | Impact minimal | Documentation manquante |

### Risque Fournisseurs (Risk Scoring)

**Formule de calcul** :
```
Risk Score = (Criticality × 40%) + (Compliance Gap × 30%) + (Last Audit Age × 30%)

Où :
- Criticality : critical=100, high=70, medium=40, low=20
- Compliance Gap : non_compliant=100, partial=50, compliant=0
- Last Audit Age : > 12 mois = 100, 6-12 mois = 50, < 6 mois = 0
```

**Catégories de risque** :
- **Low (0-39)** : Risque acceptable, monitoring standard
- **Medium (40-69)** : Risque modéré, revue trimestrielle
- **High (70-100)** : Risque élevé, action immédiate requise

---

## 📊 Métriques et KPIs

### Conformité

```dax
Compliance Rate = 
DIVIDE(
    [Controls Passed],
    [Total Controls Executed],
    0
)
```

**Benchmark** : > 95%

### MTTR (Mean Time To Remediate)

```dax
MTTR = 
AVERAGE(
    DATEDIFF(
        incidents[detection_date],
        remediation_actions[completion_date],
        DAY
    )
)
```

**Benchmark** : 
- Critical : < 24h
- High : < 7 jours
- Medium : < 30 jours

### Vendor Risk Exposure

```dax
High Risk Vendor Exposure = 
SUMX(
    FILTER(vendors, vendors[risk_score] >= 70),
    vendors[annual_spend_usd]
)
```

---

## 🧪 Procédures de Validation

### 1. Validation Schéma

Avant de déployer dans Fabric :

```bash
python src/validate_schema.py
```

**Checks effectués** :
- ✅ Colonnes requises présentes
- ✅ Types de données corrects
- ✅ Relations FK valides
- ✅ Pas de doublons sur PK
- ✅ Valeurs énumérées correctes (status, severity, etc.)

### 2. Validation Relations

**Relations clés** :
```
controls (1) ──< control_executions (N)
    control_id = control_id

control_executions (1) ──< incidents (0..1)
    execution_id = execution_id

incidents (1) ──< remediation_actions (0..N)
    incident_id = incident_id

vendors (1) ──< incidents (0..N)
    vendor_id = vendor_id
```

### 3. Validation Métriques

**Tests unitaires sur mesures DAX** :

```dax
// Test : Compliance Rate doit être entre 0-100%
Test_Compliance_Rate = 
VAR Rate = [Compliance Rate]
RETURN
    IF(Rate >= 0 && Rate <= 1, "PASS", "FAIL")
```

---

## 🔒 Sécurité et Conformité

### PII (Personal Identifiable Information)

Les données synthétiques **ne contiennent pas de vraies PII** :
- Noms : Générés par Faker (fictifs)
- Emails : `user_{id}@example.com` (non réels)
- Adresses : Générées aléatoirement

### AI Transformations - Redaction PII

Lors de l'upload dans Fabric, configurer **AI Skills** pour :
- Détecter et masquer emails, numéros de téléphone
- Anonymiser noms de personnes dans rapports d'audit
- Redacter informations sensibles (numéros de carte, SSN)

---

## 📁 Structure des Données

### CSV Files

**Encoding** : UTF-8  
**Separator** : `,` (virgule)  
**Date Format** : `YYYY-MM-DD`  
**Datetime Format** : `YYYY-MM-DD HH:MM:SS`

### Text Files

**Format Audit Report** :
```
Control ID: CTRL_XXX
Audit Date: YYYY-MM-DD
Framework: SOX/GDPR/ISO27001/PCI-DSS
Auditor: [Name]

Findings:
[Liste des findings]

Recommendations:
[Liste des recommandations]

Status: Compliant / Non-Compliant / Partial
```

**Format Incident Description** :
```
Incident ID: INC_XXXXXXXX
Date: YYYY-MM-DD HH:MM:SS
Severity: critical/high/medium/low
Type: data_breach/access_violation/policy_violation/system_failure

Description:
[Texte détaillé de l'incident]

Impact:
[Impact business et financier]

Root Cause:
[Cause racine identifiée]
```

---

## 🎯 Exemples de Données

### Control

```csv
control_id,control_name,framework,category,criticality,type,frequency,owner
CTRL_001,Segregation of Duties - Finance,SOX,financial,critical,preventive,continuous,Finance
CTRL_002,GDPR Consent Management,GDPR,privacy,high,detective,daily,Legal
CTRL_003,Access Control Review,ISO27001,security,high,detective,weekly,IT Security
```

### Control Execution

```csv
execution_id,control_id,execution_date,status,tested_by,evidence,notes
EXEC_00001,CTRL_001,2025-01-15,passed,Alice Smith,SOD_report_Q1.pdf,All segregation rules enforced
EXEC_00002,CTRL_002,2025-01-16,failed,Bob Johnson,consent_log_Jan.csv,50 consents missing documentation
```

### Incident

```csv
incident_id,incident_date,detection_date,severity,incident_type,department,execution_id,vendor_id,financial_impact_usd,status
INC_00001,2025-01-20,2025-01-20,critical,data_breach,IT,EXEC_00002,,150000,open
INC_00002,2025-01-22,2025-01-23,high,access_violation,Finance,,VND_045,5000,remediated
```

---

## 📝 Bonnes Pratiques

### Génération de Données

1. **Seed fixe** : Utiliser `seed=42` pour reproductibilité
2. **Cohérence temporelle** : Dates d'exécution >= création contrôle
3. **Réalisme** : Taux de conformité ~88-92% (réaliste)
4. **Distribution** : 
   - 70% controls passed
   - 20% failed
   - 10% not_tested

### AI Transformations

1. **Prompts clairs** : Spécifier exactement les champs à extraire
2. **Validation** : Toujours valider les outputs AI
3. **Fallback** : Prévoir des valeurs par défaut si extraction échoue

### DAX Measures

1. **Gestion des BLANK()** : Toujours utiliser `DIVIDE(..., 0)` ou `COALESCE`
2. **Filtrage contexte** : Utiliser `CALCULATE` pour changer le contexte
3. **Performance** : Éviter `FILTER(ALL(...))` sur grandes tables

---

## 🚀 Déploiement

### Checklist Pré-Déploiement

- [ ] Données générées et validées (`validate_schema.py` → exit 0)
- [ ] Fichiers texte encodés UTF-8
- [ ] Relations définies dans Semantic Model
- [ ] Mesures DAX testées (pas de BLANK() inattendu)
- [ ] Data Agent configuré avec instructions
- [ ] 5 questions test validées

### Checklist Post-Déploiement

- [ ] Delta Tables créées (5 tables)
- [ ] AI Transformations appliquées (audit reports, incidents)
- [ ] Semantic Model publié
- [ ] Data Agent répond correctement aux questions test
- [ ] Compliance Rate ~90% (valeur attendue)

---

## 📞 Support

Pour questions techniques :
- Consulter [docs/fabric_setup.md](docs/fabric_setup.md)
- Vérifier [docs/schema.md](docs/schema.md) pour structure données

---

*Conventions de développement Risk, Compliance & Audit | Dernière mise à jour : Février 2026*
