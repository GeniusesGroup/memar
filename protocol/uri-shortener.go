/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"
)

type URIShortener interface {
	ID() string                  // Short Unique ID
	URI() string                 // UUID of picture object.
	UserID() protocol.UserID     // user domain
	Status() URIShortener_Status //
	Time() protocol.Time         // save time
	RequestID() UserRequestUUID  // user-request domain
}

const shortenerPath = "/s"

type URIShortener_Status Quiddity_Status
