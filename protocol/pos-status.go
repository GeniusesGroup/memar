/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"

	urp "org/modules/user-request/protocol"
)

// PosStatus indicate the domain record data fields.
type PosStatus interface {
	PosID() PosUUID                 //
	Status() Pos_Status             //
	Time() protocol.Time            // save time
	RequestID() urp.UserRequestUUID //
}

type PosStatus_StorageServices interface {
	Save(ps PosStatus) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(posID PosUUID) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(posID PosUUID, vo protocol.VersionOffset) (ps PosStatus, nv protocol.NumberOfVersion, err protocol.Error)

	FilterByStatus(status Pos_Status, offset, limit uint64) (posIDs []PosUUID, nv protocol.NumberOfVersion, err protocol.Error)

	protocol.EventTarget
}

type Pos_Status Quiddity_Status

const (
	Pos_Status_CashLimitInactivated = Pos_Status(Quiddity_Status_FreeFlag << iota)
)
