/* For license and copyright information please see the LEGAL file in the code repository */

package services

import "libgo/achaemenid"

// ReqGetRecordsList is the standard request structure of "GetRecordsList()".
type ReqGetRecordsList struct {
	UserID string `valid:"userID"`
	Offset string `valid:"offset"`
	Limit  string `valid:"limit"`
}

// GetRecordsList returns list of owner's records.
func GetRecordsList(st *achaemenid.Stream, req *ReqGetRecordsList) {
	var logicResponse microservice.LogicResponse

	// Validate request
	logicResponse.Error = validation.ValidateObject(logicRequest)
	if logicResponse.Error != nil {
		return &logicResponse
	}

	recordIDs := []string{}
	dbRequest := usersdata.Request{
		Keys: []string{"Record", logicRequest.UserID},
		Data: &recordIDs,
		Options: usersdata.Options{
			Offset: logicRequest.Offset,
			Limit:  logicRequest.Limit}}

	logicResponse.Error = usersdata.GetKeys(&dbRequest)
	if logicResponse.Error != nil {
		return &logicResponse
	}

	logicResponse.Payload = recordIDs

	return &logicResponse
}
