/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"

	urp "org/modules/user-request/protocol"
)

type LawStatus interface {
	LawID() LawUUID                 //
	Status() Law_Status             //
	Time() protocol.Time            // save time
	RequestID() urp.UserRequestUUID //
}

type LawStatus_StorageServices interface {
	Save(ls LawStatus) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(lawID LawUUID) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(lawID LawUUID, vo protocol.VersionOffset) (ls LawStatus, nv protocol.NumberOfVersion, err protocol.Error)

	// FilterByStatus(status Law_Status, offset, limit uint64) (lawIDs []LawUUID, nv protocol.NumberOfVersion, err protocol.Error)

	// protocol.EventTarget
}

type Law_Status Quiddity_Status

const (
	Law_Status_Suggestion = Law_Status(Quiddity_Status_FreeFlag << iota)
	Law_Status_Closed
	Law_Status_Approved
	Law_Status_Denied
)
