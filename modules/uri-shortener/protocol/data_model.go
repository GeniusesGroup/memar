/* For license and copyright information please see the LEGAL file in the code repository */

package usp

import (
	"libgo/protocol"

	qsp "org/modules/quiddity-status/protocol"
	urp "org/modules/user-request/protocol"
	up "org/modules/user/protocol"
)

type DataModel interface {
	ID() string                     // Short Unique ID
	URI() string                    // e.g. UUID of picture object.
	UserID() up.UserUUID            //
	Status() Status                 //
	SaveTime() protocol.Time        //
	RequestID() urp.UserRequestUUID //
}

const shortenerPath = "/s"

type Status qsp.Quiddity_Status
