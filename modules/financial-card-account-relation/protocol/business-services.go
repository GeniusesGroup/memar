/* For license and copyright information please see the LEGAL file in the code repository */

package fcarp

import (
	"libgo/protocol"
)

type (
	BS_Register_Request interface {
		AccountID() [16]byte
		FinancialCardID() [16]byte
		Priority() uint64
		Status() Status
	}
)

type (
	BS_Get_Request interface {
		AccountID() [16]byte
		FinancialCardID() [16]byte
		VersionOffset() protocol.VersionOffset
	}
	BS_Get_Response1 = FinancialCardAccountRelation
	BS_Get_Response2 = protocol.VersionOffset
)
