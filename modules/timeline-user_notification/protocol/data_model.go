/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"

	gp "org/modules/group/protocol"
	urp "org/modules/user-request/protocol"
	up "org/modules/user/protocol"
)

// DataModel is UserNotificationTimeline domain record data fields.
type DataModel interface {
	UserID() up.UserUUID            //
	GroupID() gp.GroupUUID          // generate for group & comment domain
	SaveTime() protocol.Time        //
	RequestID() urp.UserRequestUUID //
}

type UserTimeline_StorageServices interface {
	Save(dm DataModel) (nv protocol.NumberOfVersion, err protocol.Error)

	Get(userID up.UserUUID) (dm DataModel, err protocol.Error)
}
