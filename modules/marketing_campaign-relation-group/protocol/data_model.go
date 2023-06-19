/* For license and copyright information please see the LEGAL file in the code repository */

/*
- To send SMS or ... to all user joined group. Join can be optional. DeJoin mechanism must be exist.
*/
package mcrgp

import (
	"libgo/protocol"

	urp "org/modules/user-request/protocol"
)

type DataModel interface {
	SaveTime() protocol.Time        //
	RequestID() urp.UserRequestUUID //
}
