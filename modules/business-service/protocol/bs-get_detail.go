/* For license and copyright information please see the LEGAL file in the code repository */

package bs_p

import (
	org_p "org/modules/org/protocol"
	storage_p "org/modules/storage/protocol"
)

type (
	BS_GetDetail_Request interface {
		org_p.Field_OrganizationID
		storage_p.Pagination_Offset_Request
	}

	BS_GetDetail_Response interface {
		IDs() [][32]byte
	}
)
