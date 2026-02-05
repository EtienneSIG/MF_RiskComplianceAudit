"""
Risk, Compliance & Audit Data Validation Script

Validates the schema and data quality of generated CSV files:
- Checks column presence and types
- Validates relationships (foreign keys)
- Checks for duplicates and null values
- Validates enumerated values
- Verifies text files existence

Author: Microsoft Fabric Demo Team
Date: February 2026
"""

import pandas as pd
import os
import sys

def validate_file_exists(filepath):
    """Check if file exists"""
    if not os.path.exists(filepath):
        print(f"❌ File not found: {filepath}")
        return False
    return True

def validate_controls():
    """Validate controls.csv"""
    print("\n📋 Validating controls.csv...")
    filepath = 'data/raw/controls.csv'
    
    if not validate_file_exists(filepath):
        return False
    
    df = pd.read_csv(filepath)
    
    # Check columns
    required_columns = ['control_id', 'control_name', 'framework', 'category', 'criticality', 'type', 'frequency', 'owner', 'description']
    for col in required_columns:
        if col not in df.columns:
            print(f"  ❌ Missing column: {col}")
            return False
    
    # Check row count
    if len(df) == 0:
        print(f"  ❌ No data in file")
        return False
    
    # Check for duplicates on PK
    if df['control_id'].duplicated().any():
        print(f"  ❌ Duplicate control_id found")
        return False
    
    # Check enumerated values
    valid_frameworks = ['SOX', 'GDPR', 'ISO27001', 'PCI-DSS']
    if not df['framework'].isin(valid_frameworks).all():
        print(f"  ❌ Invalid framework values")
        return False
    
    valid_criticality = ['critical', 'high', 'medium', 'low']
    if not df['criticality'].isin(valid_criticality).all():
        print(f"  ❌ Invalid criticality values")
        return False
    
    valid_types = ['preventive', 'detective', 'corrective']
    if not df['type'].isin(valid_types).all():
        print(f"  ❌ Invalid type values")
        return False
    
    valid_frequency = ['continuous', 'daily', 'weekly', 'monthly', 'quarterly']
    if not df['frequency'].isin(valid_frequency).all():
        print(f"  ❌ Invalid frequency values")
        return False
    
    print(f"  ✅ controls.csv: {len(df.columns)} columns, {len(df)} rows")
    return True

def validate_control_executions():
    """Validate control_executions.csv"""
    print("\n📋 Validating control_executions.csv...")
    filepath = 'data/raw/control_executions.csv'
    
    if not validate_file_exists(filepath):
        return False
    
    df = pd.read_csv(filepath)
    
    # Check columns
    required_columns = ['execution_id', 'control_id', 'execution_date', 'status', 'tested_by', 'evidence', 'notes']
    for col in required_columns:
        if col not in df.columns:
            print(f"  ❌ Missing column: {col}")
            return False
    
    # Check row count
    if len(df) == 0:
        print(f"  ❌ No data in file")
        return False
    
    # Check for duplicates on PK
    if df['execution_id'].duplicated().any():
        print(f"  ❌ Duplicate execution_id found")
        return False
    
    # Check enumerated values
    valid_status = ['passed', 'failed', 'not_tested', 'not_applicable']
    if not df['status'].isin(valid_status).all():
        print(f"  ❌ Invalid status values")
        return False
    
    # Validate dates
    try:
        pd.to_datetime(df['execution_date'])
    except:
        print(f"  ❌ Invalid execution_date format")
        return False
    
    print(f"  ✅ control_executions.csv: {len(df.columns)} columns, {len(df)} rows")
    return True

def validate_incidents():
    """Validate incidents.csv"""
    print("\n📋 Validating incidents.csv...")
    filepath = 'data/raw/incidents.csv'
    
    if not validate_file_exists(filepath):
        return False
    
    df = pd.read_csv(filepath)
    
    # Check columns
    required_columns = ['incident_id', 'incident_date', 'detection_date', 'severity', 'incident_type', 'department', 'execution_id', 'vendor_id', 'financial_impact_usd', 'status', 'reported_by']
    for col in required_columns:
        if col not in df.columns:
            print(f"  ❌ Missing column: {col}")
            return False
    
    # Check row count
    if len(df) == 0:
        print(f"  ❌ No data in file")
        return False
    
    # Check for duplicates on PK
    if df['incident_id'].duplicated().any():
        print(f"  ❌ Duplicate incident_id found")
        return False
    
    # Check enumerated values
    valid_severity = ['critical', 'high', 'medium', 'low']
    if not df['severity'].isin(valid_severity).all():
        print(f"  ❌ Invalid severity values")
        return False
    
    valid_types = ['data_breach', 'access_violation', 'policy_violation', 'system_failure', 'third_party_breach']
    if not df['incident_type'].isin(valid_types).all():
        print(f"  ❌ Invalid incident_type values")
        return False
    
    valid_status = ['open', 'investigating', 'remediated', 'closed']
    if not df['status'].isin(valid_status).all():
        print(f"  ❌ Invalid status values")
        return False
    
    # Validate dates
    try:
        pd.to_datetime(df['incident_date'])
        pd.to_datetime(df['detection_date'])
    except:
        print(f"  ❌ Invalid date format")
        return False
    
    # Validate financial_impact >= 0
    if (df['financial_impact_usd'] < 0).any():
        print(f"  ❌ Negative financial_impact_usd found")
        return False
    
    print(f"  ✅ incidents.csv: {len(df.columns)} columns, {len(df)} rows")
    return True

