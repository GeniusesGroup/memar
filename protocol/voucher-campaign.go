/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"

	urp "org/modules/user-request/protocol"
)

// VoucherCampaign indicate the domain record data fields.
type VoucherCampaign interface {
	VoucherID() VoucherUUID            //
	CampaignID() MarketingCampaignUUID //
	Time() protocol.Time               // save time
	RequestID() urp.UserRequestUUID    //
}

type VoucherCampaign_StorageServices interface {
	Save(vc VoucherCampaign) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(voucherID VoucherUUID) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(voucherID VoucherUUID, vo protocol.VersionOffset) (vc VoucherCampaign, nv protocol.NumberOfVersion, err protocol.Error)

	FindByCampaign(campaignID MarketingCampaignUUID, offset, limit uint64) (voucherIDs []VoucherUUID, nv protocol.NumberOfVersion, err protocol.Error)
}
