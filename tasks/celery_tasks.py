"""Celery tasks - Background job processing for cover generation"""

from celery import Celery, Task
from celery.utils.log import get_task_logger
import logging
from config.settings import SAMPLE_RATE
from services.cover_generator import CoverGenerator
import json

logger = get_task_logger(__name__)

# Initialize Celery
celery_app = Celery(
    'raga_remix_studio',
    broker='redis://localhost:6379/0',
    backend='redis://localhost:6379/0'
)

# Celery config
celery_app.conf.update(
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='UTC',
    enable_utc=True,
    task_track_started=True,
    task_time_limit=30 * 60,  # 30 minutes
)


class CallbackTask(Task):
    """Task with progress tracking"""
    
    def on_success(self, retval, task_id, args, kwargs):
        logger.info(f"Task {task_id} succeeded: {retval}")
    
    def on_failure(self, exc, task_id, args, kwargs, einfo):
        logger.error(f"Task {task_id} failed: {exc}")


@celery_app.task(base=CallbackTask, bind=True, track_started=True)
def generate_cover_task(self, job_id: str, config: dict):
    """
    Background task for cover generation
    
    Args:
        job_id: Unique job identifier
        config: Configuration dict with:
            - vocal_file: Path to vocal file
            - instrumental_file: Path to instrumental file
            - processing_mode: 1, 2, or 3
            - target_raga: Raga name (for mode 2)
            - output_path: Where to save result
    """
    try:
        logger.info(f"🎵 Starting cover generation: {job_id}")
        
        # Update task state
        self.update_state(
            state='PROGRESS',
            meta={
                'current': 0,
                'total': 100,
                'status': 'Initializing cover generator...',
                'job_id': job_id
            }
        )
        
        # Initialize cover generator
        cover_gen = CoverGenerator(config)
        
        # Update progress
        self.update_state(
            state='PROGRESS',
            meta={
                'current': 20,
                'total': 100,
                'status': 'Loading audio files...',
                'job_id': job_id
            }
        )
        
        # Load audio files
        vocal_audio = cover_gen.load_audio(config.get('vocal_file'))
        instrumental_audio = cover_gen.load_audio(config.get('instrumental_file'))
        
        # Update progress
        self.update_state(
            state='PROGRESS',
            meta={
                'current': 40,
                'total': 100,
                'status': 'Analyzing and processing...',
                'job_id': job_id
            }
        )
        
        # Generate cover based on mode
        mode = config.get('processing_mode', 1)
        
        if mode == 1:
            result = cover_gen.generate_harmonic_remix(
                vocal_audio,
                instrumental_audio
            )
        elif mode == 2:
            result = cover_gen.generate_raga_fusion(
                vocal_audio,
                instrumental_audio,
                config.get('target_raga', 'Yaman')
            )
        elif mode == 3:
            result = cover_gen.generate_voice_evolution(
                vocal_audio,
                instrumental_audio
            )
        else:
            raise ValueError(f"Invalid processing mode: {mode}")
        
        # Update progress
        self.update_state(
            state='PROGRESS',
            meta={
                'current': 80,
                'total': 100,
                'status': 'Mixing and finalizing...',
                'job_id': job_id
            }
        )
        
        # Save output
        output_path = config.get('output_path', f'outputs/{job_id}_cover.wav')
        cover_gen.save_audio(result, output_path)
        
        # Final progress update
        self.update_state(
            state='PROGRESS',
            meta={
                'current': 100,
                'total': 100,
                'status': 'Completed!',
                'job_id': job_id,
                'output_path': output_path
            }
        )
        
        logger.info(f"✅ Cover generation completed: {job_id}")
        
        return {
            'status': 'success',
            'job_id': job_id,
            'output_path': output_path,
            'message': 'Cover generation completed successfully'
        }
    
    except Exception as e:
        logger.error(f"❌ Cover generation failed: {e}")
        
        self.update_state(
            state='FAILURE',
            meta={
                'current': 0,
                'total': 100,
                'status': f'Error: {str(e)}',
                'job_id': job_id
            }
        )
        
        return {
            'status': 'error',
            'job_id': job_id,
            'error': str(e)
        }


@celery_app.task
def cleanup_old_covers():
    """
    Cleanup task to remove old cover files (runs periodically)
    """
    try:
        import os
        from pathlib import Path
        from datetime import datetime, timedelta
        
        outputs_dir = Path('outputs')
        cutoff_time = datetime.now() - timedelta(days=7)  # Keep 7 days
        
        deleted_count = 0
        for file in outputs_dir.glob('*.wav'):
            file_time = datetime.fromtimestamp(file.stat().st_mtime)
            if file_time < cutoff_time:
                os.remove(file)
                deleted_count += 1
        
        logger.info(f"Cleanup completed: {deleted_count} files deleted")
        
        return {
            'status': 'success',
            'files_deleted': deleted_count
        }
    
    except Exception as e:
        logger.error(f"Cleanup failed: {e}")
        return {
            'status': 'error',
            'error': str(e)
        }


@celery_app.task
def test_celery():
    """Test task to verify Celery is working"""
    logger.info("✅ Celery is working!")
    return {
        'status': 'success',
        'message': 'Celery test task completed'
    }
