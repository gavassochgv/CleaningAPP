// Modified App.tsx to use backend API instead of localStorage
// This file will replace the localStorage functionality with API calls

// Add this to the beginning of your App component to handle data migration and loading
const useBackendData = () => {
  const [isLoading, setIsLoading] = React.useState(true);
  const [error, setError] = React.useState(null);

  // Initialize data from backend
  React.useEffect(() => {
    const initializeData = async () => {
      try {
        setIsLoading(true);
        
        // First, try to migrate any existing localStorage data
        await window.CleaningAPI.migrateFromLocalStorage();
        
        // Then load all data from backend
        const data = await window.CleaningAPI.loadAllData();
        
        // Update state with backend data
        setReports(data.reports || []);
        setInvoices(data.invoices || []);
        setBankAccounts(data.bankAccounts || []);
        setPresets(data.presets || []);
        
        setIsLoading(false);
      } catch (err) {
        console.error('Failed to initialize data:', err);
        setError(err.message);
        setIsLoading(false);
      }
    };

    initializeData();
  }, []);

  return { isLoading, error };
};

// Replace localStorage-based state management with API calls
// Instead of:
// const [reports, setReports] = useState(() => {
//   try { const raw = localStorage.getItem("cleaning_reports_v1"); return raw ? JSON.parse(raw) : []; } catch { return []; }
// });
// useEffect(() => { try { localStorage.setItem("cleaning_reports_v1", JSON.stringify(reports)); } catch {} }, [reports]);

// Use:
const [reports, setReports] = useState([]);
const [invoices, setInvoices] = useState([]);
const [bankAccounts, setBankAccounts] = useState([]);
const [presets, setPresets] = useState([]);

// Add API-based CRUD operations
const apiOperations = {
  // Reports
  async createReport(reportData) {
    try {
      const newReport = await window.CleaningAPI.createReport(reportData);
      setReports(prev => [newReport, ...prev]);
      return newReport;
    } catch (error) {
      console.error('Failed to create report:', error);
      alert('Failed to save report. Please try again.');
      throw error;
    }
  },

  async updateReport(reportId, reportData) {
    try {
      const updatedReport = await window.CleaningAPI.updateReport(reportId, reportData);
      setReports(prev => prev.map(r => r.id === reportId ? updatedReport : r));
      return updatedReport;
    } catch (error) {
      console.error('Failed to update report:', error);
      alert('Failed to update report. Please try again.');
      throw error;
    }
  },

  async deleteReport(reportId) {
    try {
      await window.CleaningAPI.deleteReport(reportId);
      setReports(prev => prev.filter(r => r.id !== reportId));
    } catch (error) {
      console.error('Failed to delete report:', error);
      alert('Failed to delete report. Please try again.');
      throw error;
    }
  },

  // Invoices
  async createInvoice(invoiceData) {
    try {
      const newInvoice = await window.CleaningAPI.createInvoice(invoiceData);
      setInvoices(prev => [newInvoice, ...prev]);
      return newInvoice;
    } catch (error) {
      console.error('Failed to create invoice:', error);
      alert('Failed to save invoice. Please try again.');
      throw error;
    }
  },

  async updateInvoice(invoiceId, invoiceData) {
    try {
      const updatedInvoice = await window.CleaningAPI.updateInvoice(invoiceId, invoiceData);
      setInvoices(prev => prev.map(i => i.id === invoiceId ? updatedInvoice : i));
      return updatedInvoice;
    } catch (error) {
      console.error('Failed to update invoice:', error);
      alert('Failed to update invoice. Please try again.');
      throw error;
    }
  },

  async deleteInvoice(invoiceId) {
    try {
      await window.CleaningAPI.deleteInvoice(invoiceId);
      setInvoices(prev => prev.filter(i => i.id !== invoiceId));
    } catch (error) {
      console.error('Failed to delete invoice:', error);
      alert('Failed to delete invoice. Please try again.');
      throw error;
    }
  },

  // Bank Accounts
  async createBankAccount(accountData) {
    try {
      const newAccount = await window.CleaningAPI.createBankAccount(accountData);
      setBankAccounts(prev => [...prev, newAccount]);
      return newAccount;
    } catch (error) {
      console.error('Failed to create bank account:', error);
      alert('Failed to save bank account. Please try again.');
      throw error;
    }
  },

  async updateBankAccount(accountId, accountData) {
    try {
      const updatedAccount = await window.CleaningAPI.updateBankAccount(accountId, accountData);
      setBankAccounts(prev => prev.map(a => a.id === accountId ? updatedAccount : a));
      return updatedAccount;
    } catch (error) {
      console.error('Failed to update bank account:', error);
      alert('Failed to update bank account. Please try again.');
      throw error;
    }
  },

  async deleteBankAccount(accountId) {
    try {
      await window.CleaningAPI.deleteBankAccount(accountId);
      setBankAccounts(prev => prev.filter(a => a.id !== accountId));
    } catch (error) {
      console.error('Failed to delete bank account:', error);
      alert('Failed to delete bank account. Please try again.');
      throw error;
    }
  },

  // Presets
  async createPreset(presetData) {
    try {
      const newPreset = await window.CleaningAPI.createPreset(presetData);
      setPresets(prev => [...prev, newPreset]);
      return newPreset;
    } catch (error) {
      console.error('Failed to create preset:', error);
      alert('Failed to save preset. Please try again.');
      throw error;
    }
  },

  async deletePreset(presetId) {
    try {
      await window.CleaningAPI.deletePreset(presetId);
      setPresets(prev => prev.filter(p => p.id !== presetId));
    } catch (error) {
      console.error('Failed to delete preset:', error);
      alert('Failed to delete preset. Please try again.');
      throw error;
    }
  }
};

// Instructions for integrating into the main App component:
/*
1. Add the useBackendData hook at the beginning of your App component
2. Replace all localStorage-based state initialization with empty arrays
3. Remove all useEffect hooks that sync with localStorage
4. Replace direct state mutations with API calls using the apiOperations object
5. Add loading and error states to handle API operations
6. Update form submissions to use API operations instead of direct state updates

Example integration:

export default function CleaningReportApp() {
  // ... existing auth state ...
  
  // Replace localStorage state with API-backed state
  const [reports, setReports] = useState([]);
  const [invoices, setInvoices] = useState([]);
  const [bankAccounts, setBankAccounts] = useState([]);
  const [presets, setPresets] = useState([]);
  
  // Add loading and error handling
  const { isLoading, error } = useBackendData();
  
  // ... rest of your component ...
  
  // Replace form submission handlers
  const handleReportSubmit = async (e) => {
    e.preventDefault();
    try {
      const reportData = {
        date,
        staffName,
        summary,
        notes,
        areas,
        photos: await Promise.all(photos.map(fileToJPEGDataURL))
      };
      
      await apiOperations.createReport(reportData);
      
      // Reset form
      setDate("");
      setStaffName("");
      // ... reset other fields ...
      
      setView("reports");
    } catch (error) {
      // Error is already handled in apiOperations
    }
  };
  
  // Add loading state to your render
  if (isLoading) {
    return <div className="flex items-center justify-center min-h-screen">
      <div className="text-lg">Loading...</div>
    </div>;
  }
  
  if (error) {
    return <div className="flex items-center justify-center min-h-screen">
      <div className="text-red-500">Error: {error}</div>
    </div>;
  }
  
  // ... rest of your render method ...
}
*/

