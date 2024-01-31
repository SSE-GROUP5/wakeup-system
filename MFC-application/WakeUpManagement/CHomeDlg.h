#pragma once



// CHomeDlg form view

class CHomeDlg : public CFormView
{
	DECLARE_DYNCREATE(CHomeDlg)

protected:
	CHomeDlg();           // protected constructor used by dynamic creation
	virtual ~CHomeDlg();

public:
#ifdef AFX_DESIGN_TIME
	enum { IDD = IDD_HOME };
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
	CFont m_Font;
public:
	virtual void OnInitialUpdate();
};


