// CHomeDlg.cpp : implementation file
//

#include "pch.h"
#include "WakeUpManagement.h"
#include "CHomeDlg.h"


// CHomeDlg

IMPLEMENT_DYNCREATE(CHomeDlg, CFormView)

CHomeDlg::CHomeDlg()
	: CFormView(IDD_HOME)
{

}

CHomeDlg::~CHomeDlg()
{
}

void CHomeDlg::DoDataExchange(CDataExchange* pDX)
{
	CFormView::DoDataExchange(pDX);
}

BEGIN_MESSAGE_MAP(CHomeDlg, CFormView)
END_MESSAGE_MAP()


// CHomeDlg diagnostics

#ifdef _DEBUG
void CHomeDlg::AssertValid() const
{
	CFormView::AssertValid();
}

#ifndef _WIN32_WCE
void CHomeDlg::Dump(CDumpContext& dc) const
{
	CFormView::Dump(dc);
}
#endif
#endif //_DEBUG


// CHomeDlg message handlers


void CHomeDlg::OnInitialUpdate()
{
	CFormView::OnInitialUpdate();

	// TODO: Add your specialized code here and/or call the base class

	m_Font.CreatePointFont(300, _T("Calibri"));
	GetDlgItem(IDC_STATIC)->SetFont(&m_Font);
}
