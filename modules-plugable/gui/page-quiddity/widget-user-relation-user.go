/* For license and copyright information please see the LEGAL file in the code repository */

package up_p

import (
	error_p "memar/process/error/protocol"

	storage_p "memar/storage/protocol"
	org_p "org/modules/identity/organization/protocol"
	user_p "org/modules/identity/user/protocol"
)

type Widget_user_relation_user interface {
	GetIDs(orgID org_p.UUID, offset, limit uint64) (userIDs []user_p.UUID, nv storage_p.NumberOfVersion, err error_p.Error)

	// FilterByStatus(status UserOtherApp_Status, offset, limit uint64) (userIDs []user_p.UUID, nv storage_p.NumberOfVersion, err error_p.Error)
	// FindByTime(day earth.Day, offset, limit uint64) (userIDs []user_p.UUID, nv storage_p.NumberOfVersion, err error_p.Error)
}
