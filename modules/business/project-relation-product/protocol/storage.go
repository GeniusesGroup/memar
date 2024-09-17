/* For license and copyright information please see the LEGAL file in the code repository */

package prpp

import (
	"memar/protocol"

	prp "org/modules/product/protocol"
	pp "org/modules/project/protocol"
)

type StorageServices interface {
	Save(dm DataModel) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(projectID pp.ProjectUUID, productID prp.ProductUUID) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(projectID pp.ProjectUUID, productID prp.ProductUUID, vo protocol.VersionOffset) (dm DataModel, nv protocol.NumberOfVersion, err protocol.Error)

	LIST_ProductIDs_BY_ProjectID(projectID pp.ProjectUUID, offset, limit uint64) (productIDs []prp.ProductUUID, nv protocol.NumberOfVersion, err protocol.Error)
	LIST_ProjectIDs_BY_ProductID(productID prp.ProductUUID, offset, limit uint64) (projectIDs []pp.ProjectUUID, nv protocol.NumberOfVersion, err protocol.Error)
}
