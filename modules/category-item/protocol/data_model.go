/* For license and copyright information please see the LEGAL file in the code repository */

package cip


import (
	"libgo/protocol"

	urp "org/modules/user-request/protocol"
	cp "org/modules/category/protocol"
)

type DataModel interface {
	CategoryID() cp.CategoryUUID       //
	Priority() uint64               //
	ItemID() [16]byte               // any domain usually product, content, ... domain
	SaveTime() protocol.Time        //
	RequestID() urp.UserRequestUUID //
}


