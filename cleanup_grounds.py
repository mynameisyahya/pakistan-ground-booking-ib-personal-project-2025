#!/usr/bin/env python3
"""
Script to clean up junk/test grounds from the database
"""
from app import app, db, Ground

def cleanup_grounds():
    with app.app_context():
        # Get all grounds ordered by ID
        grounds = Ground.query.order_by(Ground.id).all()
        
        print("Current grounds in database:")
        for i, ground in enumerate(grounds, 1):
            print(f"{i}. ID: {ground.id}, Name: '{ground.name}', Location: '{ground.location}', Host: {ground.host_email}")
        
        if len(grounds) <= 5:
            print(f"\nOnly {len(grounds)} grounds found. Skipping deletion to avoid removing all grounds.")
            return
        
        # Delete the first 5 grounds (top 5 by ID)
        grounds_to_delete = grounds[:5]
        
        print(f"\nDeleting top 5 grounds:")
        for ground in grounds_to_delete:
            print(f"- Deleting: ID {ground.id}, '{ground.name}' in {ground.location}")
            db.session.delete(ground)
        
        # Commit the changes
        db.session.commit()
        print(f"\n✅ Successfully deleted {len(grounds_to_delete)} grounds!")
        
        # Show remaining grounds
        remaining_grounds = Ground.query.order_by(Ground.id).all()
        print(f"\nRemaining {len(remaining_grounds)} grounds:")
        for i, ground in enumerate(remaining_grounds, 1):
            print(f"{i}. ID: {ground.id}, Name: '{ground.name}', Location: '{ground.location}'")

if __name__ == "__main__":
    cleanup_grounds()
