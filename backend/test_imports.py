#!/usr/bin/env python3
"""
Test script to verify that all imports work correctly
"""

try:
    print("Testing imports...")
    
    # Test basic imports
    from fastapi import FastAPI
    print("✓ FastAPI import successful")
    
    # Test our modules
    from auth.schemas import UserIn, Token
    from documents.schemas import Document
    print("✓ Models import successful")
    
    from auth.database import users_db
    from documents.database import documents_db
    print("✓ Database import successful")
    
    from auth.security import get_password_hash, verify_password, create_access_token, get_user, get_current_user
    print("✓ Auth security import successful")
    
    from auth.router import router as auth_router
    print("✓ Auth router import successful")
    
    from documents.router import router as doc_router
    print("✓ Documents router import successful")
    
    # Test main app
    from main import app
    print("✓ Main app import successful")
    
    print("\n🎉 All imports successful! The server should start without issues.")
    
except ImportError as e:
    print(f"❌ Import error: {e}")
    import traceback
    traceback.print_exc()
except Exception as e:
    print(f"❌ Unexpected error: {e}")
    import traceback
    traceback.print_exc() 