/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"

	urp "org/modules/user-request/protocol"
)

type CategoryStatus interface {
	CategoryID() CategoryUUID       //
	Status() Category_Status        //
	Time() protocol.Time            // save time
	RequestID() urp.UserRequestUUID //
}

type CategoryStatus_StorageServices interface {
	Save(dm CategoryStatus) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(categoryID CategoryUUID) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(categoryID CategoryUUID, vo protocol.VersionOffset) (dm CategoryStatus, nv protocol.NumberOfVersion, err protocol.Error)

	FILTER_CategoryIDs_BY_Status(status Category_Status, offset, limit uint64) (categoryIDs []CategoryUUID, nv protocol.NumberOfVersion, err protocol.Error)

	protocol.EventTarget
}

type Category_Status Quiddity_Status

const (
// Category_Status_ = Category_Status(Quiddity_Status_FreeFlag << iota)
)
