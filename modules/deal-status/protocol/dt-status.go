/* For license and copyright information please see the LEGAL file in the code repository */

package osp

import (
	qsp "org/modules/quiddity-status/protocol"
)

type Status qsp.Quiddity_Status

const (
	Status_Pending = Status(qsp.Quiddity_Status_FreeFlag << iota) // Wait to approve
	Status_NeedApprovement
	Status_Approved
	Status_PartiallyDeal
	Status_FullyDeal
	Status_Expired
	Status_Cancelled // Voided
)
