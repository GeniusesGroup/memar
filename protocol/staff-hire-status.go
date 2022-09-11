/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"github.com/GeniusesGroup/libgo/protocol"
)

type StaffHireStatus interface {
	UserID() protocol.UserID    // user domain
	Status() StaffHire_Status   //
	Time() protocol.Time        // save time
	RequestID() UserRequestUUID // user-request domain
}

type StaffHireStatus_StorageServices interface {
	Save(shs StaffHireStatus) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(userID [16]byte) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(userID [16]byte, vo protocol.VersionOffset) (shs StaffHireStatus, nv protocol.NumberOfVersion, err protocol.Error)

	// FilterByStatus(status StaffHire_Status, offset, limit uint64) (userIDs [][16]byte, nv protocol.NumberOfVersion, err protocol.Error)
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
