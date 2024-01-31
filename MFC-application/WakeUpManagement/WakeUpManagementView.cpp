
// WakeUpManagementView.cpp : implementation of the CWakeUpManagementView class
//

#include "pch.h"
#include "framework.h"
// SHARED_HANDLERS can be defined in an ATL project implementing preview, thumbnail
// and search filter handlers and allows sharing of document code with that project.
#ifndef SHARED_HANDLERS
#include "WakeUpManagement.h"
#endif

#include "WakeUpManagementDoc.h"
#include "WakeUpManagementView.h"

#ifdef _DEBUG
#define new DEBUG_NEW
#endif


// CWakeUpManagementView

IMPLEMENT_DYNCREATE(CWakeUpManagementView, CView)

BEGIN_MESSAGE_MAP(CWakeUpManagementView, CView)
	// Standard printing commands
	ON_COMMAND(ID_FILE_PRINT, &CView::OnFilePrint)
	ON_COMMAND(ID_FILE_PRINT_DIRECT, &CView::OnFilePrint)
	ON_COMMAND(ID_FILE_PRINT_PREVIEW, &CView::OnFilePrintPreview)
END_MESSAGE_MAP()

// CWakeUpManagementView construction/destruction

CWakeUpManagementView::CWakeUpManagementView() noexcept
{
	// TODO: add construction code here

}

CWakeUpManagementView::~CWakeUpManagementView()
{
}

BOOL CWakeUpManagementView::PreCreateWindow(CREATESTRUCT& cs)
{
	// TODO: Modify the Window class or styles here by modifying
	//  the CREATESTRUCT cs

	return CView::PreCreateWindow(cs);
}

// CWakeUpManagementView drawing

void CWakeUpManagementView::OnDraw(CDC* /*pDC*/)
{
	CWakeUpManagementDoc* pDoc = GetDocument();
	ASSERT_VALID(pDoc);
	if (!pDoc)
		return;

	// TODO: add draw code for native data here
}


// CWakeUpManagementView printing

BOOL CWakeUpManagementView::OnPreparePrinting(CPrintInfo* pInfo)
{
	// default preparation
	return DoPreparePrinting(pInfo);
}

void CWakeUpManagementView::OnBeginPrinting(CDC* /*pDC*/, CPrintInfo* /*pInfo*/)
{
	// TODO: add extra initialization before printing
}

void CWakeUpManagementView::OnEndPrinting(CDC* /*pDC*/, CPrintInfo* /*pInfo*/)
{
	// TODO: add cleanup after printing
}


// CWakeUpManagementView diagnostics

#ifdef _DEBUG
void CWakeUpManagementView::AssertValid() const
{
	CView::AssertValid();
}

void CWakeUpManagementView::Dump(CDumpContext& dc) const
{
	CView::Dump(dc);
}

CWakeUpManagementDoc* CWakeUpManagementView::GetDocument() const // non-debug version is inline
{
	ASSERT(m_pDocument->IsKindOf(RUNTIME_CLASS(CWakeUpManagementDoc)));
	return (CWakeUpManagementDoc*)m_pDocument;
}
#endif //_DEBUG


// CWakeUpManagementView message handlers
