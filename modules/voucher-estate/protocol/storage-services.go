/* For license and copyright information please see the LEGAL file in the code repository */

package vep

import (
	"memar/protocol"

	eblp "org/modules/estate-building-location/protocol"
	ebp "org/modules/estate-building/protocol"
	ep "org/modules/estate/protocol"
	vp "org/modules/voucher/protocol"
)

type StorageServices interface {
	Save(dm DataModel) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(voucherID vp.VoucherUUID) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(voucherID vp.VoucherUUID, vo protocol.VersionOffset) (dm DataModel, nv protocol.NumberOfVersion, err protocol.Error)

	FIND_VoucherIDs_BY_EstateID(EstateID ep.EstateUUID, offset, limit uint64) (voucherIDs []vp.VoucherUUID, nv protocol.NumberOfVersion, err protocol.Error)
	FIND_VoucherIDs_BY_BuildingID(buildingID ebp.BuildingUUID, offset, limit uint64) (voucherIDs []vp.VoucherUUID, nv protocol.NumberOfVersion, err protocol.Error)
	FIND_VoucherIDs_BY_BuildingLocationID(buildingLocationID eblp.BuildingLocationUUID, offset, limit uint64) (voucherIDs []vp.VoucherUUID, nv protocol.NumberOfVersion, err protocol.Error)
}
