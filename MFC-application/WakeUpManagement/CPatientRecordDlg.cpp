// CPatientRecordDlg.cpp : implementation file
//

#include "pch.h"
#include "WakeUpManagement.h"
#include "CPatientRecordDlg.h"


// CPatientRecordDlg

IMPLEMENT_DYNCREATE(CPatientRecordDlg, CFormView)

CPatientRecordDlg::CPatientRecordDlg()
	: CFormView(IDD_DIALOG_PATIENT_RECORD)
{

}

CPatientRecordDlg::~CPatientRecordDlg()
{
}

void CPatientRecordDlg::DoDataExchange(CDataExchange* pDX)
{
	CFormView::DoDataExchange(pDX);
	DDX_Control(pDX, IDC_LIST1, m_patient_record);
}

BEGIN_MESSAGE_MAP(CPatientRecordDlg, CFormView)
END_MESSAGE_MAP()


// CPatientRecordDlg diagnostics

#ifdef _DEBUG
void CPatientRecordDlg::AssertValid() const
{
	CFormView::AssertValid();
}

#ifndef _WIN32_WCE
void CPatientRecordDlg::Dump(CDumpContext& dc) const
{
	CFormView::Dump(dc);
}
#endif
#endif //_DEBUG


// CPatientRecordDlg message handlers


void CPatientRecordDlg::OnInitialUpdate()
{
	CFormView::OnInitialUpdate();


	// Creates a 12-point-Courier-font
	m_Title_Font.CreatePointFont(120, _T("Calibri"));
	GetDlgItem(IDC_STATIC)->SetFont(&m_Title_Font);


	m_Table_Font.CreatePointFont(100, _T("Calibri"));
	m_patient_record.SetFont(&m_Table_Font);

	// TODO: Add your specialized code here and/or call the base class
	CString str[] = { TEXT("Name"), TEXT("Gender"), TEXT("DOB"), TEXT("Vision/Sound") };
	for (int i = 0; i < 4; i++) {
		//title
		m_patient_record.InsertColumn(i, str[i], LVCFMT_LEFT, 200);
	}

	CString NameArray[10] = { TEXT("budz"), TEXT("pain"), TEXT("konan"), TEXT("nagato"), TEXT("itachi"), TEXT("tobi"), TEXT("madara"), TEXT("naruto"), TEXT("danzou"), TEXT("kakashi") };

	for (int i = 0; i < 10; i++) {
		int j = 0;
		m_patient_record.InsertItem(i, NameArray[i]);
		m_patient_record.SetItemText(i, ++j, TEXT("Female"));
		m_patient_record.SetItemText(i, ++j, TEXT("22/1/1990"));
		m_patient_record.SetItemText(i, ++j, TEXT("Vision"));
	}

	//property (show table lines)
	m_patient_record.SetExtendedStyle(m_patient_record.GetExtendedStyle() | LVS_EX_FULLROWSELECT | LVS_EX_GRIDLINES);

}
