/* For license and copyright information please see the LEGAL file in the code repository */

package vep

import (
	"memar/protocol"

	eblp "org/modules/estate-building-location/protocol"
	ebp "org/modules/estate-building/protocol"
	ep "org/modules/estate/protocol"
	sp "org/modules/storage/protocol"
	vp "org/modules/voucher/protocol"
)

type StorageServices interface {
	Save(dm DataModel) (err protocol.Error)

	Get(voucherID vp.VoucherUUID, vo sp.VersionOffset) (dm DataModel, err protocol.Error)

	FIND_VoucherIDs_BY_EstateID(EstateID ep.EstateUUID, offset, limit uint64) (voucherIDs []vp.VoucherUUID, num sp.NumberOfVersion, err protocol.Error)
	FIND_VoucherIDs_BY_BuildingID(buildingID ebp.BuildingUUID, offset, limit uint64) (voucherIDs []vp.VoucherUUID, num sp.NumberOfVersion, err protocol.Error)
	FIND_VoucherIDs_BY_BuildingLocationID(buildingLocationID eblp.BuildingLocationUUID, offset, limit uint64) (voucherIDs []vp.VoucherUUID, num sp.NumberOfVersion, err protocol.Error)
}
