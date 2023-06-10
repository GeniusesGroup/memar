/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"

	urp "org/modules/user-request/protocol"
	up "org/modules/user/protocol"
)

type URIShortener interface {
	ID() string                     // Short Unique ID
	URI() string                    // e.g. UUID of picture object.
	UserID() up.UserUUID            //
	Status() URIShortener_Status    //
	Time() protocol.Time            // save time
	RequestID() urp.UserRequestUUID //
}

const shortenerPath = "/s"

type URIShortener_Status Quiddity_Status
