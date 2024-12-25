/* For license and copyright information please see the LEGAL file in the code repository */

package label

const (
	Status_Draft     = iota
	Status_Approving // AWAITING APPROVAL
	Status_Approved
	Status_Rejected
	Status_Processing // In progress, Pending
	Status_Processed  // Completed
	Status_Failed
	Status_Canceled
)

// COMPENSATED
