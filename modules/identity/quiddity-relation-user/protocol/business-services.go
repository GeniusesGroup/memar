/* For license and copyright information please see the LEGAL file in the code repository */

package qru_p

import (
	quiddity_p "org/modules/identity/quiddity/protocol"
	user_p "org/modules/identity/user/protocol"
	storage_p "org/modules/storage/primitive/protocol"
)

type (
	BS_FindByUserID_Request interface {
		user_p.Field_UserID
		storage_p.Pagination_Offset_Request
	}
	BS_FindByUserID_Response interface {
		QuiddityIDs() []quiddity_p.UUID
		storage_p.Pagination_Response
	}
)
