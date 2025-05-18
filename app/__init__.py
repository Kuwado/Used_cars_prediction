"""Main Flask application configuration."""
from flask import Flask
import os
import logging
from datetime import datetime

def create_app(test_config=None):
    """Create and configure the Flask application."""
    app = Flask(__name__, instance_relative_config=True)
    
    # Set up configuration
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'car_price.sqlite'),
        UPLOAD_FOLDER=os.path.join('data', 'raw'),
        PROCESSED_FOLDER=os.path.join('data', 'processed'),
    )
    
    if test_config is None:
        # Load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # Load the test config if passed in
        app.config.from_mapping(test_config)
    
    # Ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    
    # Ensure data folders exist
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    os.makedirs(app.config['PROCESSED_FOLDER'], exist_ok=True)
    
    # Configure logging
    logging_dir = os.path.join(os.getcwd(), 'logs')
    os.makedirs(logging_dir, exist_ok=True)
    
    log_file = os.path.join(logging_dir, 'app.log')
    logging.basicConfig(
        filename=log_file,
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Configure database
    from app.utils.database import configure_db
    db = configure_db(app)
    
    # Register blueprints
    from app.routes import main_bp
    app.register_blueprint(main_bp)
    
    # Set attribute on app to track first request
    app.first_request_processed = False
    
    # Define first request handler
    @app.before_request
    def handle_first_request():
        if not getattr(app, 'first_request_processed', False):
            # Check if today is the first day of month
            today = datetime.now()
            if today.day == 18:
                # Execute monthly crawl
                try:
                    from app.utils.crawler import schedule_monthly_crawl
                    schedule_monthly_crawl()
                    app.logger.info("Monthly crawl scheduled on first day of month")
                except Exception as e:
                    app.logger.error(f"Error scheduling monthly crawl: {str(e)}")
            
            # Mark first request as processed
            app.first_request_processed = True
            app.logger.info("First request processed")
    
    # Add a function to check crawler status
    def check_crawler_status():
        """Check the status of running crawl jobs."""
        from app.models import CrawlLog
        with app.app_context():
            # Get all running crawler jobs
            running_jobs = CrawlLog.query.filter_by(status='running').all()
            for job in running_jobs:
                # Check if job has been running for more than 1 hour without updates
                time_diff = datetime.now() - job.start_time
                if time_diff.total_seconds() > 3600:  # 1 hour
                    # Update job status
                    job.status = 'failed'
                    job.error_message = 'Job timed out after 1 hour'
                    job.end_time = datetime.now()
                    db.session.commit()
                    app.logger.warning(f"Crawler job {job.id} marked as failed due to timeout")
    
    # Run status check when app starts
    with app.app_context():
        check_crawler_status()
        app.logger.info("Application initialized")
    
    return app