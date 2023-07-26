/* For license and copyright information please see the LEGAL file in the code repository */

package ftp

import (
	"memar/protocol"

	fap "org/modules/financial-account/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	AccountID() fap.FinancialAccountUUID
	AccountOffset() protocol.NumberOfVersion
	Label() ReferenceType

	protocol.AuditLogging
	protocol.Storage_Versioned
	protocol.Storage_SaveTime
}
