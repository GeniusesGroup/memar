/* For license and copyright information please see the LEGAL file in the code repository */

package services

import "../../libgo/achaemenid"

// GetOrgConnectionReq is the request structure of GetOrgConnection()
type GetOrgConnectionReq struct {
	OrgID [16]byte `valid:"UUID"`
	AppID [16]byte `valid:"UUID"`
}

// GetOrgConnectionRes is the response structure of GetOrgConnection()
type GetOrgConnectionRes struct {
	achaemenid.Connection
}

// GetOrgConnection use to update and get related connection data.
func GetOrgConnection(st *achaemenid.Stream, req *GetOrgConnectionReq) (*GetOrgConnectionRes, error) {
	/*
		---------- Authorization ----------
	*/

	// Delegate user can't get org connection for any user!
	if cst.Connection.OwnerID != cst.Connection.DelegateUserID {
		// return
	}

	cst.AuthorizeWhich()
	cst.AuthorizeWhere()
	if cst.Err != nil {
		return nil, cst.Err
	}

	/*
		---------- Bussiness logic ----------
	*/
	var (
		res GetOrgConnectionRes
		err error
	)

	// Check exist not expired connection with same cst.Connection.OwnerID & req.AppID & req.OrgID
	// If exist use same connectionID and update AccessControl list
	// res.ConnectionID =

	// Get all user joined group info with same req.AppID

	// set data to response
	res.OwnerID = req.OrgID
	res.DelegateUserID = cst.Connection.OwnerID

	return &res, err
}
