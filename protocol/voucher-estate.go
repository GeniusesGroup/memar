/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"

	urp "org/modules/user-request/protocol"
)

// VoucherEstate indicate the domain record data fields.
// VoucherEstate is proper or appropriate location indicate specific area not specific location
// It's rule depend on products in invoices e.g. source or destination of taxi as a service(product).
type VoucherEstate interface {
	VoucherID() VoucherUUID                   //
	EstateID() EstateUUID                     //
	BuildingID() BuildingUUID                 //
	BuildingLocationID() BuildingLocationUUID //
	Time() protocol.Time                      // save time
	RequestID() urp.UserRequestUUID           //
}

type VoucherEstate_StorageServices interface {
	Save(dm VoucherEstate) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(voucherID VoucherUUID) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(voucherID VoucherUUID, vo protocol.VersionOffset) (dm VoucherEstate, nv protocol.NumberOfVersion, err protocol.Error)

	FIND_VoucherIDs_BY_EstateID(EstateID EstateUUID, offset, limit uint64) (voucherIDs []VoucherUUID, nv protocol.NumberOfVersion, err protocol.Error)
	FIND_VoucherIDs_BY_BuildingID(buildingID BuildingUUID, offset, limit uint64) (voucherIDs []VoucherUUID, nv protocol.NumberOfVersion, err protocol.Error)
	FIND_VoucherIDs_BY_BuildingLocationID(buildingLocationID BuildingLocationUUID, offset, limit uint64) (voucherIDs []VoucherUUID, nv protocol.NumberOfVersion, err protocol.Error)
}
