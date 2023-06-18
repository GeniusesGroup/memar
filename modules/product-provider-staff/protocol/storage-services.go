/* For license and copyright information please see the LEGAL file in the code repository */

package ppsp

import (
	"libgo/protocol"

	pp "org/modules/product/protocol"
	sp "org/modules/staff/protocol"
)

type StorageServices interface {
	Save(dm DataModel) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(productID pp.ProductUUID, staffID sp.StaffUUID) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(productID pp.ProductUUID, staffID sp.StaffUUID, vo protocol.VersionOffset) (dm DataModel, nv protocol.NumberOfVersion, err protocol.Error)

	LIST_ProductIDs_BY_StaffID(staffID sp.StaffUUID, offset, limit uint64) (productIDs []pp.ProductUUID, nv protocol.NumberOfVersion, err protocol.Error)
	LIST_StaffIDs_BY_ProductID(productID pp.ProductUUID, offset, limit uint64) (staffIDs []sp.StaffUUID, nv protocol.NumberOfVersion, err protocol.Error)
}
