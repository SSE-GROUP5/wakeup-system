#pragma once



// CDisplayView form view

class CDisplayView : public CFormView
{
	DECLARE_DYNCREATE(CDisplayView)

protected:
	CDisplayView();           // protected constructor used by dynamic creation
	virtual ~CDisplayView();

public:
#ifdef AFX_DESIGN_TIME
	enum { IDD = IDD_CDisplayView };
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
};


