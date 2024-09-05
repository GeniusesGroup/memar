/* For license and copyright information please see the LEGAL file in the code repository */

package department_p

import (
	ut16 "memar/identifier/uuid-time-16byte"
)

type Field_DepartmentID interface {
	DepartmentID() DepartmentUUID
}

type DepartmentUUID ut16.UUID
