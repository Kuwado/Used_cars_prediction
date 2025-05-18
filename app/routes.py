"""Flask routes and views."""
from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, current_app, copy_current_request_context
from app.utils.crawler import run_crawler, get_latest_raw_file, check_stuck_crawlers
from app.utils.preprocessor import run_preprocessing
from app.utils.database import db, import_data_to_db
from app.models import CrawlLog, ProcessingLog, Brand, Model
from datetime import datetime
import os
import threading
import concurrent.futures
import time

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    """Home page view."""
    # Get statistics for display
    brand_count = Brand.query.count()
    model_count = Model.query.count()
    
    # Get latest crawl and processing logs
    latest_crawl = CrawlLog.query.order_by(CrawlLog.start_time.desc()).first()
    latest_processing = ProcessingLog.query.order_by(ProcessingLog.start_time.desc()).first()
    
    # Auto-check for stuck crawlers
    check_stuck_crawlers()
    
    return render_template('index.html', 
                           brand_count=brand_count,
                           model_count=model_count,
                           latest_crawl=latest_crawl,
                           latest_processing=latest_processing)

@main_bp.route('/crawl', methods=['POST'])
def crawl():
    """Start a crawling job."""
    # Get parameters
    start_page = int(request.form.get('start_page', 1))
    end_page = int(request.form.get('end_page', 5))
    
    # Create a new crawl log entry
    crawl_log = CrawlLog(
        source='chotot',
        status='running'
    )
    db.session.add(crawl_log)
    db.session.commit()
    
    # Store the log ID, not the object itself
    log_id = crawl_log.id
    
    # Calculate timeout (5 minutes per page plus 1 minute buffer)
    timeout = (page_count := (end_page - start_page + 1)) * 300 + 60
    
    # Get a reference to the app for the background thread
    app = current_app._get_current_object()
    
    # Start crawling in a thread with timeout monitoring
    def run_with_timeout():
        # Create app context for the thread
        with app.app_context():
            try:
                # Create a ThreadPoolExecutor for timeout control
                with concurrent.futures.ThreadPoolExecutor() as executor:
                    # Submit the task to be executed with log_id (not the object)
                    future = executor.submit(run_crawler, start_page, end_page, log_id)
                    
                    try:
                        # Wait for the future to complete with timeout
                        result = future.result(timeout=timeout)
                        
                        # If crawler doesn't update status, update it here
                        # Get a fresh instance of the log
                        updated_log = CrawlLog.query.get(log_id)
                        if updated_log and updated_log.status.startswith('running'):
                            updated_log.status = 'completed'
                            updated_log.end_time = datetime.now()
                            db.session.commit()
                            app.logger.info(f"Crawler job {log_id} completed by timeout monitor")
                            
                    except concurrent.futures.TimeoutError:
                        # Handle timeout - get a fresh instance
                        updated_log = CrawlLog.query.get(log_id)
                        if updated_log:
                            updated_log.status = 'failed'
                            updated_log.error_message = f'Timeout after {timeout} seconds'
                            updated_log.end_time = datetime.now()
                            db.session.commit()
                            app.logger.error(f"Crawler job {log_id} timed out after {timeout} seconds")
                    
            except Exception as e:
                # Handle exceptions in the thread - get a fresh instance
                app.logger.error(f"Error in crawler thread: {str(e)}")
                updated_log = CrawlLog.query.get(log_id)
                if updated_log:
                    updated_log.status = 'failed'
                    updated_log.error_message = str(e)
                    updated_log.end_time = datetime.now()
                    db.session.commit()
    
    # Start the crawl thread
    crawl_thread = threading.Thread(target=run_with_timeout)
    crawl_thread.daemon = True
    crawl_thread.start()
    
    flash('Crawling job started successfully! Check the logs for progress.', 'success')
    return redirect(url_for('main.index'))

@main_bp.route('/preprocess', methods=['POST'])
def preprocess():
    """Start a preprocessing job."""
    # Get the latest raw file
    latest_file = get_latest_raw_file()
    
    if not latest_file:
        flash('No raw data files found. Please run a crawler first.', 'error')
        return redirect(url_for('main.index'))
    
    # Create a new processing log entry
    processing_log = ProcessingLog(
        input_file=latest_file,
        status='running'
    )
    db.session.add(processing_log)
    db.session.commit()
    
    # Store the log ID, not the object
    log_id = processing_log.id
    
    # Get a reference to the app for the background thread
    app = current_app._get_current_object()
    
    # Start a background thread for preprocessing
    def run_with_monitor():
        # Create app context for the thread
        with app.app_context():
            try:
                # Run preprocessor with log ID
                success = run_preprocessing(latest_file, log_id)
                
                # Double-check status with a fresh query
                updated_log = ProcessingLog.query.get(log_id)
                if updated_log and updated_log.status == 'running':
                    # Update status if still running
                    updated_log.status = 'completed' if success else 'failed'
                    updated_log.end_time = datetime.now()
                    db.session.commit()
            except Exception as e:
                # Handle exceptions - get a fresh instance
                app.logger.error(f"Error in preprocessing thread: {str(e)}")
                updated_log = ProcessingLog.query.get(log_id)
                if updated_log:
                    updated_log.status = 'failed'
                    updated_log.error_message = str(e)
                    updated_log.end_time = datetime.now()
                    db.session.commit()
    
    preprocess_thread = threading.Thread(target=run_with_monitor)
    preprocess_thread.daemon = True
    preprocess_thread.start()
    
    flash('Preprocessing job started successfully! Check the logs for progress.', 'success')
    return redirect(url_for('main.index'))

