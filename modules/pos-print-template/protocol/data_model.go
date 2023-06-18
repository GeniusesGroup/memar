/* For license and copyright information please see the LEGAL file in the code repository */

package pptp

import (
	"libgo/protocol"

	urp "org/modules/user-request/protocol"
	pp "org/modules/pos/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	PosID() pp.PosUUID //
	// TODO::: VAT number, store address, logo, return rule, ...
	SaveTime() protocol.Time        //
	RequestID() urp.UserRequestUUID //
}

// sabz.city/complaints?tel=xxxxxxxxxx&orgID=xxx
