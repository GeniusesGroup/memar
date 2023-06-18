/* For license and copyright information please see the LEGAL file in the code repository */

package pp

import (
	"libgo/protocol"

	urp "org/modules/user-request/protocol"
)

// DataModel indicate the domain record data fields.
// POS or point-of-sale
type DataModel interface {
	PosID() PosUUID                 //
	Type() Type                     //
	SaveTime() protocol.Time        //
	RequestID() urp.UserRequestUUID //
}

type Type uint64

// Common flags
const (
	Type_Unset Type = 0
	Type_Cash  Type = (1 << iota)
	Type_Location
	Type_Provider
	Type_Product
	// Type_
)
