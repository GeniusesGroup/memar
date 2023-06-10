/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"

	urp "org/modules/user-request/protocol"
)

// Also can be used in quiddity domains to set title, ...
type PosUUID = protocol.UUID

// POS indicate the domain record data fields.
// POS or point-of-sale
type POS interface {
	PosID() PosUUID                 //
	Type() POS_Type                 //
	Time() protocol.Time            // save time
	RequestID() urp.UserRequestUUID //
}

type POS_StorageServices interface {
	Save(dm POS) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(posID PosUUID) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(posID PosUUID, vo protocol.VersionOffset) (dm POS, nv protocol.NumberOfVersion, err protocol.Error)

	FILTER_PosIDs_BY_Type(t POS_Type, offset, limit uint64) (posIDs []PosUUID, nv protocol.NumberOfVersion, err protocol.Error)
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
