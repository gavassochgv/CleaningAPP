from flask import Blueprint, request, jsonify
import json
from src.models.cleaning import db, Report, Invoice, BankAccount, Preset

cleaning_bp = Blueprint('cleaning', __name__)

# ==================== REPORTS ====================

@cleaning_bp.route('/reports', methods=['GET'])
def get_reports():
    """Obter todos os reports"""
    try:
        reports = Report.query.order_by(Report.created_at.desc()).all()
        return jsonify([report.to_dict() for report in reports])
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@cleaning_bp.route('/reports', methods=['POST'])
def create_report():
    """Criar um novo report"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        report = Report.from_dict(data)
        db.session.add(report)
        db.session.commit()
        
        return jsonify(report.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@cleaning_bp.route('/reports/<int:report_id>', methods=['PUT'])
def update_report(report_id):
    """Atualizar um report existente"""
    try:
        report = Report.query.get_or_404(report_id)
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        report.date = data.get('date', report.date)
        report.staff_name = data.get('staffName', report.staff_name)
        report.summary = data.get('summary', report.summary)
        report.notes = data.get('notes', report.notes)
        report.areas_json = json.dumps(data.get('areas', []))
        report.photos_json = json.dumps(data.get('photos', []))
        
        db.session.commit()
        return jsonify(report.to_dict())
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@cleaning_bp.route('/reports/<int:report_id>', methods=['DELETE'])
def delete_report(report_id):
    """Deletar um report"""
    try:
        report = Report.query.get_or_404(report_id)
        db.session.delete(report)
        db.session.commit()
        return jsonify({'message': 'Report deleted successfully'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# ==================== INVOICES ====================

@cleaning_bp.route('/invoices', methods=['GET'])
def get_invoices():
    """Obter todos os invoices"""
    try:
        invoices = Invoice.query.order_by(Invoice.created_at.desc()).all()
        return jsonify([invoice.to_dict() for invoice in invoices])
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@cleaning_bp.route('/invoices', methods=['POST'])
def create_invoice():
    """Criar um novo invoice"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        invoice = Invoice.from_dict(data)
        db.session.add(invoice)
        db.session.commit()
        
        return jsonify(invoice.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@cleaning_bp.route('/invoices/<int:invoice_id>', methods=['PUT'])
def update_invoice(invoice_id):
    """Atualizar um invoice existente"""
    try:
        invoice = Invoice.query.get_or_404(invoice_id)
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        invoice.date = data.get('date', invoice.date)
        invoice.client_name = data.get('clientName', invoice.client_name)
        invoice.client_address = data.get('clientAddress', invoice.client_address)
        invoice.items_json = json.dumps(data.get('items', []))
        invoice.payment_method = data.get('paymentMethod', invoice.payment_method)
        invoice.bank_account_id = data.get('bankAccountId', invoice.bank_account_id)
        invoice.notes = data.get('notes', invoice.notes)
        
        db.session.commit()
        return jsonify(invoice.to_dict())
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@cleaning_bp.route('/invoices/<int:invoice_id>', methods=['DELETE'])
def delete_invoice(invoice_id):
    """Deletar um invoice"""
    try:
        invoice = Invoice.query.get_or_404(invoice_id)
        db.session.delete(invoice)
        db.session.commit()
        return jsonify({'message': 'Invoice deleted successfully'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# ==================== BANK ACCOUNTS ====================

@cleaning_bp.route('/bank-accounts', methods=['GET'])
def get_bank_accounts():
    """Obter todas as contas bancárias"""
    try:
        accounts = BankAccount.query.all()
        return jsonify([account.to_dict() for account in accounts])
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@cleaning_bp.route('/bank-accounts', methods=['POST'])
def create_bank_account():
    """Criar uma nova conta bancária"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        account = BankAccount.from_dict(data)
        db.session.add(account)
        db.session.commit()
        
        return jsonify(account.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@cleaning_bp.route('/bank-accounts/<string:account_id>', methods=['PUT'])
def update_bank_account(account_id):
    """Atualizar uma conta bancária existente"""
    try:
        account = BankAccount.query.get_or_404(account_id)
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        account.bank_name = data.get('bankName', account.bank_name)
        account.account_name = data.get('accountName', account.account_name)
        account.sort_code = data.get('sortCode', account.sort_code)
        account.account_number = data.get('accountNumber', account.account_number)
        account.iban = data.get('iban', account.iban)
        account.reference_note = data.get('referenceNote', account.reference_note)
        
        db.session.commit()
        return jsonify(account.to_dict())
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@cleaning_bp.route('/bank-accounts/<string:account_id>', methods=['DELETE'])
def delete_bank_account(account_id):
    """Deletar uma conta bancária"""
    try:
        account = BankAccount.query.get_or_404(account_id)
        db.session.delete(account)
        db.session.commit()
        return jsonify({'message': 'Bank account deleted successfully'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# ==================== PRESETS ====================

@cleaning_bp.route('/presets', methods=['GET'])
def get_presets():
    """Obter todos os presets"""
    try:
        presets = Preset.query.all()
        return jsonify([preset.to_dict() for preset in presets])
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@cleaning_bp.route('/presets', methods=['POST'])
def create_preset():
    """Criar um novo preset"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        preset = Preset.from_dict(data)
        db.session.add(preset)
        db.session.commit()
        
        return jsonify(preset.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@cleaning_bp.route('/presets/<int:preset_id>', methods=['DELETE'])
def delete_preset(preset_id):
    """Deletar um preset"""
    try:
        preset = Preset.query.get_or_404(preset_id)
        db.session.delete(preset)
        db.session.commit()
        return jsonify({'message': 'Preset deleted successfully'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# ==================== SYNC ====================

@cleaning_bp.route('/sync', methods=['POST'])
def sync_data():
    """Sincronizar dados do localStorage com o backend"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        # Sincronizar reports
        if 'reports' in data:
            for report_data in data['reports']:
                # Verificar se já existe pelo ID (se fornecido)
                existing_report = None
                if 'id' in report_data and report_data['id']:
                    existing_report = Report.query.get(report_data['id'])
                
                if existing_report:
                    # Atualizar existente
                    existing_report.date = report_data.get('date', existing_report.date)
                    existing_report.staff_name = report_data.get('staffName', existing_report.staff_name)
                    existing_report.summary = report_data.get('summary', existing_report.summary)
                    existing_report.notes = report_data.get('notes', existing_report.notes)
                    existing_report.areas_json = json.dumps(report_data.get('areas', []))
                    existing_report.photos_json = json.dumps(report_data.get('photos', []))
                else:
                    # Criar novo
                    new_report = Report.from_dict(report_data)
                    db.session.add(new_report)
        
        # Sincronizar invoices
        if 'invoices' in data:
            for invoice_data in data['invoices']:
                existing_invoice = None
                if 'id' in invoice_data and invoice_data['id']:
                    existing_invoice = Invoice.query.get(invoice_data['id'])
                
                if existing_invoice:
                    # Atualizar existente
                    existing_invoice.date = invoice_data.get('date', existing_invoice.date)
                    existing_invoice.client_name = invoice_data.get('clientName', existing_invoice.client_name)
                    existing_invoice.client_address = invoice_data.get('clientAddress', existing_invoice.client_address)
                    existing_invoice.items_json = json.dumps(invoice_data.get('items', []))
                    existing_invoice.payment_method = invoice_data.get('paymentMethod', existing_invoice.payment_method)
                    existing_invoice.bank_account_id = invoice_data.get('bankAccountId', existing_invoice.bank_account_id)
                    existing_invoice.notes = invoice_data.get('notes', existing_invoice.notes)
                else:
                    # Criar novo
                    new_invoice = Invoice.from_dict(invoice_data)
                    db.session.add(new_invoice)
        
        # Sincronizar bank accounts
        if 'bankAccounts' in data:
            for account_data in data['bankAccounts']:
                existing_account = BankAccount.query.get(account_data.get('id'))
                if not existing_account:
                    new_account = BankAccount.from_dict(account_data)
                    db.session.add(new_account)
        
        # Sincronizar presets
        if 'presets' in data:
            for preset_data in data['presets']:
                new_preset = Preset.from_dict(preset_data)
                db.session.add(new_preset)
        
        db.session.commit()
        
        # Retornar todos os dados atualizados
        reports = Report.query.order_by(Report.created_at.desc()).all()
        invoices = Invoice.query.order_by(Invoice.created_at.desc()).all()
        bank_accounts = BankAccount.query.all()
        presets = Preset.query.all()
        
        return jsonify({
            'reports': [report.to_dict() for report in reports],
            'invoices': [invoice.to_dict() for invoice in invoices],
            'bankAccounts': [account.to_dict() for account in bank_accounts],
            'presets': [preset.to_dict() for preset in presets]
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

