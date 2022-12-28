/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"
)

// POS indicate the domain record data fields.
// POS or point-of-sale
type POS interface {
	PosID() [16]byte            // quiddity domain
	Type() POS_Type             //
	Time() protocol.Time        // save time
	RequestID() UserRequestUUID // user-request domain
}

type POS_StorageServices interface {
	Save(pos POS) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(posID [16]byte) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(posID [16]byte, vo protocol.VersionOffset) (pos POS, nv protocol.NumberOfVersion, err protocol.Error)
}

type POS_Type uint64

// Common flags
const (
	POS_Type_Unset POS_Type = 0
	POS_Type_Cash  POS_Type = (1 << iota)
	POS_Type_Location
	POS_Type_Provider
	POS_Type_Product
	// POS_Type_
)
