/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"

	urp "org/modules/user-request/protocol"
)

type PictureStatus interface {
	ObjectID() ObjectUUID           //
	Status() Object_Status          //
	Time() protocol.Time            // save time
	RequestID() urp.UserRequestUUID //
}

type PictureStatus_StorageServices interface {
	Save(ps PictureStatus) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(objectID [16]byte) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(objectID [16]byte, vo protocol.VersionOffset) (ps PictureStatus, nv protocol.NumberOfVersion, err protocol.Error)

	// FilterByStatus(status Object_Status, offset, limit uint64) (objectIDs [][16]byte, nv protocol.NumberOfVersion, err protocol.Error)

	// protocol.EventTarget
}

type Object_Status Quiddity_Status

const (
// Object_Status_ Object_Status = (Quiddity_Status_FreeFlag << iota)
)
