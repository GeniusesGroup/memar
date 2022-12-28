/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"
)

// VoucherCampaign indicate the domain record data fields.
type VoucherCampaign interface {
	VoucherID() [16]byte        // voucher domain
	CampaignID() [16]byte       // marketing-campaign domain
	Time() protocol.Time        // save time
	RequestID() UserRequestUUID // user-request domain
}

type VoucherCampaign_StorageServices interface {
	Save(vc VoucherCampaign) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(voucherID [16]byte) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(voucherID [16]byte, vo protocol.VersionOffset) (vc VoucherCampaign, nv protocol.NumberOfVersion, err protocol.Error)

	FindByCampaign(campaignID [16]byte, offset, limit uint64) (voucherIDs [][16]byte, nv protocol.NumberOfVersion, err protocol.Error)
}
