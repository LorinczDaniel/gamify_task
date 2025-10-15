"""
Database Backup Script
Run this daily to prevent data loss
"""
import shutil
import os
from datetime import datetime

# Create backups directory if it doesn't exist
if not os.path.exists('backups'):
    os.makedirs('backups')

# Create timestamped backup
timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
source = 'quest_master.db'
destination = f'backups/quest_master_backup_{timestamp}.db'

try:
    shutil.copy2(source, destination)
    print(f"✓ Database backed up to: {destination}")
    
    # Keep only last 10 backups
    backups = sorted([f for f in os.listdir('backups') if f.startswith('quest_master_backup_')])
    if len(backups) > 10:
        for old_backup in backups[:-10]:
            os.remove(os.path.join('backups', old_backup))
            print(f"  Removed old backup: {old_backup}")
    
    print(f"\n✓ Total backups: {min(len(backups), 10)}")
except Exception as e:
    print(f"✗ Backup failed: {e}")



