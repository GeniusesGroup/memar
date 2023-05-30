/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"

	urp "org/modules/user-request/protocol"
)

// PosPrintTemplate indicate the domain record data fields.
type PosPrintTemplate interface {
	PosID() PosUUID //
	// TODO::: VAT number, store address, logo, return rule, ...
	Time() protocol.Time            // save time
	RequestID() urp.UserRequestUUID //
}

// sabz.city/complaints?tel=xxxxxxxxxx&orgID=xxx
