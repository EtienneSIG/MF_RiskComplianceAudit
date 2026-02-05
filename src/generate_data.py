"""
Risk, Compliance & Audit Data Generator

Generates synthetic data for Microsoft Fabric demo:
- controls.csv
- control_executions.csv
- incidents.csv
- remediation_actions.csv
- vendors.csv
- audit_reports_txt/*.txt
- incident_descriptions_txt/*.txt

Author: Microsoft Fabric Demo Team
Date: February 2026
"""

import pandas as pd
import numpy as np
from faker import Faker
from datetime import datetime, timedelta
import yaml
import os
import random

# Load configuration
with open('src/config.yaml', 'r', encoding='utf-8') as f:
    config = yaml.safe_load(f)

# Set seed for reproducibility
seed = config['seed']
np.random.seed(seed)
random.seed(seed)
Faker.seed(seed)
fake = Faker()

# Parse dates
start_date = datetime.strptime(config['start_date'], '%Y-%m-%d')
end_date = datetime.strptime(config['end_date'], '%Y-%m-%d')

# Create output directory
os.makedirs('data/raw/audit_reports_txt', exist_ok=True)
os.makedirs('data/raw/incident_descriptions_txt', exist_ok=True)


def weighted_choice(choices, weights):
    """Helper to make weighted random choice"""
    return random.choices(choices, weights=weights, k=1)[0]


def generate_controls():
    """Generate controls.csv"""
    controls = []
    control_id = 1
    
    for framework_config in config['control_frameworks']:
        framework = framework_config['name']
        num_controls = int(config['controls']['count'] * framework_config['percentage'] / 100)
        
        for _ in range(num_controls):
            # Determine criticality
            criticality = weighted_choice(
                ['critical', 'high', 'medium', 'low'],
                [config['control_criticality'][k] for k in ['critical', 'high', 'medium', 'low']]
            )
            
            # Determine type
            control_type = weighted_choice(
                ['preventive', 'detective', 'corrective'],
                [config['control_types'][k] for k in ['preventive', 'detective', 'corrective']]
            )
            
            # Determine frequency
            frequency = weighted_choice(
                ['continuous', 'daily', 'weekly', 'monthly', 'quarterly'],
                [config['control_frequencies'][k] for k in ['continuous', 'daily', 'weekly', 'monthly', 'quarterly']]
            )
            
            # Determine category
            category = random.choice(framework_config['categories'])
            
            # Determine owner department
            department = random.choice(config['departments'])
            owner = random.choice(config['control_owners'].get(department, ['Manager']))
            
            # Generate control name
            control_names = {
                'SOX': ['Segregation of Duties', 'Financial Reporting Controls', 'Revenue Recognition', 'Expense Approval', 'Journal Entry Review'],
                'GDPR': ['Consent Management', 'Data Subject Rights', 'Data Breach Notification', 'Privacy Impact Assessment', 'Data Retention'],
                'ISO27001': ['Access Control', 'Incident Management', 'Vulnerability Management', 'Backup Procedures', 'Security Awareness'],
                'PCI-DSS': ['Cardholder Data Encryption', 'Network Segmentation', 'Penetration Testing', 'Key Management', 'Physical Security']
            }
            base_name = random.choice(control_names[framework])
            control_name = f"{base_name} - {category.replace('_', ' ').title()}"
            
            controls.append({
                'control_id': f'CTRL_{control_id:03d}',
                'control_name': control_name,
                'framework': framework,
                'category': category,
                'criticality': criticality,
                'type': control_type,
                'frequency': frequency,
                'owner': f"{department} - {owner}",
                'description': f"{framework} control for {category} compliance - {control_type} control executed {frequency}"
            })
            control_id += 1
    
    df = pd.DataFrame(controls)
    df.to_csv('data/raw/controls.csv', index=False, encoding='utf-8')
    print(f"✅ Generated {len(df)} controls")
    return df


