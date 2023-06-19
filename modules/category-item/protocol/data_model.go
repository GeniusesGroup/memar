/* For license and copyright information please see the LEGAL file in the code repository */

package cip

import (
	"libgo/protocol"

	cp "org/modules/category/protocol"
	urp "org/modules/user-request/protocol"
)

type DataModel interface {
	CategoryID() cp.CategoryUUID    //
	Priority() uint64               //
	ItemID() protocol.UUID          // any domain usually product, content, ... domain
	SaveTime() protocol.Time        //
	RequestID() urp.UserRequestUUID //
}
