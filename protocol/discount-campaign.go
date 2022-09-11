/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"github.com/GeniusesGroup/libgo/protocol"
)

// DiscountCampaign indicate the domain record data fields.
type DiscountCampaign interface {
	DiscountID() [16]byte       // discount domain
	CampaignID() [16]byte       // marketing-campaign domain
	Time() protocol.Time        // save time
	RequestID() UserRequestUUID // user-request domain
}

type DiscountCampaign_StorageServices interface {
	Save(dc DiscountCampaign) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(discountID [16]byte) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(discountID [16]byte, vo protocol.VersionOffset) (dc DiscountCampaign, nv protocol.NumberOfVersion, err protocol.Error)
}
