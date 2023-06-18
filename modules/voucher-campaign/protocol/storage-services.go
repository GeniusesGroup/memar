/* For license and copyright information please see the LEGAL file in the code repository */

package vcp

import (
	"libgo/protocol"

	mcp "org/modules/marketing-campaign/protocol"
	vp "org/modules/voucher/protocol"
)

type StorageServices interface {
	Save(dm DataModel) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(voucherID vp.VoucherUUID) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(voucherID vp.VoucherUUID, vo protocol.VersionOffset) (dm DataModel, nv protocol.NumberOfVersion, err protocol.Error)

	FIND_VoucherIDs_BY_CampaignID(campaignID mcp.MarketingCampaignUUID, offset, limit uint64) (voucherIDs []vp.VoucherUUID, nv protocol.NumberOfVersion, err protocol.Error)
}
