/* For license and copyright information please see the LEGAL file in the code repository */

package plp

import (
	"memar/protocol"

	org "org/modules/org/protocol"
	pp "org/modules/product/protocol"
)

type StorageServices interface {
	Save(dm DataModel) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(productID pp.ProductUUID, orgID org.OrgUUID) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(productID pp.ProductUUID, orgID org.OrgUUID, vo protocol.VersionOffset) (dm DataModel, nv protocol.NumberOfVersion, err protocol.Error)

	LIST_ProductIDs_BY_OrgID(orgID org.OrgUUID, offset, limit uint64) (productIDs []pp.ProductUUID, nv protocol.NumberOfVersion, err protocol.Error)
	LIST_OrgIDs_By_ProductID(productID pp.ProductUUID, offset, limit uint64) (orgIDs []org.OrgUUID, nv protocol.NumberOfVersion, err protocol.Error)
}
