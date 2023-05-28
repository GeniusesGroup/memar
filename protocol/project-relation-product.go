/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"

	urp "org/modules/user-request/protocol"
)

// ProjectProductRelation indicate the domain record data fields.
type ProjectProductRelation interface {
	ProjectID() ProjectUUID //
	ProductID() ProductUUID //
	// TODO::: type or label??
	Time() protocol.Time            // Save time
	RequestID() urp.UserRequestUUID //
}
