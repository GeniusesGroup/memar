/* For license and copyright information please see the LEGAL file in the code repository */

package trmcp

import (
	"libgo/protocol"

	mcp "org/modules/marketing-campaign/protocol"
	tp "org/modules/task/protocol"
	urp "org/modules/user-request/protocol"
)

// TODO::: Do we need this domain? what about relate to contents? relate to objects? relate to invoices(CRM)?
// I know that in GUI we can distinguish between them to show more data base on relations(e.g. invoice price, ...).
// I think we need to improve comment types to cover more types to support these domain relation.

// DataModel indicate the domain record data fields.
type DataModel interface {
	TaskID() tp.TaskUUID                            //
	MarketingCampaignID() mcp.MarketingCampaignUUID //
	RelationType() Type                             //
	SaveTime() protocol.Time                        // Save time
	RequestID() urp.UserRequestUUID                 //
}

type Type uint8
