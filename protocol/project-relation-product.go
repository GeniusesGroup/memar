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
	Status() ProjectProductRelation_Status
	// TODO::: type or label??
	Time() protocol.Time            // Save time
	RequestID() urp.UserRequestUUID //
}

type ProjectProductRelation_StorageServices interface {
	Save(dm ProjectProductRelation) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(projectID ProjectUUID, productID ProductUUID) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(projectID ProjectUUID, productID ProductUUID, vo protocol.VersionOffset) (dm ProjectProductRelation, nv protocol.NumberOfVersion, err protocol.Error)

	LIST_ProductIDs_BY_ProjectID(projectID ProjectUUID, offset, limit uint64) (productIDs []ProductUUID, nv protocol.NumberOfVersion, err protocol.Error)
	LIST_ProjectIDs_BY_ProductID(productID ProductUUID, offset, limit uint64) (projectIDs []ProjectUUID, nv protocol.NumberOfVersion, err protocol.Error)
}

type ProjectProductRelation_Status Quiddity_Status
