/* For license and copyright information please see the LEGAL file in the code repository */

package shsp

import (
	qsp "org/modules/quiddity-status/protocol"
)

type Status qsp.Quiddity_Status

const (
	Status_Requester = Status(qsp.Quiddity_Status_FreeFlag << iota)
	Status_Referral
	Status_Talent // high skill match
	Status_NeedHRInterview
	Status_ApproveForHRInterview
	Status_NeedTechnicalInterview
	Status_ApproveForTechnicalInterview
	Status_NeedForManagerInterview
	Status_ApproveForManagerInterview
	Status_NeedForChiefInterview
	Status_ApproveForChiefInterview
	Status_NeedForBoardInterview
	Status_ApproveForBoardInterview

	// if not accepted or hired
	Status_LockFor1Month
	Status_LockFor3Month
	Status_LockFor6Month
	Status_LockFor12Month

	// if accepted
	Status_Designation
	Status_Negotiation
	Status_Reserved
	Status_ContractProposal
)