def generate_control_executions(controls_df):
    """Generate control_executions.csv"""
    executions = []
    execution_id = 1
    
    # Generate executions for each control over 24 months
    for _, control in controls_df.iterrows():
        control_id = control['control_id']
        frequency = control['frequency']
        
        # Determine execution frequency
        freq_days = {
            'continuous': 1,
            'daily': 1,
            'weekly': 7,
            'monthly': 30,
            'quarterly': 90
        }
        interval = freq_days[frequency]
        
        # Generate executions
        current_date = start_date
        while current_date <= end_date:
            # Determine status
            status = weighted_choice(
                ['passed', 'failed', 'not_tested', 'not_applicable'],
                [config['execution_status'][k] for k in ['passed', 'failed', 'not_tested', 'not_applicable']]
            )
            
            # Select tester
            tested_by = random.choice(config['auditors'])
            
            # Generate evidence
            evidence_types = ['report', 'screenshot', 'log_file', 'checklist', 'attestation']
            evidence = f"{random.choice(evidence_types)}_{control_id}_{current_date.strftime('%Y%m%d')}.pdf"
            
            # Generate notes
            notes_templates = {
                'passed': [
                    'All checks completed successfully',
                    'Control operating effectively',
                    'No exceptions identified',
                    'Compliance verified'
                ],
                'failed': [
                    'Exception identified - requires remediation',
                    'Control not operating as designed',
                    'Non-compliance detected',
                    'Significant deficiency found'
                ],
                'not_tested': [
                    'Testing postponed due to resource constraints',
                    'System unavailable for testing',
                    'Scheduled for next period'
                ],
                'not_applicable': [
                    'Control not applicable for this period',
                    'System not in scope',
                    'Process not active'
                ]
            }
            notes = random.choice(notes_templates[status])
            
            executions.append({
                'execution_id': f'EXEC_{execution_id:08d}',
                'control_id': control_id,
                'execution_date': current_date.strftime('%Y-%m-%d'),
                'status': status,
                'tested_by': tested_by,
                'evidence': evidence if status != 'not_tested' else '',
                'notes': notes
            })
            
            execution_id += 1
            current_date += timedelta(days=interval)
    
    df = pd.DataFrame(executions)
    df.to_csv('data/raw/control_executions.csv', index=False, encoding='utf-8')
    print(f"✅ Generated {len(df)} control executions")
    return df


def generate_incidents(executions_df, vendors_df):
    """Generate incidents.csv"""
    incidents = []
    
    # Get valid execution IDs  
    valid_execution_ids = executions_df['execution_id'].unique().tolist()
    
    # Generate incidents (some from failed controls, some standalone)
    num_incidents = config['incidents']['count']
    
    for i in range(num_incidents):
        incident_id = f'INC_{i+1:08d}'
        
        # Determine severity
        severity = weighted_choice(
            ['critical', 'high', 'medium', 'low'],
            [config['incident_severity'][k] for k in ['critical', 'high', 'medium', 'low']]
        )
        
        # Determine type
        incident_type_config = weighted_choice(
            config['incident_types'],
            [t['percentage'] for t in config['incident_types']]
        )
        incident_type = incident_type_config['name']
        
        # Generate dates
        incident_date = start_date + timedelta(days=random.randint(0, (end_date - start_date).days))
        detection_delay = random.randint(0, 3)  # days
        detection_date = incident_date + timedelta(days=detection_delay)
        
        # Link to execution (30% of incidents)
        execution_id = ''
        if random.random() < 0.3 and len(valid_execution_ids) > 0:
            execution_id = random.choice(valid_execution_ids)
        
        # Link to vendor (for third_party_breach)
        vendor_id = ''
        if incident_type == 'third_party_breach' and len(vendors_df) > 0:
            vendor_id = vendors_df.sample(1).iloc[0]['vendor_id']
        
        # Determine department
        department = random.choice(config['departments'])
        
        # Financial impact
        base_impact = incident_type_config['avg_financial_impact']
        financial_impact = int(base_impact * random.uniform(0.5, 2.0))
        
        # Status
        status = weighted_choice(
            ['open', 'investigating', 'remediated', 'closed'],
            [config['incident_status'][k] for k in ['open', 'investigating', 'remediated', 'closed']]
        )
        
        # Reported by
        reported_by = random.choice(config['auditors'])
        
        incidents.append({
            'incident_id': incident_id,
            'incident_date': incident_date.strftime('%Y-%m-%d %H:%M:%S'),
            'detection_date': detection_date.strftime('%Y-%m-%d %H:%M:%S'),
            'severity': severity,
            'incident_type': incident_type,
            'department': department,
            'execution_id': execution_id,
            'vendor_id': vendor_id,
            'financial_impact_usd': financial_impact,
            'status': status,
            'reported_by': reported_by
        })
    
    df = pd.DataFrame(incidents)
    df.to_csv('data/raw/incidents.csv', index=False, encoding='utf-8')
    print(f"✅ Generated {len(df)} incidents")
    return df


