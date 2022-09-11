/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"github.com/GeniusesGroup/libgo/protocol"
)

type CategoryStatus interface {
	CategoryID() [16]byte       // category domain
	Status() Category_Status    //
	Time() protocol.Time        // save time
	RequestID() UserRequestUUID // user-request domain
}

type CategoryStatus_StorageServices interface {
	Save(gs CategoryStatus) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(categoryID [16]byte) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(categoryID [16]byte, vo protocol.VersionOffset) (gs CategoryStatus, nv protocol.NumberOfVersion, err protocol.Error)

	FilterByStatus(status Category_Status, offset, limit uint64) (categoryIDs [][16]byte, err protocol.Error)

	// protocol.EventTarget
}

type Category_Status Quiddity_Status

const (
// Category_Status_ = Category_Status(Quiddity_Status_FreeFlag << iota)
)
