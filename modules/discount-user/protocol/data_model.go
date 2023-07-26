/* For license and copyright information please see the LEGAL file in the code repository */

package dup

import (
	"memar/protocol"

	dp "org/modules/discount/protocol"
	up "org/modules/user/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	DiscountID() dp.DiscountUUID //
	UserID() up.UserUUID         //

	protocol.AuditLogging
	protocol.Storage_Versioned
	protocol.Storage_SaveTime
}
