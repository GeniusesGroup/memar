/* For license and copyright information please see the LEGAL file in the code repository */

package fcp

import (
	"memar/iso"
	"memar/protocol"

	up "org/modules/user/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	FinancialCardID() FinancialCardUUID
	Issuer() up.UserUUID //, any org user
	UserID() up.UserUUID //, owner of the card
	CardNumber() iso.Card
	ExpireDate() protocol.Time
	CVC() uint16

	protocol.AuditLogging
	protocol.Storage_Versioned
	protocol.Storage_SaveTime
}
