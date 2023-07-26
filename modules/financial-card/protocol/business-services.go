/* For license and copyright information please see the LEGAL file in the code repository */

package fcp

import (
	"memar/iso"
	"memar/protocol"

	fap "org/modules/financial-account/protocol"
)

type (
	BS_Register_Request interface {
		AccountID() fap.FinancialAccountUUID
		CardNumber() iso.Card
		ExpireDate() protocol.Time
		CVC() uint16
	}
)

type (
	BS_Get_Request interface {
		AccountID() fap.FinancialAccountUUID
		VersionOffset() protocol.VersionOffset
	}
	BS_Get_Response1 = DataModel
	BS_Get_Response2 = protocol.NumberOfVersion
)