def generate_remediation_actions(incidents_df):
    """Generate remediation_actions.csv"""
    remediations = []
    remediation_id = 1
    
    # Generate remediation for ~90% of incidents
    for _, incident in incidents_df.iterrows():
        if random.random() < config['remediation_actions']['per_incident']:
            incident_id = incident['incident_id']
            severity = incident['severity']
            
            # Start date (1-7 days after detection)
            detection_date = datetime.strptime(incident['detection_date'], '%Y-%m-%d %H:%M:%S')
            start_date_rem = detection_date + timedelta(days=random.randint(1, 7))
            
            # MTTR based on severity
            mttr = config['remediation_mttr'][severity]
            completion_days = int(mttr * random.uniform(0.7, 1.5))
            
            # Status
            status = weighted_choice(
                ['pending', 'in_progress', 'completed', 'verified'],
                [config['remediation_status'][k] for k in ['pending', 'in_progress', 'completed', 'verified']]
            )
            
            # Completion date (if completed/verified)
            completion_date = ''
            if status in ['completed', 'verified']:
                completion_date = (start_date_rem + timedelta(days=completion_days)).strftime('%Y-%m-%d')
            
            # Assigned to
            assigned_to = random.choice(config['auditors'])
            
            # Action description
            action_templates = {
                'data_breach': ['Revoke compromised credentials', 'Notify affected parties', 'Strengthen encryption', 'Implement DLP'],
                'access_violation': ['Revoke unauthorized access', 'Review access controls', 'Update RBAC policies', 'User training'],
                'policy_violation': ['Update policy documentation', 'Conduct training', 'Implement monitoring', 'Enforce penalties'],
                'system_failure': ['Patch system', 'Restore from backup', 'Upgrade infrastructure', 'Implement redundancy'],
                'third_party_breach': ['Review vendor contract', 'Conduct vendor audit', 'Implement additional controls', 'Terminate relationship']
            }
            action = random.choice(action_templates[incident['incident_type']])
            
            # Cost
            cost = int(incident['financial_impact_usd'] * random.uniform(0.1, 0.3))
            
            remediations.append({
                'remediation_id': f'REM_{remediation_id:08d}',
                'incident_id': incident_id,
                'action_description': action,
                'assigned_to': assigned_to,
                'start_date': start_date_rem.strftime('%Y-%m-%d'),
                'target_completion_date': (start_date_rem + timedelta(days=mttr)).strftime('%Y-%m-%d'),
                'completion_date': completion_date,
                'status': status,
                'cost_usd': cost
            })
            remediation_id += 1
    
    df = pd.DataFrame(remediations)
    df.to_csv('data/raw/remediation_actions.csv', index=False, encoding='utf-8')
    print(f"✅ Generated {len(df)} remediation actions")
    return df


def generate_vendors():
    """Generate vendors.csv"""
    vendors = []
    
    for i in range(config['vendors']['count']):
        vendor_id = f'VND_{i+1:03d}'
        
        # Vendor name
        vendor_name = fake.company()
        
        # Criticality
        criticality = weighted_choice(
            ['critical', 'high', 'medium', 'low'],
            [config['vendor_criticality'][k] for k in ['critical', 'high', 'medium', 'low']]
        )
        
        # Compliance status
        compliance_status = weighted_choice(
            ['compliant', 'partial', 'non_compliant'],
            [config['vendor_compliance_status'][k] for k in ['compliant', 'partial', 'non_compliant']]
        )
        
        # Annual spend
        spend_range = config['vendor_annual_spend_ranges'][criticality]
        annual_spend = random.randint(spend_range[0], spend_range[1])
        
        # Last audit
        months_since_audit = random.randint(
            config['vendor_last_audit_months']['min'],
            config['vendor_last_audit_months']['max']
        )
        last_audit_date = end_date - timedelta(days=months_since_audit * 30)
        
        # Calculate risk score
        # Risk Score = (Criticality × 40%) + (Compliance Gap × 30%) + (Last Audit Age × 30%)
        criticality_score = {'critical': 100, 'high': 70, 'medium': 40, 'low': 20}[criticality]
        compliance_score = {'non_compliant': 100, 'partial': 50, 'compliant': 0}[compliance_status]
        audit_age_score = 100 if months_since_audit > 12 else (50 if months_since_audit > 6 else 0)
        
        risk_score = int(
            criticality_score * 0.4 +
            compliance_score * 0.3 +
            audit_age_score * 0.3
        )
        
        # Service type
        service_types = ['IT Services', 'Cloud Provider', 'Data Processing', 'Payment Processor', 'Logistics', 'HR Services']
        service_type = random.choice(service_types)
        
        # Country
        country = random.choice(['USA', 'UK', 'France', 'Germany', 'India', 'Singapore'])
        
        vendors.append({
            'vendor_id': vendor_id,
            'vendor_name': vendor_name,
            'service_type': service_type,
            'criticality': criticality,
            'compliance_status': compliance_status,
            'annual_spend_usd': annual_spend,
            'last_audit_date': last_audit_date.strftime('%Y-%m-%d'),
            'risk_score': risk_score,
            'country': country
        })
    
    df = pd.DataFrame(vendors)
    df.to_csv('data/raw/vendors.csv', index=False, encoding='utf-8')
    print(f"✅ Generated {len(df)} vendors")
    return df


