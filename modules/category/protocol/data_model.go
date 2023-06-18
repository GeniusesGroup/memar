/* For license and copyright information please see the LEGAL file in the code repository */

package cp

import (
	"libgo/protocol"

	urp "org/modules/user-request/protocol"
)

// DataModel indicate the domain record data fields.
// DataModel or Topic
type DataModel interface {
	CategoryID() CategoryUUID    // quiddity domain
	ParentID() CategoryUUID      // Exist if it isn't top category.
	SaveTime() protocol.Time        //
	RequestID() urp.UserRequestUUID //
}
