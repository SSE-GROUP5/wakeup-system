#pragma once



// CPatientRecordDlg form view

class CPatientRecordDlg : public CFormView
{
	DECLARE_DYNCREATE(CPatientRecordDlg)

protected:
	CPatientRecordDlg();           // protected constructor used by dynamic creation
	virtual ~CPatientRecordDlg();

public:
#ifdef AFX_DESIGN_TIME
	enum { IDD = IDD_DIALOG_PATIENT_RECORD };
#endif
#ifdef _DEBUG
	virtual void AssertValid() const;
#ifndef _WIN32_WCE
	virtual void Dump(CDumpContext& dc) const;
#endif
#endif

protected:
	virtual void DoDataExchange(CDataExchange* pDX);    // DDX/DDV support

	DECLARE_MESSAGE_MAP()
private:
	CListCtrl m_patient_record;
public:
	virtual void OnInitialUpdate();
private:
	CFont m_Title_Font;
private:
	CFont m_Table_Font;
};


