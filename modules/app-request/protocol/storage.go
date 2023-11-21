/* For license and copyright information please see the LEGAL file in the code repository */

package arp

import (
	"memar/protocol"

	up "org/modules/user/protocol"
)

// StorageServices indicates the domain storage layer services.
type StorageServices interface {
	Save(dm DataModel) (err protocol.Error)

	Get(requestID RequestUUID) (dm DataModel, err protocol.Error)

	FIND_RequestIDs_BY_DomainID(domainID protocol.MediaTypeID, offset, limit uint64) (requestIDs []RequestUUID, err protocol.Error)
	FIND_RequestIDs_BY_ServiceID(serviceID protocol.MediaTypeID, offset, limit uint64) (requestIDs []RequestUUID, err protocol.Error)
	FIND_RequestIDs_BY_UserID(userID up.UserUUID, offset, limit uint64) (requestIDs []RequestUUID, err protocol.Error)
}
