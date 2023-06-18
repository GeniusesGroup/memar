/* For license and copyright information please see the LEGAL file in the code repository */

package cp

import (
	"libgo/protocol"

	ctp "org/modules/content-type/protocol"
	urp "org/modules/user-request/protocol"
	up "org/modules/user/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	ContentID() ContentUUID             //
	UserID() up.UserUUID                //
	ContentTypeID() ctp.ContentTypeUUID //
	SaveTime() protocol.Time            //
	RequestID() urp.UserRequestUUID     //
}

