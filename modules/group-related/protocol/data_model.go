/* For license and copyright information please see the LEGAL file in the code repository */

package grp

import (
	"libgo/protocol"

	gp "org/modules/group/protocol"
	qsp "org/modules/quiddity-status/protocol"
	urp "org/modules/user-request/protocol"
)

// GroupRelated indicate the domain record data fields.
type GroupRelated interface {
	GroupID() gp.GroupUUID          //
	RelatedGroupID() gp.GroupUUID   // Use to categorize and graph groups
	Status() Status                 //
	SaveTime() protocol.Time        //
	RequestID() urp.UserRequestUUID //
}

type Status qsp.Quiddity_Status
