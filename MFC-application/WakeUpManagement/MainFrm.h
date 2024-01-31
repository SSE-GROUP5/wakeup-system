
// MainFrm.h : interface of the CMainFrame class
//

#pragma once


//Customised message
#define NM_HOME (WM_USER + 99)
#define NM_A (WM_USER + 100)
#define NM_B (WM_USER + 101)
#define NM_C (WM_USER + 102)

class CMainFrame : public CFrameWnd
{
	
protected: // create from serialization only
	CMainFrame() noexcept;
	DECLARE_DYNCREATE(CMainFrame)

// Attributes
public:

// Operations
public:

// Overrides
public:
	virtual BOOL PreCreateWindow(CREATESTRUCT& cs);

// Implementation
public:
	virtual ~CMainFrame();
#ifdef _DEBUG
	virtual void AssertValid() const;
	virtual void Dump(CDumpContext& dc) const;
#endif

protected:  // control bar embedded members
	CStatusBar        m_wndStatusBar;

// Generated message map functions
protected:
	afx_msg int OnCreate(LPCREATESTRUCT lpCreateStruct);
	DECLARE_MESSAGE_MAP()

	virtual BOOL OnCreateClient(LPCREATESTRUCT lpcs, CCreateContext* pContext);

private:
	CSplitterWnd m_spliter; //split the window


	afx_msg LRESULT OnMyChange(WPARAM wParam, LPARAM lParam);
};


