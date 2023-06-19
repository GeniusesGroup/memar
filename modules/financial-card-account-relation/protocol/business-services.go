/* For license and copyright information please see the LEGAL file in the code repository */

package fcarp

import (
	"libgo/protocol"

	fap "org/modules/financial-account/protocol"
	fcp "org/modules/financial-card/protocol"
)

type (
	BS_Register_Request interface {
		AccountID() fap.FinancialAccountUUID
		FinancialCardID() fcp.FinancialCardUUID
		Priority() uint64
		Status() Status
	}
)

type (
	BS_Get_Request interface {
		AccountID() fap.FinancialAccountUUID
		FinancialCardID() fcp.FinancialCardUUID
		VersionOffset() protocol.VersionOffset
	}
	BS_Get_Response1 = DataModel
	BS_Get_Response2 = protocol.VersionOffset
)