def generate_audit_reports(controls_df):
    """Generate audit_reports_txt/*.txt"""
    num_reports = config['audit_reports']['count']
    
    # Select random controls for audit
    audited_controls = controls_df.sample(n=num_reports)
    
    for _, control in audited_controls.iterrows():
        control_id = control['control_id']
        framework = control['framework']
        
        # Audit date (random date in range)
        audit_date = start_date + timedelta(days=random.randint(0, (end_date - start_date).days))
        
        # Auditor
        auditor = random.choice(config['auditors'])
        
        # Findings
        num_findings = random.randint(0, 5)
        findings = []
        for i in range(num_findings):
            finding_templates = [
                f"Control execution frequency not aligned with policy ({control['frequency']} vs expected daily)",
                f"Evidence documentation incomplete for {random.randint(1, 10)} instances",
                f"Segregation of duties violation detected in {random.randint(1, 5)} cases",
                f"Missing approvals for {random.randint(1, 8)} control activities",
                f"System access logs not reviewed for {random.randint(1, 15)} days"
            ]
            findings.append(f"- {random.choice(finding_templates)}")
        
        # Recommendations
        num_recommendations = random.randint(1, 4)
        recommendations = []
        for i in range(num_recommendations):
            rec_templates = [
                "Update control documentation to reflect current process",
                "Implement automated monitoring for continuous compliance",
                "Provide additional training to control owners",
                "Strengthen segregation of duties controls",
                "Enhance evidence collection and retention procedures"
            ]
            recommendations.append(f"- {random.choice(rec_templates)}")
        
        # Status
        status = 'Compliant' if len(findings) == 0 else ('Partial' if len(findings) <= 2 else 'Non-Compliant')
        
        # Generate report
        report = f"""Control ID: {control_id}
Control Name: {control['control_name']}
Audit Date: {audit_date.strftime('%Y-%m-%d')}
Framework: {framework}
Auditor: {auditor}

FINDINGS:
"""
        if len(findings) > 0:
            report += '\n'.join(findings)
        else:
            report += "- No findings identified. Control operating effectively."
        
        report += f"""

RECOMMENDATIONS:
"""
        report += '\n'.join(recommendations)
        
        report += f"""

STATUS: {status}

CONCLUSION:
"""
        if status == 'Compliant':
            report += f"The control {control_id} is operating effectively and meets {framework} compliance requirements."
        elif status == 'Partial':
            report += f"The control {control_id} requires minor improvements to fully comply with {framework} standards."
        else:
            report += f"The control {control_id} has significant deficiencies and requires immediate remediation to meet {framework} requirements."
        
        # Save to file
        filename = f"data/raw/audit_reports_txt/audit_report_{control_id}_{audit_date.strftime('%Y%m%d')}.txt"
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(report)
    
    print(f"✅ Generated {num_reports} audit reports")


