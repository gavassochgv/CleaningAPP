// API helper functions for communicating with the backend

const API_BASE = window.location.origin + '/api';

class CleaningAPI {
  // Helper method for making API requests
  static async request(endpoint, options = {}) {
    const url = `${API_BASE}${endpoint}`;
    const config = {
      headers: {
        'Content-Type': 'application/json',
        ...options.headers,
      },
      ...options,
    };

    try {
      const response = await fetch(url, config);
      
      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.error || `HTTP ${response.status}: ${response.statusText}`);
      }

      return await response.json();
    } catch (error) {
      console.error(`API request failed for ${endpoint}:`, error);
      throw error;
    }
  }

  // ==================== REPORTS ====================
  
  static async getReports() {
    return this.request('/reports');
  }

  static async createReport(reportData) {
    return this.request('/reports', {
      method: 'POST',
      body: JSON.stringify(reportData),
    });
  }

  static async updateReport(reportId, reportData) {
    return this.request(`/reports/${reportId}`, {
      method: 'PUT',
      body: JSON.stringify(reportData),
    });
  }

  static async deleteReport(reportId) {
    return this.request(`/reports/${reportId}`, {
      method: 'DELETE',
    });
  }

  // ==================== INVOICES ====================
  
  static async getInvoices() {
    return this.request('/invoices');
  }

  static async createInvoice(invoiceData) {
    return this.request('/invoices', {
      method: 'POST',
      body: JSON.stringify(invoiceData),
    });
  }

  static async updateInvoice(invoiceId, invoiceData) {
    return this.request(`/invoices/${invoiceId}`, {
      method: 'PUT',
      body: JSON.stringify(invoiceData),
    });
  }

  static async deleteInvoice(invoiceId) {
    return this.request(`/invoices/${invoiceId}`, {
      method: 'DELETE',
    });
  }

  // ==================== BANK ACCOUNTS ====================
  
  static async getBankAccounts() {
    return this.request('/bank-accounts');
  }

  static async createBankAccount(accountData) {
    return this.request('/bank-accounts', {
      method: 'POST',
      body: JSON.stringify(accountData),
    });
  }

  static async updateBankAccount(accountId, accountData) {
    return this.request(`/bank-accounts/${accountId}`, {
      method: 'PUT',
      body: JSON.stringify(accountData),
    });
  }

  static async deleteBankAccount(accountId) {
    return this.request(`/bank-accounts/${accountId}`, {
      method: 'DELETE',
    });
  }

  // ==================== PRESETS ====================
  
  static async getPresets() {
    return this.request('/presets');
  }

  static async createPreset(presetData) {
    return this.request('/presets', {
      method: 'POST',
      body: JSON.stringify(presetData),
    });
  }

  static async deletePreset(presetId) {
    return this.request(`/presets/${presetId}`, {
      method: 'DELETE',
    });
  }

  // ==================== SYNC ====================
  
  static async syncData(localData) {
    return this.request('/sync', {
      method: 'POST',
      body: JSON.stringify(localData),
    });
  }

  // ==================== MIGRATION HELPERS ====================
  
  // Migrate data from localStorage to backend
  static async migrateFromLocalStorage() {
    try {
      const localData = {};
      
      // Get data from localStorage
      const reportsData = localStorage.getItem('cleaning_reports_v1');
      if (reportsData) {
        localData.reports = JSON.parse(reportsData);
      }
      
      const invoicesData = localStorage.getItem('cleaning_invoices_v1');
      if (invoicesData) {
        localData.invoices = JSON.parse(invoicesData);
      }
      
      const bankAccountsData = localStorage.getItem('bank_accounts_v1');
      if (bankAccountsData) {
        localData.bankAccounts = JSON.parse(bankAccountsData);
      }
      
      const presetsData = localStorage.getItem('cleaning_presets_v1');
      if (presetsData) {
        localData.presets = JSON.parse(presetsData);
      }
      
      // Only sync if there's data to migrate
      if (Object.keys(localData).length > 0) {
        console.log('Migrating data from localStorage to backend...', localData);
        const result = await this.syncData(localData);
        
        // Clear localStorage after successful migration
        localStorage.removeItem('cleaning_reports_v1');
        localStorage.removeItem('cleaning_invoices_v1');
        localStorage.removeItem('bank_accounts_v1');
        localStorage.removeItem('cleaning_presets_v1');
        
        console.log('Migration completed successfully');
        return result;
      }
      
      return null;
    } catch (error) {
      console.error('Migration failed:', error);
      throw error;
    }
  }

  // Load all data from backend
  static async loadAllData() {
    try {
      const [reports, invoices, bankAccounts, presets] = await Promise.all([
        this.getReports(),
        this.getInvoices(),
        this.getBankAccounts(),
        this.getPresets(),
      ]);

      return {
        reports,
        invoices,
        bankAccounts,
        presets,
      };
    } catch (error) {
      console.error('Failed to load data from backend:', error);
      throw error;
    }
  }
}

// Make API available globally
window.CleaningAPI = CleaningAPI;

