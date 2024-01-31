#pragma once



// CDevicesSettingDlg form view

class CDevicesSettingDlg : public CFormView
{
	DECLARE_DYNCREATE(CDevicesSettingDlg)

protected:
	CDevicesSettingDlg();           // protected constructor used by dynamic creation
	virtual ~CDevicesSettingDlg();

public:
#ifdef AFX_DESIGN_TIME
	enum { IDD = IDD_DIALOG_DEVICES_SETTING };
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
public:
	virtual void OnInitialUpdate();
private:
	CListCtrl m_controllers;
	CListCtrl m_matter_devices;
private:
	CFont m_Table_Font;
};