def generate_incident_descriptions(incidents_df):
    """Generate incident_descriptions_txt/*.txt"""
    num_descriptions = config['incident_descriptions']['count']
    
    # Select random incidents for detailed description
    described_incidents = incidents_df.sample(n=min(num_descriptions, len(incidents_df)))
    
    for _, incident in described_incidents.iterrows():
        incident_id = incident['incident_id']
        severity = incident['severity']
        incident_type = incident['incident_type']
        incident_date = incident['incident_date']
        
        # Description templates
        descriptions = {
            'data_breach': f"""On {incident_date}, a data breach was detected in the {incident['department']} department. Unauthorized access was gained to customer databases containing personally identifiable information (PII). The breach was discovered during routine security monitoring when anomalous access patterns were detected. Initial investigation suggests the breach occurred due to compromised employee credentials. Approximately {random.randint(100, 10000)} customer records may have been exposed.""",
            
            'access_violation': f"""An access violation was identified on {incident_date} when user {fake.name()} attempted to access restricted financial systems without proper authorization. The incident was flagged by the access control system and immediately blocked. Review of access logs indicates this may be part of a pattern of unauthorized access attempts. The user's account has been temporarily suspended pending investigation.""",
            
            'policy_violation': f"""A policy violation was reported on {incident_date} regarding non-compliance with {random.choice(['GDPR data retention', 'SOX documentation', 'ISO27001 security', 'PCI-DSS encryption'])} requirements. The violation was discovered during a routine audit by {incident['reported_by']}. The {incident['department']} department failed to follow established procedures for {random.choice(['data classification', 'change management', 'incident reporting', 'access reviews'])}.""",
            
            'system_failure': f"""A critical system failure occurred on {incident_date} affecting {random.choice(['production database', 'authentication service', 'payment gateway', 'email server', 'file storage'])}. The outage lasted approximately {random.randint(1, 8)} hours and impacted {random.randint(10, 500)} users. Root cause analysis indicates the failure was due to {random.choice(['hardware malfunction', 'software bug', 'network outage', 'configuration error', 'capacity overload'])}. Business continuity plans were activated to minimize impact.""",
            
            'third_party_breach': f"""A security breach at vendor {fake.company()} was reported on {incident_date}. The vendor notified us that their systems were compromised, potentially exposing data shared with them as part of our business operations. The vendor provides {random.choice(['cloud services', 'payment processing', 'data analytics', 'customer support', 'logistics'])} and has access to {random.choice(['customer data', 'financial records', 'employee information', 'intellectual property'])}. We have initiated our third-party incident response procedures."""
        }
        
        description = descriptions[incident_type]
        
        # Impact assessment
        impact = f"""

IMPACT ASSESSMENT:
- Financial Impact: ${incident['financial_impact_usd']:,} USD
- Severity Level: {severity.upper()}
- Affected Department: {incident['department']}
- Potential Regulatory Implications: {random.choice(['GDPR Article 33 breach notification required', 'SOX Section 404 control deficiency', 'PCI-DSS non-compliance penalty', 'ISO27001 certification at risk', 'None identified'])}
"""
        
        # Root cause
        root_causes = [
            "Insufficient access controls and authentication mechanisms",
            "Lack of employee security awareness training",
            "Outdated software with known vulnerabilities",
            "Inadequate vendor due diligence procedures",
            "Missing or ineffective monitoring and alerting",
            "Failure to follow change management procedures",
            "Inadequate segregation of duties",
            "Human error in system configuration"
        ]
        root_cause = f"""

ROOT CAUSE:
{random.choice(root_causes)}

IMMEDIATE ACTIONS TAKEN:
- Incident response team activated
- Affected systems isolated
- Senior management notified
- Forensic investigation initiated
- Legal and compliance teams engaged
"""
        
        # Full description
        full_description = f"""Incident ID: {incident_id}
Date: {incident_date}
Severity: {severity}
Type: {incident_type}

DESCRIPTION:
{description}
{impact}
{root_cause}
"""
        
        # Save to file
        filename = f"data/raw/incident_descriptions_txt/incident_{incident_id}_{datetime.strptime(incident_date, '%Y-%m-%d %H:%M:%S').strftime('%Y%m%d')}.txt"
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(full_description)
    
    print(f"✅ Generated {len(described_incidents)} incident descriptions")


if __name__ == '__main__':
    print("🚀 Starting Risk, Compliance & Audit data generation...\n")
    
    # Generate vendors first (needed for incidents)
    vendors_df = generate_vendors()
    
    # Generate controls
    controls_df = generate_controls()
    
    # Generate control executions
    executions_df = generate_control_executions(controls_df)
    
    # Generate incidents
    incidents_df = generate_incidents(executions_df, vendors_df)
    
    # Generate remediation actions
    remediation_df = generate_remediation_actions(incidents_df)
    
    # Generate text files
    generate_audit_reports(controls_df)
    generate_incident_descriptions(incidents_df)
    
    print("\n✅ All data generated successfully!")
    print(f"\n📊 Summary:")
    print(f"   - Controls: {len(controls_df)}")
    print(f"   - Executions: {len(executions_df)}")
    print(f"   - Incidents: {len(incidents_df)}")
    print(f"   - Remediations: {len(remediation_df)}")
    print(f"   - Vendors: {len(vendors_df)}")
    print(f"   - Audit Reports: {config['audit_reports']['count']}")
    print(f"   - Incident Descriptions: {config['incident_descriptions']['count']}")
    print(f"\n💾 Data saved to: data/raw/")
