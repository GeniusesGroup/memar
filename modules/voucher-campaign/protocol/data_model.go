/* For license and copyright information please see the LEGAL file in the code repository */

package vcp

import (
	"libgo/protocol"

	mcp "org/modules/marketing-campaign/protocol"
	urp "org/modules/user-request/protocol"
	vp "org/modules/voucher/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	VoucherID() vp.VoucherUUID             //
	CampaignID() mcp.MarketingCampaignUUID //
	SaveTime() protocol.Time               //
	RequestID() urp.UserRequestUUID        //
}
