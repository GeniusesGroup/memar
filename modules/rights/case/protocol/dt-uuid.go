/* For license and copyright information please see the LEGAL file in the code repository */

package case_p

import (
	group_p "org/modules/organization/group/protocol"
)

type Field_CaseID interface {
	CaseID() UUID
}

// a comprehensive term for any proceeding in a court of law whereby an individual seeks a legal remedy
type UUID group_p.UUID
