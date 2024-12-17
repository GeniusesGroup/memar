/* For license and copyright information please see the LEGAL file in the code repository */

package top

import (
	request_p "memar/audit/request/protocol"

	thing_p "org/modules/identity/thing/protocol"
	user_p "org/modules/identity/user/protocol"
	storage_p "org/modules/storage/primitive/protocol"
)

type ThingOwner interface {
	thing_p.Field_ThingID
	user_p.Field_OwnerID

	request_p.Field_RequestID
	storage_p.Field_SaveTime
}
