/* For license and copyright information please see the LEGAL file in the code repository */

package pup

import (
	"memar/protocol"

	pp "org/modules/product/protocol"
	up "org/modules/user/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	SubscriptionID() pp.ProductUUID //
	UserID() up.UserUUID            //

	// protocol.AuditLogging
	protocol.Storage_Versioned
	protocol.Storage_SaveTime
}
