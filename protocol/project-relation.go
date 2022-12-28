/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"
)

// ProjectRelation indicate the domain record data fields.
type ProjectRelation interface {
	ProjectID() ProjectUUID //
	OtherID() ProjectUUID   //
	// TODO::: type or label??
	Time() protocol.Time        // Save time
	RequestID() UserRequestUUID // user-request domain
}
