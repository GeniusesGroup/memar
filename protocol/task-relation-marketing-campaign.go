/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"

	urp "org/modules/user-request/protocol"
)

// TODO::: Do we need this domain? what about relate to contents? relate to objects? relate to invoices(CRM)?
// I know that in GUI we can distinguish between them to show more data base on relations(e.g. invoice price, ...).
// I think we need to improve comment types to cover more types to support these domain relation.

// TaskRelationMarketingCampaign indicate the domain record data fields.
type TaskRelationMarketingCampaign interface {
	TaskID() TaskUUID                                 //
	MarketingCampaignID() MarketingCampaignUUID       //
	RelationType() TaskRelationMarketingCampaign_Type //
	Time() protocol.Time                              // Save time
	RequestID() urp.UserRequestUUID                   //
}

type TaskRelationMarketingCampaign_Type uint8
