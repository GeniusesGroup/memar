/* For license and copyright information please see the LEGAL file in the code repository */

package trmcp

import (
	"memar/protocol"

	mcp "org/modules/marketing-campaign/protocol"
	tp "org/modules/task/protocol"
)

type StorageServices interface {
	Save(dm DataModel) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(marketingCampaignID mcp.MarketingCampaignUUID, taskID tp.TaskUUID) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(marketingCampaignID mcp.MarketingCampaignUUID, taskID tp.TaskUUID, vo protocol.VersionOffset) (dm DataModel, nv protocol.NumberOfVersion, err protocol.Error)
}
