/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"
)

type QuiddityMedia interface {
	QuiddityID() [16]byte       // quiddity domain. any domain e.g. user, ...
	Priority() uint64           // Media priority
	ObjectID() [16]byte         // object domain
	Time() protocol.Time        // save time
	RequestID() UserRequestUUID // user-request domain
}

type QuiddityMedia_StorageServices interface {
	Save(p QuiddityMedia) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(quiddityID [16]byte, priority uint64) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(quiddityID [16]byte, priority uint64, vo protocol.VersionOffset) (p QuiddityMedia, nv protocol.NumberOfVersion, err protocol.Error)

	ListMedias(quiddityID [16]byte, offset, limit uint64) (objectIDs [][16]byte, nv protocol.NumberOfVersion, err protocol.Error)
	ListRelates(objectID [16]byte, offset, limit uint64) (quiddityIDs [][16]byte, nv protocol.NumberOfVersion, err protocol.Error)
	ListPriorities(objectID, quiddityID [16]byte, offset, limit uint64) (priorities []uint64, nv protocol.NumberOfVersion, err protocol.Error)
}
