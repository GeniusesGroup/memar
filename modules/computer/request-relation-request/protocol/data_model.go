/* For license and copyright information please see the LEGAL file in the code repository */

package arrrp

import (
	aap "org/modules/app-audit/protocol"
	sp "org/modules/storage/protocol"
)

// DataModel indicates the domain record data fields.
type DataModel interface {
	aap.AuditRequest
	SideRequestID() aap.RequestUUID
	Reason() Reason

	sp.SaveTime
}
