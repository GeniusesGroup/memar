/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"

	urp "org/modules/user-request/protocol"
)

type StaffHireStatus interface {
	UserID() UserUUID               //
	Status() StaffHire_Status       //
	Time() protocol.Time            // save time
	RequestID() urp.UserRequestUUID //
}

type StaffHireStatus_StorageServices interface {
	Save(f StaffHireStatus) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(userID UserUUID) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(userID UserUUID, vo protocol.VersionOffset) (f StaffHireStatus, nv protocol.NumberOfVersion, err protocol.Error)

	Find_ByStatus(status StaffHire_Status, offset, limit uint64) (userIDs []UserUUID, nv protocol.NumberOfVersion, err protocol.Error)
	Find_ByStatus_Current(status StaffHire_Status, offset, limit uint64) (userIDs []UserUUID, nv protocol.NumberOfVersion, err protocol.Error)

	// protocol.EventTarget
}

type StaffHire_Status Quiddity_Status

const (
	StaffHire_Status_Requester = StaffHire_Status(Quiddity_Status_FreeFlag << iota)
	StaffHire_Status_Referral
	StaffHire_Status_Talent // high skill match
	StaffHire_Status_NeedHRInterview
	StaffHire_Status_ApproveForHRInterview
	StaffHire_Status_NeedTechnicalInterview
	StaffHire_Status_ApproveForTechnicalInterview
	StaffHire_Status_NeedForManagerInterview
	StaffHire_Status_ApproveForManagerInterview
	StaffHire_Status_NeedForChiefInterview
	StaffHire_Status_ApproveForChiefInterview
	StaffHire_Status_NeedForBoardInterview
	StaffHire_Status_ApproveForBoardInterview

	// if not accepted or hired
	StaffHire_Status_LockFor1Month
	StaffHire_Status_LockFor3Month
	StaffHire_Status_LockFor6Month
	StaffHire_Status_LockFor12Month

	// if accepted
	StaffHire_Status_Designation
	StaffHire_Status_Negotiation
	StaffHire_Status_Reserved
	StaffHire_Status_ContractProposal
)
