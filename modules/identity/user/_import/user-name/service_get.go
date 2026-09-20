/* For license and copyright information please see the LEGAL file in the code repository */

package services

import (
	"libgo/achaemenid"
	"libgo/protocol"
)

// GetNameReq is the request structure of GetName()
type GetNameReq struct {
	UserID [16]byte
}

// GetNameRes is the response structure of GetName()
type GetNameRes struct {
	Username string `valid:"userID"`
}

// GetName get UUID of user and return the user name.
func GetName(st *achaemenid.Stream, req GetNameReq) (res *GetNameRes, err protocol.Error) {
	//Ready dbRequest for database layer
	var profileDetails Profile
	dbRequest := usersdata.Request{
		Keys: []string{"Profiles", req.UserID},
		Data: &profileDetails}
	logicResponse.Error = usersdata.GetData(&dbRequest)
	if logicResponse.Error != nil {
		return nil, &logicResponse
	}

	logicResponse.LastModified = dbRequest.LastModified
	logicResponse.Payload = profileDetails
	return nil, &logicResponse
}
