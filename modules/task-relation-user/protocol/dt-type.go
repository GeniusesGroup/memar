/* For license and copyright information please see the LEGAL file in the code repository */

package trup

type Type uint8

const (
	Type_Unset Type = iota
	Type_Participant
	Type_Assigner
	Type_Assigned
	Type_Reviewer
	Type_Approver
)
