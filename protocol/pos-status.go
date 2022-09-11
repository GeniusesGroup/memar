/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"github.com/GeniusesGroup/libgo/protocol"
)

// PosStatus indicate the domain record data fields.
type PosStatus interface {
	PosID() [16]byte            // pos domain
	Status() Pos_Status         //
	Time() protocol.Time        // save time
	RequestID() UserRequestUUID // user-request domain
}

type PosStatus_StorageServices interface {
	Save(ps PosStatus) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(posID [16]byte) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(posID [16]byte, vo protocol.VersionOffset) (ps PosStatus, nv protocol.NumberOfVersion, err protocol.Error)

	FilterByStatus(status Pos_Status, offset, limit uint64) (posIDs [][16]byte, nv protocol.NumberOfVersion, err protocol.Error)

	protocol.EventTarget
}

type Pos_Status Quiddity_Status

const (
	Pos_Status_CashLimitInactivated = Pos_Status(Quiddity_Status_FreeFlag << iota)
)
