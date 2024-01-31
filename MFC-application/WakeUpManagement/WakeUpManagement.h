
// WakeUpManagement.h : main header file for the WakeUpManagement application
//
#pragma once

#ifndef __AFXWIN_H__
	#error "include 'pch.h' before including this file for PCH"
#endif

#include "resource.h"       // main symbols


// CWakeUpManagementApp:
// See WakeUpManagement.cpp for the implementation of this class
//

class CWakeUpManagementApp : public CWinApp
{
public:
	CWakeUpManagementApp() noexcept;


// Overrides
public:
	virtual BOOL InitInstance();
	virtual int ExitInstance();

// Implementation
	afx_msg void OnAppAbout();
	DECLARE_MESSAGE_MAP()
};

extern CWakeUpManagementApp theApp;
