/* For license and copyright information please see the LEGAL file in the code repository */

package services

import "libgo/achaemenid"

var approveOrgPositionByPersonService = achaemenid.Service{
	ID:                0,
	Name:              "approveOrgPositionByPerson",
	IssueDate:         0,
	ExpiryDate:        0,
	ExpireInFavorOf:   "",
	ExpireInFavorOfID: 0,
	Status:            achaemenid.ServiceStatePreAlpha,
	Handler:           ApproveOrgPositionByPerson,
	Description: []string{
		``,
	},
	TAGS: []string{"OrganizationStaff"},
}

// ApproveOrgPositionByPerson will
func ApproveOrgPositionByPerson(s *achaemenid.Server, st *achaemenid.Stream) {}

func approveOrgPositionByPerson(st *achaemenid.Stream, req *approveOrgPositionByPersonReq) *approveOrgPositionByPersonRes {
	return nil
}

type approveOrgPositionByPersonReq struct {
	PositionID [16]byte
}

type approveOrgPositionByPersonRes struct {
}
