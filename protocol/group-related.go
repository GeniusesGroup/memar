/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"

	urp "org/modules/user-request/protocol"
)

// GroupRelated indicate the domain record data fields.
type GroupRelated interface {
	GroupID() GroupUUID             //
	RelatedGroupID() GroupUUID      // Use to categorize and graph groups
	Time() protocol.Time            // save time
	RequestID() urp.UserRequestUUID //
}
