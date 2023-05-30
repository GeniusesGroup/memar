/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"

	urp "org/modules/user-request/protocol"
)

// QuiddityOwner indicate the domain record data fields.
type QuiddityOwner interface {
	QuiddityID() QuiddityUUID       //
	UserID() UserUUID               // Owner of the quiddity
	Time() protocol.Time            // save time
	RequestID() urp.UserRequestUUID //
}

type QuiddityOwner_StorageServices interface {
	Save(qo QuiddityOwner) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(quiddityID QuiddityUUID) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(quiddityID QuiddityUUID, vo protocol.VersionOffset) (qo QuiddityOwner, nv protocol.NumberOfVersion, err protocol.Error)

	FindByOwnerID(userID UserUUID, offset, limit uint64) (quiddityIDs []QuiddityUUID, nv protocol.NumberOfVersion, err protocol.Error)
}

type QuiddityOwner_Service_FindByUserID_Request interface {
	UserID() UserUUID
	Offset() uint64
	Limit() uint64
}
type QuiddityOwner_Service_FindByUserID_Response interface {
	QuiddityIDs() []QuiddityUUID
	Numbers() uint64
}