@main_bp.route('/import-to-db', methods=['POST'])
def import_to_db():
    """Import processed data to database."""
    file_path = request.form.get('file_path')
    if not file_path:
        # Get the most recent processed file
        processed_dir = current_app.config['PROCESSED_FOLDER']
        processed_files = [f for f in os.listdir(processed_dir) if f.endswith('.csv')]
        
        if not processed_files:
            flash('No processed files found. Please run preprocessing first.', 'error')
            return redirect(url_for('main.index'))
        
        # Sort by modification time (most recent first)
        processed_files.sort(key=lambda f: os.path.getmtime(os.path.join(processed_dir, f)), reverse=True)
        file_path = os.path.join(processed_dir, processed_files[0])
    
    # Get a reference to the app for the background thread
    app = current_app._get_current_object()
    
    # Run import in a background thread
    def import_with_monitor():
        # Create app context for the thread
        with app.app_context():
            try:
                # Run the import
                start_time = datetime.now()
                app.logger.info(f"Starting import at {start_time}")
                
                success = import_data_to_db(file_path)
                
                end_time = datetime.now()
                duration = (end_time - start_time).total_seconds()
                
                # Log the result
                if success:
                    app.logger.info(f"Successfully imported data from {file_path} in {duration:.2f} seconds")
                else:
                    app.logger.error(f"Failed to import data from {file_path} after {duration:.2f} seconds")
                    
            except Exception as e:
                app.logger.error(f"Error importing data: {str(e)}")
    
    import_thread = threading.Thread(target=import_with_monitor)
    import_thread.daemon = True
    import_thread.start()
    
    flash('Data import started! This may take a few minutes.', 'success')
    return redirect(url_for('main.index'))

@main_bp.route('/logs')
def logs():
    """View logs page."""
    crawl_logs = CrawlLog.query.order_by(CrawlLog.start_time.desc()).limit(10).all()
    processing_logs = ProcessingLog.query.order_by(ProcessingLog.start_time.desc()).limit(10).all()
    
    return render_template('logs.html', 
                           crawl_logs=crawl_logs, 
                           processing_logs=processing_logs)

@main_bp.route('/api/crawl-status/<int:log_id>')
def crawl_status(log_id):
    """API to check crawling status."""
    log = CrawlLog.query.get_or_404(log_id)
    return jsonify({
        'id': log.id,
        'status': log.status,
        'records_count': log.records_count,
        'start_time': log.start_time.strftime('%Y-%m-%d %H:%M:%S'),
        'end_time': log.end_time.strftime('%Y-%m-%d %H:%M:%S') if log.end_time else None,
        'error_message': log.error_message
    })

@main_bp.route('/api/processing-status/<int:log_id>')
def processing_status(log_id):
    """API to check preprocessing status."""
    log = ProcessingLog.query.get_or_404(log_id)
    return jsonify({
        'id': log.id,
        'status': log.status,
        'records_count': log.records_count,
        'start_time': log.start_time.strftime('%Y-%m-%d %H:%M:%S'),
        'end_time': log.end_time.strftime('%Y-%m-%d %H:%M:%S') if log.end_time else None,
        'input_file': log.input_file,
        'output_file': log.output_file,
        'error_message': log.error_message
    })

@main_bp.route('/api/check-stuck-crawlers')
def check_stuck_crawlers_api():
    """API to check for crawlers that might be stuck and update their status."""
    updated_count = check_stuck_crawlers()
    
    return jsonify({
        'success': True,
        'updated_jobs': updated_count
    })

@main_bp.route('/api/reset-crawler/<int:log_id>')
def reset_crawler(log_id):
    """API to reset a specific crawler job."""
    log = CrawlLog.query.get_or_404(log_id)
    
    if log.status.startswith('running'):
        log.status = 'completed'
        log.end_time = datetime.now()
        log.error_message = 'Manually reset by user'
        db.session.commit()
        return jsonify({'success': True, 'message': f'Crawler job {log_id} has been reset to completed'})
    
    return jsonify({'success': False, 'message': f'Crawler job {log_id} is not in running state'})

@main_bp.route('/api/reset-processing/<int:log_id>')
def reset_processing(log_id):
    """API to reset a specific processing job."""
    log = ProcessingLog.query.get_or_404(log_id)
    
    if log.status == 'running':
        log.status = 'completed'
        log.end_time = datetime.now()
        log.error_message = 'Manually reset by user'
        db.session.commit()
        return jsonify({'success': True, 'message': f'Processing job {log_id} has been reset to completed'})
    
    return jsonify({'success': False, 'message': f'Processing job {log_id} is not in running state'})

@main_bp.route('/database-info')
def database_info():
    """View database information."""
    # Get counts
    brand_count = Brand.query.count()
    model_count = Model.query.count()
    
    # Get sample data
    brands = Brand.query.all()
    models = Model.query.limit(20).all()
    
    # Get counts for other tables
    from app.models import CarType, FuelType, Transmission, Year, Seat
    car_type_count = CarType.query.count()
    fuel_type_count = FuelType.query.count()
    transmission_count = Transmission.query.count()
    year_count = Year.query.count()
    seat_count = Seat.query.count()
    
    return render_template('database_info.html',
                           brand_count=brand_count,
                           model_count=model_count,
                           car_type_count=car_type_count,
                           fuel_type_count=fuel_type_count,
                           transmission_count=transmission_count,
                           year_count=year_count,
                           seat_count=seat_count,
                           brands=brands,
                           models=models)