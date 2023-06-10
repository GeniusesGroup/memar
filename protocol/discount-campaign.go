/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"

	urp "org/modules/user-request/protocol"
)

// DiscountCampaign indicate the domain record data fields.
type DiscountCampaign interface {
	DiscountID() DiscountUUID          //
	CampaignID() MarketingCampaignUUID 
	Time() protocol.Time               // save time
	RequestID() urp.UserRequestUUID    //
}

type DiscountCampaign_StorageServices interface {
	Save(dm DiscountCampaign) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(discountID DiscountUUID) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(discountID DiscountUUID, vo protocol.VersionOffset) (dm DiscountCampaign, nv protocol.NumberOfVersion, err protocol.Error)

	FIND_DiscountIDs_BY_CampaignID(campaignID MarketingCampaignUUID, offset, limit uint64) (discountIDs []DiscountUUID, nv protocol.NumberOfVersion, err protocol.Error)
}
