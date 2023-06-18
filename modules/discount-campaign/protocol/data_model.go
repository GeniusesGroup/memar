/* For license and copyright information please see the LEGAL file in the code repository */

package dcp

import (
	"libgo/protocol"

	dp "org/modules/discount/protocol"
	mcp "org/modules/marketing-campaign/protocol"
	urp "org/modules/user-request/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	DiscountID() dp.DiscountUUID //
	CampaignID() mcp.MarketingCampaignUUID
	SaveTime() protocol.Time        //
	RequestID() urp.UserRequestUUID //
}


