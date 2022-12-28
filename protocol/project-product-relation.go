/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"
)

// ProjectProductRelation indicate the domain record data fields.
type ProjectProductRelation interface {
	ProjectID() ProjectUUID // group domain. use to get and show locale title.
	ProductID() ProductUUID //
	// TODO::: type or label??
	Time() protocol.Time        // Save time
	RequestID() UserRequestUUID // user-request domain
}
