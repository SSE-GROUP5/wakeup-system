// CSelectView.cpp : implementation file
//

#include "pch.h"
#include "WakeUpManagement.h"
#include "CSelectView.h"
#include "MainFrm.h"


// CSelectView

IMPLEMENT_DYNCREATE(CSelectView, CTreeView)

CSelectView::CSelectView()
{

}

CSelectView::~CSelectView()
{
}

BEGIN_MESSAGE_MAP(CSelectView, CTreeView)
	ON_NOTIFY_REFLECT(TVN_SELCHANGED, &CSelectView::OnTvnSelchanged)
END_MESSAGE_MAP()


// CSelectView diagnostics

#ifdef _DEBUG
void CSelectView::AssertValid() const
{
	CTreeView::AssertValid();
}

#ifndef _WIN32_WCE
void CSelectView::Dump(CDumpContext& dc) const
{
	CTreeView::Dump(dc);
}
#endif
#endif //_DEBUG


// CSelectView message handlers


void CSelectView::OnInitialUpdate()
{
	CTreeView::OnInitialUpdate();

	// TODO: Add your specialized code here and/or call the base class

	//Initialize Tree View
	//Get TreeCtrl
	m_treeCtrl = &GetTreeCtrl();

	//Add Image List

	HICON icon = AfxGetApp()->LoadIconW(IDI_ICON_ARROW);

	m_imageList.Create(30, 30, ILC_COLOR32, 1, 1);
	m_imageList.Add(icon);

	m_treeCtrl->SetImageList(&m_imageList, TVSIL_NORMAL);
	m_treeCtrl->SetItemHeight(60);

	//Add Node
	m_treeCtrl->InsertItem(TEXT("Home"), 0, 0, NULL);
	m_treeCtrl->InsertItem(TEXT("Patient Record"), 0, 0, NULL);
	m_treeCtrl->InsertItem(TEXT("Devices"), 0, 0, NULL);
	m_treeCtrl->InsertItem(TEXT("Wake Up Setting"), 0, 0, NULL);
}


void CSelectView::OnTvnSelchanged(NMHDR* pNMHDR, LRESULT* pResult)
{
	LPNMTREEVIEW pNMTreeView = reinterpret_cast<LPNMTREEVIEW>(pNMHDR);
	// TODO: Add your control notification handler code here
	*pResult = 0;

	//Get Current Selected
	HTREEITEM item = m_treeCtrl->GetSelectedItem();
	CString str = m_treeCtrl->GetItemText(item);

	if (str == TEXT("Home"))
	{
		//::means api, because selectView send message to MainFrame which are different windows
		::PostMessage(AfxGetMainWnd()->GetSafeHwnd(), NM_HOME, (WPARAM)NM_HOME, (LPARAM)0);
	}
	else if (str == TEXT("Patient Record"))
	{
		//::means api, because selectView send message to MainFrame which are different windows
		::PostMessage(AfxGetMainWnd()->GetSafeHwnd(), NM_A, (WPARAM)NM_A, (LPARAM)0);
	} 
	else if (str == TEXT("Devices"))
	{
		::PostMessage(AfxGetMainWnd()->GetSafeHwnd(), NM_B, (WPARAM)NM_B, (LPARAM)0);
	}
	else if (str == TEXT("Wake Up Setting"))
	{
		::PostMessage(AfxGetMainWnd()->GetSafeHwnd(), NM_C, (WPARAM)NM_C, (LPARAM)0);
	}
}
