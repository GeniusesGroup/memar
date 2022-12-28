/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"
)

type LawStatus interface {
	LawID() [16]byte            // LawID
	Status() Law_Status         //
	Time() protocol.Time        // save time
	RequestID() UserRequestUUID // user-request domain
}

type LawStatus_StorageServices interface {
	Save(ls LawStatus) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(lawID [16]byte) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(lawID [16]byte, vo protocol.VersionOffset) (ls LawStatus, nv protocol.NumberOfVersion, err protocol.Error)

	// FilterByStatus(status Law_Status, offset, limit uint64) (lawIDs [][16]byte, nv protocol.NumberOfVersion, err protocol.Error)

	// protocol.EventTarget
}

type Law_Status Quiddity_Status

const (
	Law_Status_Suggestion = Law_Status(Quiddity_Status_FreeFlag << iota)
	Law_Status_Closed
	Law_Status_Approved
	Law_Status_Denied
)
