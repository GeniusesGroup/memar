/* For license and copyright information please see the LEGAL file in the code repository */

package esp

import (
	"libgo/protocol"

	org "org/modules/org/protocol"
	urp "org/modules/user-request/protocol"
	up "org/modules/user/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	OrgID() org.OrgUUID             //
	UserID() up.UserUUID            //
	Score() uint64                  //
	SaveTime() protocol.Time        //
	RequestID() urp.UserRequestUUID //
}
