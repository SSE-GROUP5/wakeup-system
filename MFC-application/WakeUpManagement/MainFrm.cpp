
// MainFrm.cpp : implementation of the CMainFrame class
//

#include "pch.h"
#include "framework.h"
#include "WakeUpManagement.h"

#include "MainFrm.h"
#include "CSelectView.h"
#include "CDisplayView.h"
#include "CPatientRecordDlg.h"
#include "CDevicesSettingDlg.h"
#include "CWakeUpSettingDlg.h"
#include "CHomeDlg.h"

#ifdef _DEBUG
#define new DEBUG_NEW
#endif

// CMainFrame

IMPLEMENT_DYNCREATE(CMainFrame, CFrameWnd)

BEGIN_MESSAGE_MAP(CMainFrame, CFrameWnd)
	ON_WM_CREATE()
	//respond to the customised message
	ON_MESSAGE(NM_HOME, OnMyChange)
	ON_MESSAGE(NM_A, OnMyChange)
	ON_MESSAGE(NM_B, OnMyChange)
	ON_MESSAGE(NM_C, OnMyChange)
END_MESSAGE_MAP()

static UINT indicators[] =
{
	ID_SEPARATOR,           // status line indicator
	ID_INDICATOR_CAPS,
	ID_INDICATOR_NUM,
	ID_INDICATOR_SCRL,
};

// CMainFrame construction/destruction

CMainFrame::CMainFrame() noexcept
{
	// TODO: add member initialization code here
}

CMainFrame::~CMainFrame()
{
}

int CMainFrame::OnCreate(LPCREATESTRUCT lpCreateStruct)
{
	if (CFrameWnd::OnCreate(lpCreateStruct) == -1)
		return -1;

	if (!m_wndStatusBar.Create(this))
	{
		TRACE0("Failed to create status bar\n");
		return -1;      // fail to create
	}
	m_wndStatusBar.SetIndicators(indicators, sizeof(indicators)/sizeof(UINT));

	//Set Icon
	SetClassLongPtr(m_hWnd, GCLP_HICON, (LONG_PTR)AfxGetApp()->LoadIconW(IDI_ICON_TECH));

	//Set Subtitle
	SetTitle(TEXT("Management System"));

	//Set Window Size
	MoveWindow(0, 0, 1800, 1000);

	//Show in the center
	CenterWindow();

	return 0;
}

BOOL CMainFrame::PreCreateWindow(CREATESTRUCT& cs)
{
	if( !CFrameWnd::PreCreateWindow(cs) )
		return FALSE;
	// TODO: Modify the Window class or styles here by modifying
	//  the CREATESTRUCT cs

	return TRUE;
}

// CMainFrame diagnostics

#ifdef _DEBUG
void CMainFrame::AssertValid() const
{
	CFrameWnd::AssertValid();
}

void CMainFrame::Dump(CDumpContext& dc) const
{
	CFrameWnd::Dump(dc);
}
#endif //_DEBUG


// CMainFrame message handlers



BOOL CMainFrame::OnCreateClient(LPCREATESTRUCT lpcs, CCreateContext* pContext)
{
	// TODO: Add your specialized code here and/or call the base class

	//return CFrameWnd::OnCreateClient(lpcs, pContext);

	//Split into 1 row 2 col
	m_spliter.CreateStatic(this, 1, 2);

	//Show each cell
	m_spliter.CreateView(0, 0, RUNTIME_CLASS(CSelectView), CSize(300, 1000), pContext);
	m_spliter.CreateView(0, 1, RUNTIME_CLASS(CDisplayView), CSize(1500, 1000), pContext);

	return TRUE; //split not by default
}

LRESULT CMainFrame::OnMyChange(WPARAM wParam, LPARAM lParam)
{
	CCreateContext Context;
	if (wParam == NM_HOME)
	{
		Context.m_pNewViewClass = RUNTIME_CLASS(CHomeDlg);
		Context.m_pCurrentFrame = this;
		Context.m_pLastView = (CFormView*)m_spliter.GetPane(0, 1);
		m_spliter.DeleteView(0, 1);
		m_spliter.CreateView(0, 1, RUNTIME_CLASS(CHomeDlg), CSize(1800, 1000), &Context);
		CHomeDlg* pNewView = (CHomeDlg*)m_spliter.GetPane(0, 1);
		m_spliter.RecalcLayout();
		pNewView->OnInitialUpdate();
		m_spliter.SetActivePane(0, 1);
	}
	else if (wParam == NM_A)
	{
		Context.m_pNewViewClass = RUNTIME_CLASS(CPatientRecordDlg);
		Context.m_pCurrentFrame = this;
		Context.m_pLastView = (CFormView*)m_spliter.GetPane(0, 1);
		m_spliter.DeleteView(0, 1);
		m_spliter.CreateView(0, 1, RUNTIME_CLASS(CPatientRecordDlg), CSize(1800, 1000), &Context);
		CPatientRecordDlg* pNewView = (CPatientRecordDlg*)m_spliter.GetPane(0, 1);
		m_spliter.RecalcLayout();
		pNewView->OnInitialUpdate();
		m_spliter.SetActivePane(0, 1);
	}
	else if (wParam == NM_B)
	{
		Context.m_pNewViewClass = RUNTIME_CLASS(CDevicesSettingDlg);
		Context.m_pCurrentFrame = this;
		Context.m_pLastView = (CFormView*)m_spliter.GetPane(0, 1);
		m_spliter.DeleteView(0, 1);
		m_spliter.CreateView(0, 1, RUNTIME_CLASS(CDevicesSettingDlg), CSize(1800, 1000), &Context);
		CDevicesSettingDlg* pNewView = (CDevicesSettingDlg*)m_spliter.GetPane(0, 1);
		m_spliter.RecalcLayout();
		pNewView->OnInitialUpdate();
		m_spliter.SetActivePane(0, 1);
	}
	else if (wParam == NM_C)
	{
		Context.m_pNewViewClass = RUNTIME_CLASS(CWakeUpSettingDlg);
		Context.m_pCurrentFrame = this;
		Context.m_pLastView = (CFormView*)m_spliter.GetPane(0, 1);
		m_spliter.DeleteView(0, 1);
		m_spliter.CreateView(0, 1, RUNTIME_CLASS(CWakeUpSettingDlg), CSize(1800, 1000), &Context);
		CWakeUpSettingDlg* pNewView = (CWakeUpSettingDlg*)m_spliter.GetPane(0, 1);
		m_spliter.RecalcLayout();
		pNewView->OnInitialUpdate();
		m_spliter.SetActivePane(0, 1);
	}
	return 0;
}
