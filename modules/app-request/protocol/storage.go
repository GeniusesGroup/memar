/* For license and copyright information please see the LEGAL file in the code repository */

package arp

import (
	"memar/protocol"

	aap "org/modules/app-audit/protocol"
	// amp "org/modules/app-module/protocol"
	asp "org/modules/app-service/protocol"
	up "org/modules/user/protocol"
)

// StorageServices indicates the domain storage layer services.
type StorageServices interface {
	Save(dm DataModel) (err protocol.Error)

	Get(requestID aap.RequestUUID) (dm DataModel, err protocol.Error)

	FIND_RequestIDs_BY_UserID(userID up.UserUUID, offset, limit uint64) (requestIDs []aap.RequestUUID, err protocol.Error)
	FIND_RequestIDs_BY_ServiceID(serviceID asp.ServiceUUID, offset, limit uint64) (requestIDs []aap.RequestUUID, err protocol.Error)

	// TODO::: Is it GUI service that find by ServiceID and filter by other data??
	// FILTER_RequestIDs_BY_DomainID(domainID amp.ModuleUUID, offset, limit uint64) (requestIDs []aap.RequestUUID, err protocol.Error)
}
