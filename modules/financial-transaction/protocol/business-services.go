/* For license and copyright information please see the LEGAL file in the code repository */

package ftp

import (
	fap "org/modules/financial-account/protocol"
)

type (
	BS_Transfer_Request interface{}
)

type (
	BS_RecoverTransfer_Request interface{}
)

type (
	BS_Get_Request interface {
		AccountID() fap.FinancialAccountUUID
	}
)

type (
	BS_GetByTime_Request interface{}
)

type (
	BS_Find_Request interface{}
)
