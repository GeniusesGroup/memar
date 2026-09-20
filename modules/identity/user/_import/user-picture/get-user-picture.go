/* For license and copyright information please see the LEGAL file in the code repository */

package services

// Profile Pictures
// We send in array. first pic is default one.

// GetPictureReq is the request structure of GetPicture()
type GetPictureReq struct {
	UserID string `valid:"userID"`
}

// GetPicture : Get UUID of user and return the profile of user.
func GetPicture(req *GetPictureReq) error {
	//Ready dbRequest for database layer
	var profileDetails Profile
	dbRequest := usersdata.Request{
		Keys: []string{"Profiles", req.UserID},
		Data: &profileDetails}
	logicResponse.Error = usersdata.GetData(&dbRequest)
	if logicResponse.Error != nil {
		return &logicResponse
	}

	logicResponse.LastModified = dbRequest.LastModified
	logicResponse.Payload = profileDetails
	return &logicResponse
}