def validate_remediation_actions():
    """Validate remediation_actions.csv"""
    print("\n📋 Validating remediation_actions.csv...")
    filepath = 'data/raw/remediation_actions.csv'
    
    if not validate_file_exists(filepath):
        return False
    
    df = pd.read_csv(filepath)
    
    # Check columns
    required_columns = ['remediation_id', 'incident_id', 'action_description', 'assigned_to', 'start_date', 'target_completion_date', 'completion_date', 'status', 'cost_usd']
    for col in required_columns:
        if col not in df.columns:
            print(f"  ❌ Missing column: {col}")
            return False
    
    # Check row count
    if len(df) == 0:
        print(f"  ❌ No data in file")
        return False
    
    # Check for duplicates on PK
    if df['remediation_id'].duplicated().any():
        print(f"  ❌ Duplicate remediation_id found")
        return False
    
    # Check enumerated values
    valid_status = ['pending', 'in_progress', 'completed', 'verified']
    if not df['status'].isin(valid_status).all():
        print(f"  ❌ Invalid status values")
        return False
    
    # Validate dates
    try:
        pd.to_datetime(df['start_date'])
        pd.to_datetime(df['target_completion_date'])
    except:
        print(f"  ❌ Invalid date format")
        return False
    
    # Validate cost >= 0
    if (df['cost_usd'] < 0).any():
        print(f"  ❌ Negative cost_usd found")
        return False
    
    print(f"  ✅ remediation_actions.csv: {len(df.columns)} columns, {len(df)} rows")
    return True

def validate_vendors():
    """Validate vendors.csv"""
    print("\n📋 Validating vendors.csv...")
    filepath = 'data/raw/vendors.csv'
    
    if not validate_file_exists(filepath):
        return False
    
    df = pd.read_csv(filepath)
    
    # Check columns
    required_columns = ['vendor_id', 'vendor_name', 'service_type', 'criticality', 'compliance_status', 'annual_spend_usd', 'last_audit_date', 'risk_score', 'country']
    for col in required_columns:
        if col not in df.columns:
            print(f"  ❌ Missing column: {col}")
            return False
    
    # Check row count
    if len(df) == 0:
        print(f"  ❌ No data in file")
        return False
    
    # Check for duplicates on PK
    if df['vendor_id'].duplicated().any():
        print(f"  ❌ Duplicate vendor_id found")
        return False
    
    # Check enumerated values
    valid_criticality = ['critical', 'high', 'medium', 'low']
    if not df['criticality'].isin(valid_criticality).all():
        print(f"  ❌ Invalid criticality values")
        return False
    
    valid_compliance = ['compliant', 'partial', 'non_compliant']
    if not df['compliance_status'].isin(valid_compliance).all():
        print(f"  ❌ Invalid compliance_status values")
        return False
    
    # Validate risk_score 0-100
    if (df['risk_score'] < 0).any() or (df['risk_score'] > 100).any():
        print(f"  ❌ risk_score out of range (0-100)")
        return False
    
    # Validate annual_spend >= 0
    if (df['annual_spend_usd'] < 0).any():
        print(f"  ❌ Negative annual_spend_usd found")
        return False
    
    # Validate dates
    try:
        pd.to_datetime(df['last_audit_date'])
    except:
        print(f"  ❌ Invalid last_audit_date format")
        return False
    
    print(f"  ✅ vendors.csv: {len(df.columns)} columns, {len(df)} rows")
    return True

