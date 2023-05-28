/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"

	urp "org/modules/user-request/protocol"
)

// ProjectTiming indicate the domain record data fields.
type ProjectTiming interface {
	ProjectID() ProjectUUID         //
	ExpectedTime() protocol.Time    //
	Deadline() protocol.Time        //
	Time() protocol.Time            // save time
	RequestID() urp.UserRequestUUID //
}
