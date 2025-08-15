from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import json

db = SQLAlchemy()

class Report(db.Model):
    __tablename__ = 'reports'
    
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(10), nullable=False)  # ISO date format
    staff_name = db.Column(db.String(100), nullable=False)
    summary = db.Column(db.Text, nullable=False)
    notes = db.Column(db.Text, default='')
    areas_json = db.Column(db.Text, nullable=False)  # JSON string of areas
    photos_json = db.Column(db.Text, default='[]')  # JSON string of photo data URLs
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'date': self.date,
            'staffName': self.staff_name,
            'summary': self.summary,
            'notes': self.notes,
            'areas': json.loads(self.areas_json) if self.areas_json else [],
            'photos': json.loads(self.photos_json) if self.photos_json else []
        }
    
    @classmethod
    def from_dict(cls, data):
        return cls(
            date=data.get('date', ''),
            staff_name=data.get('staffName', ''),
            summary=data.get('summary', ''),
            notes=data.get('notes', ''),
            areas_json=json.dumps(data.get('areas', [])),
            photos_json=json.dumps(data.get('photos', []))
        )

class Invoice(db.Model):
    __tablename__ = 'invoices'
    
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(10), nullable=False)  # ISO date format
    client_name = db.Column(db.String(100), nullable=False)
    client_address = db.Column(db.Text, nullable=False)
    items_json = db.Column(db.Text, nullable=False)  # JSON string of invoice items
    payment_method = db.Column(db.String(20), nullable=False)  # 'cash' or 'bank'
    bank_account_id = db.Column(db.String(50), nullable=True)
    notes = db.Column(db.Text, default='')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'date': self.date,
            'clientName': self.client_name,
            'clientAddress': self.client_address,
            'items': json.loads(self.items_json) if self.items_json else [],
            'paymentMethod': self.payment_method,
            'bankAccountId': self.bank_account_id,
            'notes': self.notes
        }
    
    @classmethod
    def from_dict(cls, data):
        return cls(
            date=data.get('date', ''),
            client_name=data.get('clientName', ''),
            client_address=data.get('clientAddress', ''),
            items_json=json.dumps(data.get('items', [])),
            payment_method=data.get('paymentMethod', 'cash'),
            bank_account_id=data.get('bankAccountId'),
            notes=data.get('notes', '')
        )

class BankAccount(db.Model):
    __tablename__ = 'bank_accounts'
    
    id = db.Column(db.String(50), primary_key=True)
    bank_name = db.Column(db.String(100), nullable=False)
    account_name = db.Column(db.String(100), nullable=False)
    sort_code = db.Column(db.String(20), nullable=False)
    account_number = db.Column(db.String(20), nullable=False)
    iban = db.Column(db.String(50), nullable=True)
    reference_note = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'bankName': self.bank_name,
            'accountName': self.account_name,
            'sortCode': self.sort_code,
            'accountNumber': self.account_number,
            'iban': self.iban,
            'referenceNote': self.reference_note
        }
    
    @classmethod
    def from_dict(cls, data):
        return cls(
            id=data.get('id', ''),
            bank_name=data.get('bankName', ''),
            account_name=data.get('accountName', ''),
            sort_code=data.get('sortCode', ''),
            account_number=data.get('accountNumber', ''),
            iban=data.get('iban'),
            reference_note=data.get('referenceNote')
        )

class Preset(db.Model):
    __tablename__ = 'presets'
    
    id = db.Column(db.Integer, primary_key=True)
    site_name = db.Column(db.String(100), nullable=False)
    sections_json = db.Column(db.Text, nullable=False)  # JSON string of sections
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'siteName': self.site_name,
            'sections': json.loads(self.sections_json) if self.sections_json else []
        }
    
    @classmethod
    def from_dict(cls, data):
        return cls(
            site_name=data.get('siteName', ''),
            sections_json=json.dumps(data.get('sections', []))
        )

