/* For license and copyright information please see the LEGAL file in the code repository */

package dcp

import (
	"memar/protocol"

	arp "org/modules/app-request/protocol"
	dp "org/modules/discount/protocol"
	mcp "org/modules/marketing-campaign/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	DiscountID() dp.DiscountUUID
	CampaignID() mcp.MarketingCampaignUUID

	arp.AuditLogging
	protocol.Storage_Versioned
	protocol.Storage_SaveTime
}
