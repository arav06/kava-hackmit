#!/usr/bin/env python3
"""
Test script to verify the enhanced progressive validation system works correctly
"""

import sys
import os
sys.path.append('backend')

from dotenv import load_dotenv
from services.ai_judge import AIJudge
from models.claim import ClaimPacket, Document, DocumentType
from datetime import datetime
import json

# Load environment variables
load_dotenv('.env')

def test_progressive_validation():
    print("🧪 Testing Enhanced Progressive Validation System...")
    
    # Initialize AI Judge
    judge = AIJudge()
    
    # Create test claims for different scenarios
    
    # SCENARIO 1: High-quality claim (should stop at iteration 1)
    print("\n" + "="*70)
    print("🎯 SCENARIO 1: High-Quality Claim (Expected: Early approval)")
    print("="*70)
    
    high_quality_claim = ClaimPacket(
        claim_id="test_high_quality",
        policy_number="PREMIUM-POL-12345",
        claimant_name="Premium Customer",
        incident_date=datetime(2024, 10, 15),  # Recent incident
        property_address="123 Premium Street, Fire Zone, CA 90210",
        documents=[
            Document(
                id="hq_fire_report",
                filename="official_fire_department_report.pdf",
                document_type=DocumentType.DAMAGE_REPORT,
                extracted_data={
                    "document_type": "fire_report",
                    "agency": "Cal Fire Department",
                    "incident_details": "Confirmed wildfire damage - total loss",
                    "damage_assessment": "Complete structural loss",
                    "official_determination": "Wildfire causation confirmed"
                },
                confidence_score=0.95,
                file_size=500000,
                upload_timestamp=datetime.now()
            ),
            Document(
                id="hq_photos",
                filename="damage_photos_before_after.jpg",
                document_type=DocumentType.PHOTO,
                extracted_data={
                    "damage_type": "severe fire damage",
                    "severity": "total loss",
                    "wildfire_evidence": "charring, ash, structural collapse",
                    "before_after": "comprehensive photo documentation"
                },
                confidence_score=0.92,
                file_size=3000000,
                upload_timestamp=datetime.now()
            ),
            Document(
                id="hq_policy",
                filename="insurance_policy_active.pdf", 
                document_type=DocumentType.POLICY,
                extracted_data={
                    "policy_number": "PREMIUM-POL-12345",
                    "coverage_amount": 500000,
                    "effective_date": "2024-01-01",
                    "wildfire_coverage": "included"
                },
                confidence_score=0.98,
                file_size=200000,
                upload_timestamp=datetime.now()
            )
        ],
        estimated_damage=250000.00,
        created_at=datetime.now()
    )
    
    # Test high-quality claim progression
    test_claim_progression(judge, high_quality_claim, "HIGH_QUALITY")
    
    # SCENARIO 2: Medium-quality claim (should improve with iterations)
    print("\n" + "="*70)
    print("🎯 SCENARIO 2: Medium-Quality Claim (Expected: Progressive improvement)")
    print("="*70)
    
    medium_quality_claim = ClaimPacket(
        claim_id="test_medium_quality",
        policy_number="STANDARD-POL-67890",
        claimant_name="Standard Customer",
        incident_date=datetime(2024, 8, 20),  # Older incident
        property_address="456 Standard Ave, Suburban, CA 90211",
        documents=[
            Document(
                id="mq_basic_report",
                filename="basic_fire_report.pdf",
                document_type=DocumentType.DAMAGE_REPORT,
                extracted_data={
                    "document_type": "incident_report",
                    "damage_type": "fire damage",
                    "severity": "moderate"
                },
                confidence_score=0.75,
                file_size=100000,
                upload_timestamp=datetime.now()
            ),
            Document(
                id="mq_receipt",
                filename="home_depot_receipt.pdf",
                document_type=DocumentType.RECEIPT,
                extracted_data={
                    "merchant": "Home Depot",
                    "total_amount": 2500.00,
                    "date": "2024-08-25",
                    "items": ["Emergency supplies", "Tarps"]
                },
                confidence_score=0.80,
                file_size=50000,
                upload_timestamp=datetime.now()
            )
        ],
        estimated_damage=75000.00,
        created_at=datetime.now()
    )
    
    # Test medium-quality claim progression
    test_claim_progression(judge, medium_quality_claim, "MEDIUM_QUALITY")

def test_claim_progression(judge, claim_packet, scenario_name):
    """Test a claim through the progressive validation system"""
    
    print(f"📋 Testing {scenario_name} claim: {claim_packet.claim_id}")
    print(f"💰 Estimated Damage: ${claim_packet.estimated_damage:,.2f}")
    print(f"📄 Initial Documents: {len(claim_packet.documents)}")
    
    previous_scores = []
    
    try:
        import asyncio
        
        # Test each iteration depth
        for iteration in range(1, 5):
            print(f"\n🔍 Testing Iteration {iteration}...")
            
            validation = asyncio.run(judge.evaluate_with_depth(claim_packet, iteration, previous_scores))
            
            current_score = validation.overall_score
            improvement = (current_score - previous_scores[-1]) if previous_scores else 0
            
            print(f"📊 Score: {current_score:.1%}")
            print(f"📈 Improvement: {improvement:+.1%}" if previous_scores else "📈 Initial Score")
            print(f"🔍 Analysis Depth: {judge._get_depth_name(iteration)}")
            print(f"✅ Approved: {validation.approved}")
            print(f"⚠️ Missing Docs: {len(validation.missing_documents)}")
            print(f"🚨 Fraud Indicators: {len(validation.fraud_indicators)}")
            
            # Simulate the exit conditions from the actual validation loop
            if iteration == 1 and current_score >= 0.8:
                print("🎉 EARLY APPROVAL: Score ≥80% on first iteration!")
                break
            elif iteration == 2 and improvement < 0.05 and current_score >= 0.7:
                print("✅ Sufficient score after enhancement, stopping.")
                break
            elif iteration == 3 and improvement < 0.02 and current_score >= 0.6:
                print("✅ Acceptable score after forensic analysis.")
                break
            elif iteration >= 4:
                print("⚖️ Expert review complete - final assessment.")
                break
                
            previous_scores.append(current_score)
            
        print(f"\n✅ {scenario_name} VALIDATION COMPLETE")
        print(f"🏁 Final Score: {current_score:.1%}")
        print(f"🔄 Iterations Used: {iteration}")
        total_improvement = (current_score - previous_scores[0]) if previous_scores else 0
        print(f"📈 Total Improvement: {total_improvement:+.1%}")
        
        return True
        
    except Exception as e:
        print(f"❌ Test failed for {scenario_name}: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_progressive_validation()
    print(f"\n{'✅ PROGRESSIVE VALIDATION TEST PASSED' if success else '❌ TEST FAILED'}")
    sys.exit(0 if success else 1)
