/* For license and copyright information please see the LEGAL file in the code repository */

package crp

import (
	"libgo/protocol"

	cp "org/modules/content/protocol"
	urp "org/modules/user-request/protocol"
	ctp "org/modules/content-type/protocol"
)

type DataModel interface {
	ContentID() cp.ContentUUID         //
	Priority() uint64                  // substitute priority
	PriorityType() ctp.ContentTypeUUID //
	RelatedID() cp.ContentUUID         //
	SaveTime() protocol.Time           //
	RequestID() urp.UserRequestUUID    //
}


