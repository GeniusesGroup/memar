/* For license and copyright information please see the LEGAL file in the code repository */

package qs_p

// qsp.Quiddity_Status indicate any quiddity record status
type Quiddity_Status uint64

// base quiddity status
const Quiddity_Status_Unset Quiddity_Status = 0
const (
	// by owner
	Quiddity_Status_Locked Quiddity_Status = (1 << iota)

	// by justice(admins) or fraud detection mechanism
	Quiddity_Status_Blocked

	// Due to some reason quiddity was Locked, Closed, ... and must not use or edit
	Quiddity_Status_PermanentInactivated
	Quiddity_Status_TemporaryInactivated
	Quiddity_Status_Hidden
	Quiddity_Status_Deleted
	Quiddity_Status_Revoked

	Quiddity_Status_ManuallyAdded    // data is belong to other application(org) and add by users by GUI
	Quiddity_Status_ManuallyVerified // manual added data in some way was verified.
	Quiddity_Status_Edited

	_
	_
	_
	_
	_
	_
	Quiddity_Status_FreeFlag
)
