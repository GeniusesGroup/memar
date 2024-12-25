/* For license and copyright information please see the LEGAL file in the code repository */

package label

const (
	Status_Pending = iota // Wait to approve
	Status_NeedApprovement
	Status_Approved
	Status_PartiallyDeal
	Status_FullyDeal
	Status_Expired
	Status_Cancelled // Voided
)
