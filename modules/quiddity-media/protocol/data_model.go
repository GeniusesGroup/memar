/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"

	urp "org/modules/user-request/protocol"
)

type QuiddityMedia interface {
	QuiddityID() QuiddityUUID       //
	Priority() uint64               // Media priority
	ObjectID() ObjectUUID           //
	Time() protocol.Time            // save time
	RequestID() urp.UserRequestUUID //
}

type QuiddityMedia_StorageServices interface {
	Save(p QuiddityMedia) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(quiddityID QuiddityUUID, priority uint64) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(quiddityID QuiddityUUID, priority uint64, vo protocol.VersionOffset) (p QuiddityMedia, nv protocol.NumberOfVersion, err protocol.Error)

	ListMedias(quiddityID QuiddityUUID, offset, limit uint64) (objectIDs []ObjectUUID, nv protocol.NumberOfVersion, err protocol.Error)
	ListRelates(objectID ObjectUUID, offset, limit uint64) (quiddityIDs []QuiddityUUID, nv protocol.NumberOfVersion, err protocol.Error)
	ListPriorities(objectID ObjectUUID, quiddityID QuiddityUUID, offset, limit uint64) (priorities []uint64, nv protocol.NumberOfVersion, err protocol.Error)
}
