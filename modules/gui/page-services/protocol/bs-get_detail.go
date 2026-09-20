/* For license and copyright information please see the LEGAL file in the code repository */

package service_p

import (
	container_p "memar/computer/adt/container/protocol"

	org_p "org/modules/identity/organization/protocol"
)

type (
	BS_GetDetail_Request interface {
		org_p.Field_OrganizationID
		container_p.Pagination_Offset_Request
	}

	BS_GetDetail_Response interface {
		IDs() [][32]byte
	}
)
