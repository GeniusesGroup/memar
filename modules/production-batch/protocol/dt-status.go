/* For license and copyright information please see the LEGAL file in the code repository */

package pbp

import (
	qsp "org/modules/quiddity-status/protocol"
)

type Status qsp.Quiddity_Status

// 0//created 1//ManagerApprove 2//WarehouseApprove 3//ActiveWithApprove 4//ActiveWithoutApprove 5//ActiveWithOrderer 6//Inactive 7//Normal 8//Reject 9//Void
