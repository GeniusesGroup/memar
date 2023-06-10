/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"

	urp "org/modules/user-request/protocol"
	up "org/modules/user/protocol"
)

// use to get and show locale title from quiddity-title domain.
type ProjectUUID = protocol.UUID

// Project indicate the domain record data fields.
type Project interface {
	ProjectID() ProjectUUID         //
	UserID() up.UserUUID            //
	Time() protocol.Time            // Save time
	RequestID() urp.UserRequestUUID //
}

type Project_StorageServices interface {
	Save(dm Project) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(projectID ProjectUUID) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(projectID ProjectUUID, vo protocol.VersionOffset) (dm Project, nv protocol.NumberOfVersion, err protocol.Error)

	FIND_UserIDs_By_ProjectID(projectID ProjectUUID, offset, limit uint64) (userIDs []up.UserUUID, nv protocol.NumberOfVersion, err protocol.Error)
}
