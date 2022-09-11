/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"github.com/GeniusesGroup/libgo/protocol"
)

type QuiddityMediaStatus interface {
	QuiddityID() [16]byte         // quiddity domain. any domain e.g. user, ...
	ObjectID() [16]byte           // object domain. media file
	Status() QuiddityMedia_Status //
	Time() protocol.Time          // save time
	RequestID() UserRequestUUID   // user-request domain
}

type QuiddityMediaStatus_StorageServices interface {
	Save(q QuiddityMediaStatus) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(quiddityID, objectID [16]byte) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(quiddityID, objectID [16]byte, vo protocol.VersionOffset) (q QuiddityMediaStatus, nv protocol.NumberOfVersion, err protocol.Error)
}

type QuiddityMedia_Status Quiddity_Status

const (
// QuiddityMedia_Status_ QuiddityMedia_Status = (Quiddity_Status_FreeFlag << iota)
)
