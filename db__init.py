"""Database initialization script to create tables and populate with initial data."""
from flask import Flask
from app.utils.database import configure_db, db
from app.models import Brand, Model, CarType, FuelType, Transmission, Year, Seat
import os
import csv

def create_app():
    """Create a Flask app instance for database initialization."""
    app = Flask(__name__)
    configure_db(app)
    return app

def init_db():
    """Initialize the database with tables and initial values."""
    app = create_app()
    
    with app.app_context():
        # Create all tables
        db.create_all()
        
        print("Tables created successfully.")
        
        # Add initial fuel types
        fuel_types = ['Xăng', 'Dầu', 'Điện', 'Hybrid', 'Khác']
        for fuel in fuel_types:
            if not FuelType.query.filter_by(type=fuel).first():
                db.session.add(FuelType(type=fuel))
        
        # Add initial transmission types
        transmissions = ['Số sàn', 'Số tự động', 'Số hỗn hợp', 'Khác']
        for trans in transmissions:
            if not Transmission.query.filter_by(transmission=trans).first():
                db.session.add(Transmission(transmission=trans))
        
        # Add initial years (2000-2025)
        for year in range(2000, 2026):
            if not Year.query.filter_by(year=year).first():
                db.session.add(Year(year=year))
        
        # Add initial seat counts
        seats = [2, 4, 5, 7, 8, 9, 12, 16]
        for seat in seats:
            if not Seat.query.filter_by(seat=seat).first():
                db.session.add(Seat(seat=seat))
        
        # Add some common car brands
        common_brands = [
            'Toyota', 'Honda', 'Ford', 'Mazda', 'Kia', 
            'Hyundai', 'Mercedes-Benz', 'BMW', 'Audi', 'Lexus',
            'Mitsubishi', 'Nissan', 'Suzuki', 'Volkswagen', 'Chevrolet',
            'Porsche', 'Land Rover', 'Volvo', 'Subaru', 'Peugeot'
        ]
        
        for brand_name in common_brands:
            if not Brand.query.filter_by(name=brand_name).first():
                db.session.add(Brand(name=brand_name))
        
        db.session.commit()
        
        print("Database initialized with initial data!")

if __name__ == "__main__":
    init_db()
    print("Database setup complete!")