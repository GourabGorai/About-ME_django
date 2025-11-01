"""
Management command to migrate media files to static directory for production
"""
import os
import shutil
from django.core.management.base import BaseCommand
from django.conf import settings


class Command(BaseCommand):
    help = 'Migrate media files to static directory for production deployment'

    def handle(self, *args, **options):
        media_root = settings.MEDIA_ROOT
        static_media_dir = os.path.join(settings.BASE_DIR, 'static', 'media')
        
        # Create static/media directory if it doesn't exist
        os.makedirs(static_media_dir, exist_ok=True)
        
        if os.path.exists(media_root) and os.listdir(media_root):
            self.stdout.write(f"Migrating media files from {media_root} to {static_media_dir}")
            
            # Copy all files from media to static/media
            for root, dirs, files in os.walk(media_root):
                for file in files:
                    src_path = os.path.join(root, file)
                    # Calculate relative path from media root
                    rel_path = os.path.relpath(src_path, media_root)
                    dst_path = os.path.join(static_media_dir, rel_path)
                    
                    # Create destination directory if it doesn't exist
                    os.makedirs(os.path.dirname(dst_path), exist_ok=True)
                    
                    # Copy file
                    shutil.copy2(src_path, dst_path)
                    self.stdout.write(f"Copied: {rel_path}")
            
            self.stdout.write(
                self.style.SUCCESS(
                    f'Successfully migrated media files to {static_media_dir}'
                )
            )
        else:
            self.stdout.write(
                self.style.WARNING('No media files found to migrate')
            )