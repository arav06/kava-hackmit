#!/usr/bin/env python3
"""
Quick test script to verify AI Judge is working correctly
"""

import sys
import os
sys.path.append('backend')

from dotenv import load_dotenv
from services.ai_judge import AIJudge
from models.claim import ClaimPacket, Document, DocumentType
from datetime import datetime

# Load environment variables
load_dotenv('.env')

def test_ai_judge():
    print("🧪 Testing AI Judge setup...")
    
    # Initialize AI Judge
    judge = AIJudge()
    
    # Create a simple test claim
    test_claim = ClaimPacket(
        claim_id="test_001",
        policy_number="TEST-POL-123",
        claimant_name="Test Claimant",
        incident_date=datetime(2024, 8, 15),
        property_address="123 Test Street, Anytown, CA 90210",
        documents=[
            Document(
                id="test_photo_1",
                filename="damage_photo.jpg",
                document_type=DocumentType.PHOTO,
                extracted_data={
                    "damage_type": "fire damage",
                    "severity": "moderate",
                    "location": "living room"
                },
                confidence_score=0.85,
                file_size=2048000,
                upload_timestamp=datetime.now()
            ),
            Document(
                id="test_receipt_1", 
                filename="home_depot_receipt.pdf",
                document_type=DocumentType.RECEIPT,
                extracted_data={
                    "merchant": "Home Depot",
                    "total_amount": 1250.00,
                    "date": "2024-08-20",
                    "items": ["Fire extinguisher", "Emergency supplies", "Tarps"]
                },
                confidence_score=0.92,
                file_size=156000,
                upload_timestamp=datetime.now()
            )
        ],
        estimated_damage=25000.00,
        created_at=datetime.now()
    )
    
    print("✅ Test claim packet created")
    print(f"📋 Claim ID: {test_claim.claim_id}")
    print(f"📋 Documents: {len(test_claim.documents)}")
    print(f"📋 Estimated Damage: ${test_claim.estimated_damage:,.2f}")
    
    # Test the AI Judge evaluation
    print("\n🤖 Running AI Judge evaluation...")
    
    try:
        import asyncio
        validation = asyncio.run(judge.evaluate_claim(test_claim))
        
        print("✅ AI Judge evaluation completed!")
        print(f"📊 Overall Score: {validation.overall_score:.2%}")
        print(f"🔍 Confidence: {validation.confidence:.2%}")
        print(f"✅ Approved: {validation.approved}")
        print(f"📝 Rules Evaluated: {len(validation.rules_evaluated)}")
        print(f"⚠️ Missing Documents: {len(validation.missing_documents)}")
        print(f"🚨 Fraud Indicators: {len(validation.fraud_indicators)}")
        print(f"💬 Rationale: {validation.rationale[:200]}...")
        
        if validation.overall_score > 0.0 and validation.overall_score < 1.0:
            print("✅ AI Judge is working correctly - dynamic scoring detected!")
            return True
        else:
            print("❌ AI Judge may be using fallback scoring")
            return False
            
    except Exception as e:
        print(f"❌ AI Judge evaluation failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_ai_judge()
    print(f"\n{'✅ Test PASSED' if success else '❌ Test FAILED'}")
    sys.exit(0 if success else 1)
