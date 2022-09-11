/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"github.com/GeniusesGroup/libgo/protocol"
)

type AreaStatus interface {
	AreaID() [16]byte           // quiddity domain
	Status() Area_Status        //
	Time() protocol.Time        // save time
	RequestID() UserRequestUUID // user-request domain
}

type AreaStatus_StorageServices interface {
	Save(as AreaStatus) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(areaID [16]byte) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(areaID [16]byte, vo protocol.VersionOffset) (as AreaStatus, nv protocol.NumberOfVersion, err protocol.Error)

	FilterByStatus(status Area_Status, offset, limit uint64) (areaIDs [][16]byte, err protocol.Error)

	// protocol.EventTarget
}

type Area_Status Quiddity_Status

const (
	Area_Status_NeighborsConflict = Area_Status(Quiddity_Status_FreeFlag << iota)
)
