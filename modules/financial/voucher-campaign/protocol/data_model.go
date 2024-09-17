/* For license and copyright information please see the LEGAL file in the code repository */

package vcp

import (
	aap "org/modules/app-audit/protocol"
	mcp "org/modules/marketing-campaign/protocol"
	sp "org/modules/storage/protocol"
	vp "org/modules/voucher/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	vp.VoucherID
	CampaignID() mcp.MarketingCampaignUUID

	aap.AuditRequest
	sp.SaveTime
}
