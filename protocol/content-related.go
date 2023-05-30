/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"

	urp "org/modules/user-request/protocol"
)

type ContentRelated interface {
	ContentID() ContentUUID         //
	Priority() uint64               // substitute priority
	PriorityType() ContentTypeUUID  //
	RelatedID() ContentUUID         //
	UserID() UserUUID               //
	Time() protocol.Time            // save time
	RequestID() urp.UserRequestUUID //
}