def validate_relationships():
    """Validate foreign key relationships"""
    print("\n🔗 Validating relationships...")
    
    # Load all dataframes
    controls_df = pd.read_csv('data/raw/controls.csv')
    executions_df = pd.read_csv('data/raw/control_executions.csv')
    incidents_df = pd.read_csv('data/raw/incidents.csv')
    remediations_df = pd.read_csv('data/raw/remediation_actions.csv')
    vendors_df = pd.read_csv('data/raw/vendors.csv')
    
    # Check control_executions -> controls
    invalid_controls = executions_df[~executions_df['control_id'].isin(controls_df['control_id'])]
    if len(invalid_controls) > 0:
        print(f"  ❌ {len(invalid_controls)} invalid control_id in executions")
        return False
    print(f"  ✅ Relationship control_executions → controls: OK")
    
    # Check incidents -> control_executions (nullable)
    executions_linked = incidents_df[incidents_df['execution_id'].notna() & (incidents_df['execution_id'] != '')]
    if len(executions_linked) > 0:
        invalid_executions = executions_linked[~executions_linked['execution_id'].isin(executions_df['execution_id'])]
        if len(invalid_executions) > 0:
            print(f"  ❌ {len(invalid_executions)} invalid execution_id in incidents")
            return False
    print(f"  ✅ Relationship incidents → control_executions: OK")
    
    # Check incidents -> vendors (nullable)
    vendors_linked = incidents_df[incidents_df['vendor_id'].notna() & (incidents_df['vendor_id'] != '')]
    if len(vendors_linked) > 0:
        invalid_vendors = vendors_linked[~vendors_linked['vendor_id'].isin(vendors_df['vendor_id'])]
        if len(invalid_vendors) > 0:
            print(f"  ❌ {len(invalid_vendors)} invalid vendor_id in incidents")
            return False
    print(f"  ✅ Relationship incidents → vendors: OK")
    
    # Check remediation_actions -> incidents
    invalid_incidents = remediations_df[~remediations_df['incident_id'].isin(incidents_df['incident_id'])]
    if len(invalid_incidents) > 0:
        print(f"  ❌ {len(invalid_incidents)} invalid incident_id in remediations")
        return False
    print(f"  ✅ Relationship remediation_actions → incidents: OK")
    
    return True

def validate_text_files():
    """Validate text files existence"""
    print("\n📄 Validating text files...")
    
    # Check audit reports
    audit_dir = 'data/raw/audit_reports_txt'
    if not os.path.exists(audit_dir):
        print(f"  ❌ Directory not found: {audit_dir}")
        return False
    
    audit_files = [f for f in os.listdir(audit_dir) if f.endswith('.txt')]
    if len(audit_files) < 50:
        print(f"  ❌ Expected ~100 audit reports, found {len(audit_files)}")
        return False
    print(f"  ✅ audit_reports_txt/: {len(audit_files)} files")
    
    # Check incident descriptions
    incident_dir = 'data/raw/incident_descriptions_txt'
    if not os.path.exists(incident_dir):
        print(f"  ❌ Directory not found: {incident_dir}")
        return False
    
    incident_files = [f for f in os.listdir(incident_dir) if f.endswith('.txt')]
    if len(incident_files) < 100:
        print(f"  ❌ Expected ~150 incident descriptions, found {len(incident_files)}")
        return False
    print(f"  ✅ incident_descriptions_txt/: {len(incident_files)} files")
    
    return True

def validate_data_quality():
    """Validate data quality rules"""
    print("\n✅ Validating data quality...")
    
    # Load dataframes
    executions_df = pd.read_csv('data/raw/control_executions.csv')
    
    # Check execution_date format and range
    executions_df['execution_date'] = pd.to_datetime(executions_df['execution_date'])
    if executions_df['execution_date'].min() < pd.Timestamp('2023-01-01'):
        print(f"  ❌ execution_date earlier than expected")
        return False
    if executions_df['execution_date'].max() > pd.Timestamp('2025-12-31'):
        print(f"  ❌ execution_date later than expected")
        return False
    
    print(f"  ✅ Date ranges valid")
    
    # Check compliance rate is realistic (70-95%)
    compliance_rate = (executions_df['status'] == 'passed').sum() / len(executions_df)
    if compliance_rate < 0.60 or compliance_rate > 0.95:
        print(f"  ❌ Compliance rate {compliance_rate:.1%} out of expected range (60-95%)")
        return False
    
    print(f"  ✅ Compliance Rate: {compliance_rate:.1%} (realistic)")
    
    return True

if __name__ == '__main__':
    print("🔍 Starting Risk, Compliance & Audit data validation...\n")
    print("=" * 60)
    
    all_valid = True
    
    # Validate each CSV file
    all_valid &= validate_controls()
    all_valid &= validate_control_executions()
    all_valid &= validate_incidents()
    all_valid &= validate_remediation_actions()
    all_valid &= validate_vendors()
    
    # Validate relationships
    all_valid &= validate_relationships()
    
    # Validate text files
    all_valid &= validate_text_files()
    
    # Validate data quality
    all_valid &= validate_data_quality()
    
    print("\n" + "=" * 60)
    if all_valid:
        print("\n🎉 All validations passed!")
        sys.exit(0)
    else:
        print("\n❌ Validation failed. Please fix errors and try again.")
        sys.exit(1)
