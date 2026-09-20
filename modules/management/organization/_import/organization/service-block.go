/* For license and copyright information please see the LEGAL file in the code repository */

package org

import "libgo/achaemenid"

var blockOrgService = achaemenid.Service{
	ID:                0,
	Name:              "BlockOrg",
	IssueDate:         0,
	ExpiryDate:        0,
	ExpireInFavorOf:   "",
	ExpireInFavorOfID: 0,
	Status:            achaemenid.ServiceStatePreAlpha,
	Handler:           BlockOrg,
	Description: []string{
		``,
	},
	TAGS: []string{"OrganizationAuthentication"},
}

// BlockOrg will
func BlockOrg(s *achaemenid.Server, st *achaemenid.Stream) {}

func blockOrg(st *achaemenid.Stream, req *blockOrgReq) {
	// Just justice MS can do this operation
}

type blockOrgReq struct {
}
