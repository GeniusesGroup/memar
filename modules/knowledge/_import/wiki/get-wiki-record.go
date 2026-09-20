/* For license and copyright information please see the LEGAL file in the code repository */

package services

import (
	"strings"

	"libgo/achaemenid"
)

// ReqGetRecord is the standard request structure of "GetRecord()".
type ReqGetRecord struct {
	UserID   string `valid:"userID"`
	RecordID string `valid:"wikiRecordID"`
}

// ResGetRecord is the standard request structure of "GetRecord()".
type ResGetRecord struct {
	// Wiki
}

// GetRecord create a new wiki record for owner.
func GetRecord(st *achaemenid.Stream, req *ReqGetRecord) {
	var logicResponse microservice.LogicResponse

	// Validate request
	logicResponse.Error = validation.ValidateObject(logicRequest)
	if logicResponse.Error != nil {
		return &logicResponse
	}

	if !strings.HasPrefix(logicRequest.RecordID, logicRequest.UserID) {
		logicResponse.Error = errors.AccessForbidden
		return &logicResponse
	}

	record := Record{}
	dbRequest := usersdata.Request{
		Keys: []string{"Record", logicRequest.RecordID},
		Data: &record}

	logicResponse.Error = usersdata.GetData(&dbRequest)
	if logicResponse.Error != nil {
		return &logicResponse
	}

	logicResponse.Payload = ResGetRecord{Record: record}

	return &logicResponse
}
