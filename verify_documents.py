#!/usr/bin/env python3
import os
import re

def check_document(filepath, expected_sections):
    """Verify document contains expected sections"""
    with open(filepath, 'r') as f:
        content = f.read()
    
    missing_sections = []
    for section in expected_sections:
        if section not in content:
            missing_sections.append(section)
    
    # Check for Mermaid diagrams
    has_mermaid = '```mermaid' in content
    
    return {
        'exists': os.path.exists(filepath),
        'has_mermaid': has_mermaid,
        'missing_sections': missing_sections,
        'length': len(content.split('\n'))
    }

def main():
    documents = {
        'output/exec_review.md': [
            'Executive Summary',
            'System Overview', 
            'High-Level Architecture',
            'External Dependencies',
            'Critical & High Risk Areas',
            'System Complexity'
        ],
        'output/architect_review.md': [
            'System Overview',
            'Repository & Component Map',
            'Architecture & Dependencies',
            'Execution Flows',
            'Data Flow & State Model',
            'Configuration & Environment Model',
            'Deployment & Runtime Topology',
            'Architectural Risk Observations'
        ],
        'output/developer_review.md': [
            'How to Think About This System',
            'Codebase Mental Model',
            'Entry Points & Lifecycles',
            'Key Modules Explained',
            'Module Interactions & Dependencies',
            'Configuration & Runtime Behavior',
            'Developer Guidelines & Pitfalls',
            'Suggested Reading Order'
        ]
    }
    
    print("Document Verification Results")
    print("=" * 50)
    
    all_good = True
    for filepath, sections in documents.items():
        result = check_document(filepath, sections)
        print(f"\n{filepath}:")
        print(f"  ✓ Exists: {result['exists']}")
        print(f"  ✓ Has Mermaid diagrams: {result['has_mermaid']}")
        print(f"  ✓ Length: {result['length']} lines")
        
        if result['missing_sections']:
            print(f"  ✗ Missing sections: {result['missing_sections']}")
            all_good = False
        else:
            print(f"  ✓ All required sections present")
    
    print(f"\nOverall Status: {'✓ PASS' if all_good else '✗ FAIL'}")
    return 0 if all_good else 1

if __name__ == '__main__':
    exit(main())
