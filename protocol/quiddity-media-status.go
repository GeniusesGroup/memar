/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"

	urp "org/modules/user-request/protocol"
)

type QuiddityMediaStatus interface {
	QuiddityID() QuiddityUUID       //
	ObjectID() ObjectUUID           // media file
	Status() QuiddityMedia_Status   //
	Time() protocol.Time            // save time
	RequestID() urp.UserRequestUUID //
}

type QuiddityMediaStatus_StorageServices interface {
	Save(q QuiddityMediaStatus) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(quiddityID QuiddityUUID, objectID ObjectUUID) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(quiddityID QuiddityUUID, objectID ObjectUUID, vo protocol.VersionOffset) (q QuiddityMediaStatus, nv protocol.NumberOfVersion, err protocol.Error)
}

type QuiddityMedia_Status Quiddity_Status

const (
// QuiddityMedia_Status_ QuiddityMedia_Status = (Quiddity_Status_FreeFlag << iota)
)
