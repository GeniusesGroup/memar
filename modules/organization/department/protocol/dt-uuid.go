/* For license and copyright information please see the LEGAL file in the code repository */

package department_p

import (
	group_p "org/modules/organization/group/protocol"
)

type Field_DepartmentID interface {
	DepartmentID() UUID
}

type UUID group_p.UUID
