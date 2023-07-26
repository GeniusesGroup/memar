/* For license and copyright information please see the LEGAL file in the code repository */

package vcp

import (
	"memar/protocol"

	mcp "org/modules/marketing-campaign/protocol"
	vp "org/modules/voucher/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	VoucherID() vp.VoucherUUID
	CampaignID() mcp.MarketingCampaignUUID

	protocol.AuditLogging
	protocol.Storage_Versioned
	protocol.Storage_SaveTime
}
