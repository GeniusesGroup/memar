/* For license and copyright information please see the LEGAL file in the code repository */

package faip

import (
	"libgo/iso"
	"libgo/protocol"

	fap "org/modules/financial-account/protocol"
)

type (
	BS_Register_Request interface {
		AccountID() fap.FinancialAccountUUID
		IBAN() iso.IBAN
	}
)

type (
	BS_Get_Request interface {
		AccountID() fap.FinancialAccountUUID
		VersionOffset() protocol.VersionOffset
	}
	BS_Get_Response interface {
		DataModel

		Numbers() uint64
	}
)
