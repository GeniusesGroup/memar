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

type ProjectProductRelation_StorageServices interface {
	Save(f ProjectProductRelation) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(productID ProductUUID, projectID ProjectUUID) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(productID ProductUUID, projectID ProjectUUID, vo protocol.VersionOffset) (f ProjectProductRelation, nv protocol.NumberOfVersion, err protocol.Error)
}
