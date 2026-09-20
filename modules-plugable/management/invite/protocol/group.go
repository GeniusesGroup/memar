/* For license and copyright information please see the LEGAL file in the code repository */

package ig_p

import (
	group_p "org/modules/management/group/protocol"
)

// Limit to this group
type Group interface {
	group_p.Field_GroupID
}
