/* For license and copyright information please see the LEGAL file in the code repository */

package qop

import (
	"libgo/protocol"

	qp "org/modules/quiddity/protocol"
	urp "org/modules/user-request/protocol"
	up "org/modules/user/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	QuiddityID() qp.QuiddityUUID    //
	UserID() up.UserUUID            // Owner of the quiddity
	SaveTime() protocol.Time        //
	RequestID() urp.UserRequestUUID //
}
