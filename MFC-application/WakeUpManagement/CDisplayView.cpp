// CDisplayView.cpp : implementation file
//

#include "pch.h"
#include "WakeUpManagement.h"
#include "CDisplayView.h"


// CDisplayView

IMPLEMENT_DYNCREATE(CDisplayView, CFormView)

CDisplayView::CDisplayView()
	: CFormView(IDD_CDisplayView)
{

}

CDisplayView::~CDisplayView()
{
}

void CDisplayView::DoDataExchange(CDataExchange* pDX)
{
	CFormView::DoDataExchange(pDX);
}

BEGIN_MESSAGE_MAP(CDisplayView, CFormView)
END_MESSAGE_MAP()


// CDisplayView diagnostics

#ifdef _DEBUG
void CDisplayView::AssertValid() const
{
	CFormView::AssertValid();
}

#ifndef _WIN32_WCE
void CDisplayView::Dump(CDumpContext& dc) const
{
	CFormView::Dump(dc);
}
#endif
#endif //_DEBUG


// CDisplayView message handlers
